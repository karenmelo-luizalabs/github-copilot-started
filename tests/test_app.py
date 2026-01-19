import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

def test_signup_and_unregister():
    # Inscreve um novo participante
    email = "testuser@mergington.edu"
    activity = "Soccer Team"
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert f"Signed up {email}" in signup.json()["message"]

    # Remove o participante
    unregister = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister.status_code == 200
    assert f"{email} removido" in unregister.json()["message"]

    # Tenta remover novamente (deve dar erro)
    unregister2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister2.status_code == 404
    assert "Participant not found" in unregister2.json()["detail"]
