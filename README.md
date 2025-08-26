

# Seed to Shelf - Agri Automation + Processing + Distribution

Seed to Shelf is the supply chain component of the Seed to Chef platform, handling farm automation, food processing, distribution, and shared API contracts.

## Architecture Overview

This repository contains:

- **Backend Services** (Python FastAPI):
  - `/services/traceability`: FSMA 204 compliance and lot tracking
  - `/services/farm`: Grow planning and IoT sensor integration
  - `/services/logistics`: Dispatch, routing, and delivery providers
  - `/services/recommender`: Demand forecasting

- **Shared Contracts**:
  - `/contracts/events/asyncapi.yaml`: Event-driven contract specification
  - `/contracts/schemas/json/...`: JSON schema definitions for shared models
  - `/contracts/typescript/index.ts`: Zod type exports (TypeScript)
  - `/contracts/python/pydantic_models.py`: Pydantic model exports (Python)

## Getting Started

### Prerequisites

- Python 3.11+
- Docker
- Poetry (Python dependency management)

### Local Development

```bash
# Install dependencies
poetry install

# Start the full stack with docker-compose
docker-compose up --build
```

## Project Structure

```
.
├── contracts/           # Shared API & event schemas (published to npm/PyPI)
│   ├── events/          # AsyncAPI specifications
│   ├── schemas/json/    # JSON schema definitions
│   ├── typescript/      # Zod type exports
│   └── python/          # Pydantic model exports
├── services/            # Backend microservices
│   ├── traceability/    # Traceability and compliance
│   ├── farm/            # Farming operations
│   ├── logistics/       # Logistics and delivery
│   └── recommender/     # Recommendation engine
└── infra/               # Infrastructure as code
    └── docker/          # Docker-compose setup
```

## Contributing

Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the MIT License.

