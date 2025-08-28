
# Seed to Chef (S2C) - Vertically Integrated Food Platform

A vertically-integrated platform that grows ingredients via automated farms, routes them to distributed chefs, and delivers finished food via pickup/driver/drone.

## Architecture Overview

This monorepo contains:

- **Frontend Applications**:
  - `/apps/web`: Next.js 14 consumer web application
  - `/apps/consumer`: React Native Expo mobile app for consumers
  - `/apps/chef`: React Native Expo mobile app for chefs
  - `/apps/admin`: Next.js 14 admin dashboard

- **Backend Services** (Python FastAPI):
  - `/services/api`: Core API with authentication, orders, dishes, etc.
  - `/services/traceability`: FSMA 204 compliance and lot tracking
  - `/services/logistics`: Dispatch, routing, and delivery providers
  - `/services/recommender`: Demand forecasting and chef matching
  - `/services/farm`: Grow planning and IoT sensor integration

- **Shared Packages**:
  - `/packages/ui`: Shared React components with Tailwind + Radix
  - `/packages/types`: OpenAPI types + zod schemas

- **Infrastructure**:
  - `/infra/docker`: Docker-compose setup for local development
  - `/infra/k8s`: Helm charts and kustomize overlays for Kubernetes deployment

## Getting Started

### Prerequisites

- Node.js (v18+)
- Python 3.11+
- Docker
- pnpm (JavaScript package manager)
- Poetry (Python dependency management)

### Local Development

```bash
# Install dependencies
pnpm install
poetry install

# Start the full stack with docker-compose
docker-compose up --build
```

## Project Structure

```
.
├── apps/                # Frontend applications
│   ├── web/             # Consumer web app (Next.js)
│   ├── consumer/        # Consumer mobile app (React Native Expo)
│   ├── chef/            # Chef mobile app (React Native Expo)
│   └── admin/           # Admin dashboard (Next.js)
├── services/            # Backend microservices
│   ├── api/             # Core API service
│   ├── traceability/    # Traceability and compliance
│   ├── logistics/       # Logistics and delivery
│   ├── recommender/     # Recommendation engine
│   └── farm/            # Farming operations
├── packages/            # Shared components and types
│   ├── ui/              # UI components
│   └── types/           # Type definitions
├── infra/               # Infrastructure as code
│   ├── docker/          # Docker-compose setup
│   └── k8s/             # Kubernetes manifests
└── docs/                # Documentation
```

## Contributing

Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for development guidelines.

## License

This project is licensed under the MIT License.
