










"""
Test complete traceability service workflow.
"""

import httpx
import time

def test_traceability_workflow():
    """Test the full traceability workflow."""
    base_url = "http://localhost:8002"

    print("=== Traceability Service Workflow Test ===")
    print()

    # Start server in background (if not already running)
    import subprocess
    import os

    def is_server_running():
        try:
            response = httpx.get(f"{base_url}/health", timeout=5.0)
            return response.status_code == 200
        except:
            return False

    if not is_server_running():
        print("Starting traceability service...")
        server_process = subprocess.Popen(
            ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"],
            cwd="/workspace/seed-to-chef/services/traceability",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        # Wait for server to start
        max_retries = 10
        for i in range(max_retries):
            if is_server_running():
                print("Service started successfully!")
                break
            time.sleep(2)
        else:
            print("Failed to start service after several attempts")
            return

    try:
        # Test health check
        print("\n1. Testing health endpoint...")
        with httpx.Client() as client:
            response = client.get(f"{base_url}/health")
            assert response.status_code == 200, f"Health check failed: {response.text}"
            print("✓ Health check passed")

        # Test recording compliance events
        print("\n2. Testing compliance event recording...")

        test_events = [
            {
                "entity_ref": "lot-12345",
                "cte_type": "Receive",
                "data": {
                    "quantity": 10,
                    "location": "Kitchen A",
                    "timestamp": "2025-08-25T12:00:00Z"
                }
            },
            {
                "entity_ref": "lot-transformed",
                "cte_type": "Transform",
                "data": {
                    "input_lots": ["lot-12345"],
                    "output_lot": "lot-transformed",
                    "process": "Chopping and mixing"
                }
            },
            {
                "entity_ref": "order-67890",
                "cte_type": "Ship",
                "data": {
                    "lot_codes": ["lot-transformed"],
                    "destination": "Consumer address",
                    "delivery_method": "Driver"
                }
            }
        ]

        for i, event_data in enumerate(test_events):
            print(f"  Recording event {i+1}: {event_data['cte_type']} ({event_data['entity_ref']})")
            with httpx.Client() as client:
                response = client.post(
                    f"{base_url}/trace/events",
                    json=event_data
                )
                assert response.status_code == 200, f"Event recording failed: {response.text}"
                print(f"    ✓ Event recorded (ID: {response.json().get('id')})")

        # Test backtrace endpoint
        print("\n3. Testing order backtrace...")
        with httpx.Client() as client:
            response = client.get(
                f"{base_url}/trace/backtrace",
                params={"order_id": "order-67890"}
            )
            assert response.status_code == 200, f"Backtrace failed: {response.text}"
            backtrace_data = response.json()
            print(f"    ✓ Backtrace retrieved for order-67890")
            print(f"       Lineage steps: {len(backtrace_data['lot_lineage'])}")

        # Test lot info endpoint
        print("\n4. Testing lot information...")
        test_lots = ["lot-12345", "lot-transformed"]
        for lot_code in test_lots:
            with httpx.Client() as client:
                response = client.get(f"{base_url}/trace/lot/{lot_code}")
                assert response.status_code == 200, f"Lot info failed: {response.text}"
                print(f"    ✓ Lot information retrieved for {lot_code}")

        # Test error handling
        print("\n5. Testing error cases...")
        with httpx.Client() as client:
            # Invalid lot code
            response = client.get(f"{base_url}/trace/lot/invalid-lot")
            assert response.status_code == 404, f"Expected 404 for invalid lot: {response.text}"
            print("    ✓ Properly handles invalid lot codes")

        print("\n=== All workflow tests passed! ===")

    finally:
        # Clean up server if we started it
        try:
            if 'server_process' in locals():
                print("\nStopping traceability service...")
                server_process.terminate()
                server_process.wait(timeout=5)
                print("Service stopped.")
        except Exception as e:
            print(f"Error stopping service: {e}")

if __name__ == "__main__":
    test_traceability_workflow()






