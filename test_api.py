import pytest
from fastapi.testclient import TestClient
from rest_api import app

client = TestClient(app)

# Тест для GET /nodes
def test_read_all_nodes():
    response = client.get("/nodes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Тест для GET /node/{node_id}
def test_read_node_not_found():
    response = client.get("/node/999")
    assert response.status_code == 404

# Тест для POST /nodes
def test_create_node():
    response = client.post(
        "/nodes",
        headers={"Authorization": "Bearer test_token"},
        json={"id": 1, "label": "Test Node"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Node created successfully"

# Тест для DELETE /nodes/{node_id}
def test_delete_node():
    response = client.delete(
        "/nodes/1",
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Node deleted successfully"

# Тест для GET /graph-segment
def test_read_graph_segment():
    response = client.get("/graph-segment")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
