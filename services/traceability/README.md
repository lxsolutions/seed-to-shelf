







# Seed to Chef Traceability Service

FSMA 204 compliant traceability system for food supply chain tracking.

## Overview

This service handles Key Data Element (KDE) tracking and lot lineage graph generation for compliance with FSMA 204 regulations. It supports:

- Compliance Trace Events (CTEs): Receive, Transform, Ship
- Lot lineage graph construction
- Backtrace queries by order ID or lot code
- JSON/CSV export for regulatory reporting

## API Endpoints

### Health Check
```bash
GET /health
```
Returns service health status.

### Record Compliance Event
```bash
POST /trace/events
Content-Type: application/json

{
  "entity_ref": "lot-12345",
  "cte_type": "Receive",      # Receive/Transform/Ship
  "data": {
    "quantity": 10,
    "location": "Kitchen A",
    "timestamp": "2025-08-25T12:00:00Z"
  }
}
```
Records a compliance trace event with KDE tracking.

### Get Order Backtrace
```bash
GET /trace/backtrace?order_id=ORDER_ID
```
Returns complete supply chain backtrace for an order including all lot transformations.

### Get Lot Information
```bash
GET /trace/lot/{lot_code}
```
Returns information about a specific lot, including parent/child relationships and order references.

## Development

### Setup
```bash
cd services/traceability
poetry install --with dev
```

### Run locally
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Test endpoints
```bash
./demo_traceability.sh
```

## Database Schema

- `compliance_events`: Stores all CTEs with KDE payloads
- `lot_lineage`: Tracks lot transformations and relationships
- `traceability_config`: Service configuration settings



