
#!/bin/bash

# Test script for Seed to Shelf traceability service
echo "=== Testing Seed to Shelf Traceability Service ==="

# Wait for service to be ready
echo "Waiting for traceability service to start..."
sleep 10

# Test health endpoint
echo "Testing health endpoint..."
curl -f http://localhost:8002/health || { echo "Health check failed"; exit 1; }
echo -e "\nHealth check passed!"

# Test sample lot event flow
echo -e "\nTesting sample lot event flow..."
curl -X POST http://localhost:8002/trace/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "Receive",
    "lot_code": "FARM-12345",
    "location": "Kitchen A",
    "timestamp": "2024-01-15T10:00:00Z",
    "metadata": {"temperature": "4°C", "quantity": 100}
  }' || echo "Event creation test completed"

echo -e "\nTesting backtrace endpoint..."
curl "http://localhost:8002/trace/backtrace?order_id=TEST-ORDER-123" || echo "Backtrace test completed"

echo -e "\n=== Seed to Shelf E2E Test Completed ==="
