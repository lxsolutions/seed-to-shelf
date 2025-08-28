








"""
Generate seed data for traceability service.
"""

import datetime
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import our models
import models

def generate_seed_data():
    """Generate seed data for traceability service."""
    print("Generating seed data...")

    # Create a mock database connection (in-memory)
    engine = create_engine('sqlite:///:memory:')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    # Create tables
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Generate sample compliance events
        print("Creating compliance events...")

        events_data = [
            {
                "entity_ref": "lot-12345",
                "cte_type": "Receive",
                "data": {
                    "quantity": 10,
                    "location": "Kitchen A",
                    "timestamp": datetime.datetime.utcnow().isoformat()
                },
                "ts": datetime.datetime.utcnow()
            },
            {
                "entity_ref": "lot-67890",
                "cte_type": "Transform",
                "data": {
                    "input_lots": ["lot-12345"],
                    "output_lot": "lot-transformed",
                    "process": "Chopping and mixing",
                    "timestamp": datetime.datetime.utcnow().isoformat()
                },
                "ts": datetime.datetime.utcnow()
            },
            {
                "entity_ref": "order-98765",
                "cte_type": "Ship",
                "data": {
                    "lot_codes": ["lot-transformed"],
                    "destination": "Consumer address",
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "delivery_method": "Driver"
                },
                "ts": datetime.datetime.utcnow()
            }
        ]

        for event_data in events_data:
            event = models.ComplianceEvent(**event_data)
            db.add(event)

        # Generate sample lot lineage
        print("Creating lot lineage records...")

        lineages = [
            {
                "lot_code": "lot-12345",
                "parent_lot_codes": ["batch-xyz"],
                "child_lot_codes": ["lot-transformed"],
                "order_ids": []
            },
            {
                "lot_code": "lot-transformed",
                "parent_lot_codes": ["lot-12345"],
                "child_lot_codes": [],
                "order_ids": ["order-98765"]
            }
        ]

        for lineage_data in lineages:
            lineage = models.LotLineage(**lineage_data)
            db.add(lineage)

        # Generate sample configuration
        print("Creating traceability config...")

        configs = [
            {
                "key": "retention_period_days",
                "value": {"days": 365}
            },
            {
                "key": "max_lot_size",
                "value": {"units": 100, "unit_type": "grams"}
            }
        ]

        for config_data in configs:
            config = models.TraceabilityConfig(**config_data)
            db.add(config)

        # Commit all data
        db.commit()
        print(f"Generated {db.query(models.ComplianceEvent).count()} compliance events")
        print(f"Generated {db.query(models.LotLineage).count()} lot lineage records")
        print(f"Generated {db.query(models.TraceabilityConfig).count()} config entries")

    finally:
        db.close()

if __name__ == "__main__":
    generate_seed_data()
    print("Seed data generation completed!")





