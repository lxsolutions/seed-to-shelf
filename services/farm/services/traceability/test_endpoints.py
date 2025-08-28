







"""
Test all traceability service endpoints.
"""

import httpx
from pprint import pprint

def test_all_endpoints():
    """Test all endpoints of the traceability service."""
    base_url = "http://localhost:8002"

    # Test health check
    print("Testing /health endpoint...")
    with httpx.Client() as client:
        response = client.get(f"{base_url}/health")
        print(f"Health status: {response.status_code}")
        pprint(response.json())
        assert response.status_code == 200

    # Test record_trace_event
    print("\nTesting /trace/events endpoint...")
    with httpx.Client() as client:
        event_data = {
            "entity_ref": "lot-12345",
            "cte_type": "Receive",
            "data": {
                "quantity": 10,
                "location": "Kitchen A",
                "timestamp": "2025-08-25T12:00:00Z"
            }
        }

        response = client.post(f"{base_url}/trace/events", json=event_data)
        print(f"Record event status: {response.status_code}")
        pprint(response.json())
        assert response.status_code == 200

    # Test backtrace
    print("\nTesting /trace/backtrace endpoint...")
    with httpx.Client() as client:
        order_id = "order-67890"
        response = client.get(f"{base_url}/trace/backtrace", params={"order_id": order_id})
        print(f"Backtrace status: {response.status_code}")
        pprint(response.json())
        assert response.status_code == 200

    # Test lot info
    print("\nTesting /trace/lot/{lot_code} endpoint...")
    with httpx.Client() as client:
        lot_code = "lot-12345"
        response = client.get(f"{base_url}/trace/lot/{lot_code}")
        print(f"Lot info status: {response.status_code}")
        pprint(response.json())
        assert response.status_code == 200

    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    test_all_endpoints()




