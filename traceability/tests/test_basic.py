

"""
Basic tests for traceability service.
"""

import pytest
from fastapi.testclient import TestClient

def test_health():
    """Test health endpoint."""
    from ..main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])

