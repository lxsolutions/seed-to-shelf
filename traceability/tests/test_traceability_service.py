

"""
Comprehensive pytest suite for the traceability service.
Tests all endpoints with valid and invalid inputs, including proper validation.
"""

import pytest

# Import our application and models
from ..main import app
from ..models import ComplianceEventCreate, ReceiveCTEData  # Import specific models we need

# Create a test client for FastAPI
import sys
sys.path.append('.venv/lib/python3.12/site-packages')
from fastapi.testclient import TestClient
client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.parametrize("cte_type,data", [
    # Valid Receive CTE
    ("Receive", {
        "timestamp": "2025-08-25T12:00:00Z",
        "quantity": 10.5,
        "location": "Kitchen A"
    }),
    # Valid Transform CTE
    ("Transform", {
        "timestamp": "2025-08-26T14:30:00Z",
        "input_lots": ["lot-123", "lot-456"],
        "output_lot": "lot-transformed",
        "process_description": "Chopping vegetables"
    }),
    # Valid Ship CTE
    ("Ship", {
        "timestamp": "2025-08-27T10:15:00Z",
        "quantity_shipped": 8.2,
        "destination_location": "Consumer home",
        "carrier": "Driver"
    })
])
def test_valid_trace_events(cte_type, data):
    """Test recording valid compliance events."""
    payload = {
        "entity_ref": f"lot-{cte_type.lower()}-test",
        "cte_type": cte_type,
        "data": data
    }

    response = client.post("/trace/events", json=payload)
    assert response.status_code == 200, f"Failed for {cte_type}: {response.text}"
    assert "id" in response.json()

@pytest.mark.parametrize("invalid_payload,expected_status", [
    # Missing required fields
    ({}, 422),
    ({"entity_ref": "lot-123"}, 422),
    ({"cte_type": "Receive"}, 422),
    ({"data": {"quantity": 5}}, 422),

    # Invalid cte_type
    ({"entity_ref": "lot-123", "cte_type": "InvalidType", "data": {}}, 422),

    # Missing timestamp in data
    ({"entity_ref": "lot-123", "cte_type": "Receive", "data": {"quantity": 5}}, 422),

    # Invalid Receive CTE - missing quantity
    ({"entity_ref": "lot-123", "cte_type": "Receive", "data": {"timestamp": "2025-08-25T12:00:00Z"}}, 422),

    # Invalid Transform CTE - missing input_lots
    ({"entity_ref": "lot-123", "cte_type": "Transform", "data": {"timestamp": "2025-08-25T12:00:00Z"}}, 422),

    # Invalid Ship CTE - missing quantity_shipped
    ({"entity_ref": "lot-123", "cte_type": "Ship", "data": {"timestamp": "2025-08-25T12:00:00Z"}}, 422),
])
def test_invalid_trace_events(invalid_payload, expected_status):
    """Test recording invalid compliance events."""
    response = client.post("/trace/events", json=invalid_payload)
    assert response.status_code == expected_status

@pytest.mark.parametrize("order_id", [
    "order-12345",
    "order-67890",
    "test-order"
])
def test_backtrace_endpoint(order_id):
    """Test backtrace endpoint with various order IDs."""
    response = client.get("/trace/backtrace", params={"order_id": order_id})
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert isinstance(data["lot_lineage"], list)
    assert len(data["lot_lineage"]) > 0

@pytest.mark.parametrize("lot_code,expected_status", [
    ("lot-12345", 200),
    ("batch-xyz", 200),
    ("test-lot", 200),

    # Error cases
    ("invalid-lot", 404),
    ("error-test", 404)
])
def test_lot_info_endpoint(lot_code, expected_status):
    """Test lot info endpoint with valid and invalid lot codes."""
    response = client.get(f"/trace/lot/{lot_code}")
    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.json()
        assert "lot_code" in data
        assert isinstance(data["parent_lots"], list)
        assert isinstance(data["child_lots"], list)
        assert isinstance(data["order_references"], list)

def test_model_validation():
    """Test Pydantic model validation."""
    # Test valid Receive CTE
    receive_event = models.ComplianceEventCreate(
        entity_ref="lot-123",
        cte_type="Receive",
        data=models.ReceiveCTEData(
            timestamp="2025-08-25T12:00:00Z",
            quantity=10.5,
            location="Kitchen A"
        )
    )

    assert receive_event.entity_ref == "lot-123"
    assert isinstance(receive_event.data, models.ReceiveCTEData)
    assert receive_event.data.quantity == 10.5

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])

