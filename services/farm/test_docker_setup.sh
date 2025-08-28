





#!/bin/bash

# Test Docker Compose setup
echo "Testing Docker Compose setup..."

# Build services
cd /workspace/seed-to-chef || exit 1

echo "Building API service..."
docker build -f services/api/Dockerfile -t s2c-api .

echo "Building Traceability service..."
docker build -f services/traceability/Dockerfile -t s2c-traceability .

# Test docker-compose
cd infra/docker || exit 1

echo "Testing docker-compose config..."
docker-compose config > /dev/null 2>&1 && echo "Docker Compose config is valid!" || (echo "Docker Compose config error!"; exit 1)

echo "All tests passed!"
exit 0



