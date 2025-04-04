import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_verify_claim():
    response = client.post("/verify", json={"text": "The president claims that the economy is growing.", "language": "en"})
    assert response.status_code == 200
    data = response.json()
    assert data["is_claim"] == True
    assert "fact_check" in data
    assert "similar_claims" in data

if __name__ == "__main__":
    pytest.main()