






"""
Test the traceability service endpoints.
"""

import httpx

def test_health_check():
    """Test health check endpoint."""
    with httpx.Client() as client:
        response = client.get("http://localhost:8002/health")
        print(f"Response status: {response.status_code}")
        print(f"Response JSON: {response.json()}")

if __name__ == "__main__":
    test_health_check()
    print("Health check completed!")



