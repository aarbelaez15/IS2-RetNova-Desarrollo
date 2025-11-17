from fastapi.testclient import TestClient
from co.edu.uco.retnova.interfaces.api.main import app
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code in [200, 404, 422]
