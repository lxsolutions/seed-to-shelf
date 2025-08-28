







#!/bin/bash

# Add traceability service files to git
echo "Adding traceability service files to git..."

cd /workspace/seed-to-chef || exit 1

git add services/traceability/
git commit -m "Add FSMA 204 compliant traceability service with:
- SQLAlchemy models for compliance events, lot lineage, and config
- FastAPI endpoints: health check, event recording, backtrace, lot info
- Dockerfile with Poetry support
- Comprehensive test suite
- Seed data generation scripts"

echo "Traceability service files added to git!"





