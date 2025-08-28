





# Seed to Chef Operations Guide

## Table of Contents
1. [Local Development Setup](#local-development-setup)
2. [Docker Compose Configuration](#docker-compose-configuration)
3. [Service Deployment](#service-deployment)
4. [Database Management](#database-management)
5. [Environment Variables](#environment-variables)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Restore Procedures](#backup-and-restore-procedures)

## Local Development Setup

### Prerequisites
- Docker 20+
- Node.js v18 or later
- Python 3.11
- pnpm (JavaScript package manager)
- Poetry (Python dependency management)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lxsolutions/seed-to-chef.git
   cd seed-to-chef
   ```

2. **Install JavaScript dependencies**:
   ```bash
   pnpm install --frozen-lockfile
   ```

3. **Install Python dependencies for all services**:
   ```bash
   poetry install --all
   ```

4. **Create environment files** (copy templates):
   ```bash
   cp .env.template .env
   ```

## Docker Compose Configuration

The `docker-compose.yml` file in `/infra/docker/` defines the complete development stack:

- PostgreSQL database
- Redis cache
- Redpanda message broker
- MinIO object storage
- Jaeger tracing system
- All backend services (API, traceability, etc.)

### Starting the Development Stack

```bash
cd /workspace/seed-to-chef/infra/docker
docker-compose up -d --build
```

This command will:
1. Build all service containers
2. Start the database and messaging systems
3. Launch the API service on port 8000

## Service Deployment

### Kubernetes Deployment

The `/infra/k8s` directory contains Helm charts for production deployment:

```bash
# Deploy to a Kubernetes cluster
cd /workspace/seed-to-chef/infra/k8s
helm install s2c ./charts/s2c-api
```

### Service Endpoints

| Service | Port | Description |
|---------|------|-------------|
| API Gateway | 8000 | Main FastAPI service |
| Traceability | 8001 | Lot tracking and compliance |
| Logistics | 8002 | Dispatch and routing |
| Recommender | 8003 | Demand forecasting |

## Database Management

### Migrations

Alembic is used for database migrations:

```bash
# Generate a new migration
cd /workspace/seed-to-chef/services/api
poetry run alembic revision --autogenerate -m "Add users table"

# Apply migrations to the development database
docker-compose exec postgres psql -U user -d s2c -f path/to/migration.sql

# Alternatively, use Alembic directly:
poetry run alembic upgrade head
```

### Seed Data

To populate the database with initial data:

```bash
cd /workspace/seed-to-chef/services/api
python scripts/seed_database.py
```

This will create:
- 3 chefs (1 HOME in CA San Mateo, 1 HOME in CO Boulder, 1 COMMERCIAL)
- 10 dishes across different risk levels
- 6 ingredients + 3 farm batches + lots
- 5 sample orders

## Environment Variables

The `.env` file should contain:

```ini
# Database configuration
DATABASE_URL="postgresql://user:password@localhost:5432/s2c"

# Redis cache
REDIS_URL="redis://localhost:6379/0"

# Stripe Connect (for payments)
STRIPE_SECRET_KEY=""
STRIPE_CONNECT_CLIENT_ID=""
STRIPE_WEBHOOK_SECRET=""

# Messaging queue
NATS_URL="nats://localhost:4222"
REDPANDA_BROKERS="redpanda:9092"

# Object storage for uploads
MINIO_ENDPOINT="http://minio:9000"
MINIO_ACCESS_KEY=""
MINIO_SECRET_KEY=""
MINIO_BUCKET_NAME="uploads"

# Observability
OTEL_EXPORTER_OTLP_ENDPOINT="http://jaeger:4317"

# Feature flags
FEATURE_FLAGS_ENABLED=true
```

## CI/CD Pipeline

The GitHub Actions workflow in `.github/workflows/ci.yml` handles:

- Linting (TypeScript, Python)
- Type checking (mypy)
- Unit tests (pytest, Jest)
- Build verification
- Docker image building

### Manual Trigger

To manually trigger a build:
1. Go to the repository on GitHub
2. Navigate to "Actions"
3. Select the CI workflow
4. Click "Run workflow"

## Monitoring and Logging

### Prometheus + Grafana Dashboards

The monitoring stack includes:

- **Prometheus**: Metrics collection from all services
- **Grafana**: Visualization dashboards for performance monitoring

To access:
1. Open Grafana at `http://localhost:3000`
2. Login with default credentials (`admin/admin`)
3. Import the dashboard JSON files from `/infra/monitoring/dashboards/`

### Jaeger Tracing

For distributed tracing:
- Access Jaeger UI at `http://localhost:16686`
- View traces by service or operation name
- Filter by specific order IDs or lot codes

## Backup and Restore Procedures

### Database Backups

```bash
# Create a backup of the PostgreSQL database
docker-compose exec postgres pg_dump -U user s2c > backups/s2c_$(date +%Y%m%d).sql.gz

# Restore from backup
gunzip < backups/s2c_20250825.sql.gz | docker-compose exec -i postgres psql -U user -d s2c
```

### MinIO Backups

```bash
# Backup all files from MinIO
mc alias set myminio http://localhost:9000 minioadmin minioadmin
mc mirror myminio/uploads backups/minio_uploads_$(date +%Y%m%d)/ --overwrite
```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| **Database connection refused** | Check if PostgreSQL container is running: `docker-compose ps` |
| **Missing environment variables** | Verify `.env` file exists and contains required values |
| **Service not responding on port 8000** | Check Docker logs: `docker-compose logs api` |
| **Migration errors** | Run migrations manually: `poetry run alembic upgrade head` |

### Debugging Commands

```bash
# View all running containers
docker-compose ps

# Check logs for a specific service
docker-compose logs -f api

# Execute a shell in the API container
docker-compose exec api /bin/sh

# Test database connectivity
psql "postgresql://user:password@localhost:5432/s2c" -c "\dt"
```

## Performance Optimization

### Caching Strategies

- **Redis**: Used for session storage, rate limiting, and frequent query results
- **HTTP Caching**: Cache-Control headers on immutable assets (API docs, static files)
- **Database Indexing**: Optimized queries with indexes on frequently searched columns

### Load Testing

To perform load testing:

```bash
# Install locust
pip install locust

# Run a load test
locust -f scripts/load_test.py --host=http://localhost:8000
```

## Security Best Practices

1. **Environment Isolation**: Use separate `.env` files for development, staging, and production
2. **Secret Management**: Store sensitive credentials in AWS Secrets Manager or HashiCorp Vault
3. **Database Security**:
   - Regular backups
   - Read-only replicas for analytics
   - Connection pooling to prevent overload

## Development Workflow

### Feature Branch Strategy

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/new-feature main
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "Add new feature with description"
   ```

3. Push to GitHub and create a Pull Request

### Code Reviews

All pull requests require approval from at least one maintainer before merging.

## Contributing Guidelines

1. Follow the [CONTRIBUTING.md](CONTRIBUTING.md) document
2. Write unit tests for new functionality
3. Update documentation as needed
4. Ensure all linters and type checks pass

## Support and Contact

For issues or questions:
- Open a GitHub issue in the repository
- Join our Slack community (invite link on website)
- Email support@seedtochef.com


