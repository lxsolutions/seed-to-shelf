






#!/bin/bash

# Demo script for Seed to Chef Traceability Service
echo "=== Seed to Chef Traceability Service Demo ==="
echo ""

# Start the traceability service in the background
cd /workspace/seed-to-chef/services/traceability || exit 1

echo "Starting traceability service..."
python -m uvicorn main:app --host 0.0.0.0 --port 8002 > server.log 2>&1 &
SERVER_PID=$!
sleep 3
echo "Service started (PID: $SERVER_PID)"
echo ""

# Test the endpoints using curl
echo "Testing health check..."
curl -s http://localhost:8002/health | jq .
echo ""

echo "Recording a compliance event (Receive CTE)..."
curl -s -X POST http://localhost:8002/trace/events \
  -H "Content-Type: application/json" \
  -d '{
    "entity_ref": "lot-12345",
    "cte_type": "Receive",
    "data": {
      "quantity": 10,
      "location": "Kitchen A",
      "timestamp": "2025-08-25T12:00:00Z"
    }
  }' | jq .
echo ""

echo "Getting backtrace for order..."
curl -s http://localhost:8002/trace/backtrace?order_id=order-67890 | jq .
echo ""

echo "Getting lot information..."
curl -s http://localhost:8002/trace/lot/lot-12345 | jq .
echo ""

# Clean up
echo "Stopping traceability service..."
kill $SERVER_PID > /dev/null 2>&1 || true
wait $SERVER_PID 2>/dev/null || true

echo ""
echo "Demo completed successfully!"




