

# Seed to Shelf - Agri Automation + Processing + Distribution

Seed to Shelf is the supply chain component of the Seed to Chef platform, handling farm automation, food processing, and distribution.

## Architecture Overview

This repository contains:

- **Backend Services** (Python FastAPI):
  - `/services/traceability`: FSMA 204 compliance and lot tracking
  - `/services/farm`: Grow planning and IoT sensor integration
  - `/services/logistics`: Dispatch, routing, and delivery providers
  - `/services/recommender`: Demand forecasting

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

