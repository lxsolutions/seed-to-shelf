










import psycopg2
from datetime import datetime, timedelta

def seed_database():
    """Seed the database with demo data for testing"""
    conn = psycopg2.connect(
        dbname="s2c",
        user="user",
        password="password",
        host="localhost"
    )
    cursor = conn.cursor()

    # Create tables if they don't exist
    create_tables(cursor)

    # Seed users (consumers, chefs)
    seed_users(cursor)

    # Seed kitchens
    seed_kitchens(cursor)

    # Seed permits
    seed_permits(cursor)

    # Seed ingredients and farm batches
    seed_ingredients_and_batches(cursor)

    # Seed dishes
    seed_dishes(cursor)

    # Seed orders
    seed_orders(cursor)

    conn.commit()
    cursor.close()
    conn.close()

def create_tables(cursor):
    """Create necessary tables for demo data"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            role VARCHAR(20),
            identity_verification BOOLEAN DEFAULT FALSE,
            rating FLOAT DEFAULT 5.0,
            location TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kitchens (
            id SERIAL PRIMARY KEY,
            owner_user_id INTEGER REFERENCES users(id),
            type VARCHAR(20),
            permits JSONB[],
            inspections JSONB[],
            geo GEOGRAPHY(Point, 4326)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chefs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            kitchen_id INTEGER REFERENCES kitchens(id),
            skills TEXT[],
            availability JSONB,
            training_badges TEXT[]
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS permits (
            id SERIAL PRIMARY KEY,
            kitchen_id INTEGER REFERENCES kitchens(id),
            jurisdiction_code VARCHAR(50),
            permit_type VARCHAR(50),
            status VARCHAR(20),
            docs JSONB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id SERIAL PRIMARY KEY,
            name TEXT,
            allergens TEXT[],
            nutrition JSONB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farm_batches (
            id SERIAL PRIMARY KEY,
            method VARCHAR(50),
            crop TEXT,
            planned_yield FLOAT,
            planted_at TIMESTAMP,
            harvest_at TIMESTAMP,
            sensors JSONB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lots (
            id SERIAL PRIMARY KEY,
            ingredient_id INTEGER REFERENCES ingredients(id),
            farm_batch_id INTEGER REFERENCES farm_batches(id),
            lot_code TEXT UNIQUE,
            harvest_date TIMESTAMP,
            FTL_flag BOOLEAN DEFAULT FALSE,
            trace_meta JSONB
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dishes (
            id SERIAL PRIMARY KEY,
            chef_id INTEGER REFERENCES chefs(id),
            name TEXT,
            recipe_steps JSONB,
            required_ingredients INTEGER[],
            risk_level VARCHAR(20),
            jurisdictions_allowed TEXT[]
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            consumer_id INTEGER REFERENCES users(id),
            status VARCHAR(50),
            delivery_mode VARCHAR(20),
            address TEXT,
            price FLOAT,
            tax FLOAT DEFAULT 0.0,
            tip FLOAT DEFAULT 0.0,
            assigned_chef_id INTEGER REFERENCES chefs(id)
        )
    """)

def seed_users(cursor):
    """Seed user data"""
    users = [
        # Consumers
        {"role": "consumer", "location": "San Mateo, CA"},
        {"role": "consumer", "location": "Boulder, CO"},

        # Chefs - will be linked to kitchens and dishes
        {"role": "chef", "location": "San Mateo, CA"},
        {"role": "chef", "location": "Boulder, CO"},
        {"role": "chef", "location": "Denver, CO"}
    ]

    for user in users:
        cursor.execute("""
            INSERT INTO users (role, location)
            VALUES (%s, %s) RETURNING id
        """, (user['role'], user['location']))

def seed_kitchens(cursor):
    """Seed kitchen data"""
    kitchens = [
        {
            "owner_user_id": 3,  # Chef in San Mateo
            "type": "HOME",
            "geo": "SRID=4326;POINT(-122.278 37.509)"
        },
        {
            "owner_user_id": 4,  # Chef in Boulder
            "type": "HOME",
            "geo": "SRID=4326;POINT(-105.28 40.015)"
        },
        {
            "owner_user_id": 5,  # Commercial chef in Denver
            "type": "COMMERCIAL",
            "geo": "SRID=4326;POINT(-104.99 39.739)"
        }
    ]

    for kitchen in kitchens:
        cursor.execute("""
            INSERT INTO kitchens (owner_user_id, type, geo)
            VALUES (%s, %s, ST_GeogFromText(%s)) RETURNING id
        """, (kitchen['owner_user_id'], kitchen['type'], kitchen['geo']))

def seed_permits(cursor):
    """Seed permit data"""
    permits = [
        {
            "kitchen_id": 1,
            "jurisdiction_code": "CA_SAN_MATEO_MEHKO",
            "permit_type": "MEHKO",
            "status": "approved"
        },
        {
            "kitchen_id": 2,
            "jurisdiction_code": "CO_BOULDER_COTTAGE",
            "permit_type": "COTTAGE_FOODS",
            "status": "approved"
        }
    ]

    for permit in permits:
        cursor.execute("""
            INSERT INTO permits (kitchen_id, jurisdiction_code, permit_type, status)
            VALUES (%s, %s, %s, %s)
        """, (permit['kitchen_id'], permit['jurisdiction_code'],
              permit['permit_type'], permit['status']))

def seed_ingredients_and_batches(cursor):
    """Seed ingredients and farm batches"""
    # Ingredients
    ingredients = [
        {"name": "Organic Lettuce", "allergens": []},
        {"name": "Heirloom Tomatoes", "allergens": ["tomato"]},
        {"name": "Fresh Basil", "allergens": []}
    ]

    for ingredient in ingredients:
        cursor.execute("""
            INSERT INTO ingredients (name, allergens)
            VALUES (%s, %s) RETURNING id
        """, (ingredient['name'], ingredient['allergens']))

    # Farm batches
    batch_ids = []
    now = datetime.now()
    for i in range(3):
        cursor.execute("""
            INSERT INTO farm_batches (
                method, crop, planned_yield,
                planted_at, harvest_at, sensors
            ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """, (
            "HYDROPONIC",
            f"Crop {i+1}",
            50.0 + i * 20,
            now - timedelta(days=30),
            now + timedelta(days=10),
            {}
        ))

def seed_dishes(cursor):
    """Seed dish data"""
    dishes = [
        {
            "chef_id": 1,  # San Mateo chef
            "name": "Farm Fresh Salad",
            "required_ingredients": [1, 2],  # Lettuce + Tomatoes
            "risk_level": "low"
        },
        {
            "chef_id": 2,  # Boulder chef
            "name": "Cottage Food Cookies",
            "required_ingredients": [],
            "risk_level": "none"
        }
    ]

    for dish in dishes:
        cursor.execute("""
            INSERT INTO dishes (
                chef_id, name,
                required_ingredients, risk_level
            ) VALUES (%s, %s, %s, %s)
        """, (dish['chef_id'], dish['name'],
              dish['required_ingredients'], dish['risk_level']))

def seed_orders(cursor):
    """Seed order data"""
    orders = [
        {
            "consumer_id": 1,
            "status": "completed",
            "delivery_mode": "PICKUP"
        },
        {
            "consumer_id": 2,
            "status": "in_progress",
            "delivery_mode": "DRIVER"
        }
    ]

    for order in orders:
        cursor.execute("""
            INSERT INTO orders (
                consumer_id, status, delivery_mode
            ) VALUES (%s, %s, %s)
        """, (order['consumer_id'], order['status'],
              order['delivery_mode']))

if __name__ == "__main__":
    seed_database()
    print("Database seeded with demo data!")










