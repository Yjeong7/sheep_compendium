# Import TestClient to simulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance from the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON matches the expected data
    assert response.json() == {
        # Expected JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }
def test_add_sheep():
    new_sheep={
        "id":7,
        "name": "Apple",
        "breed": "Gotland",
        "sex": "ewe"
    }

    response = client.post("/sheep/", json=new_sheep)
    assert response.status_code == 201
    assert response.json() == new_sheep

    get_resp = client.get("/sheep/7")
    assert get_resp.status_code == 200
    assert get_resp.json() == new_sheep

def test_delete_sheep():
    client.post("/sheep/3", json={"id": 3, "name": "Cherry", "breed": "Suffolk", "sex": "ewe"})
    response = client.delete("/sheep/3")
    assert response.status_code == 204
    check = client.get("/sheep/3")
    assert check.status_code == 404

def test_update_sheep():
    client.post("/sheep/2", json={"id": 2, "name": "Berry", "breed": "Merino", "sex": "ram"})
    updated_sheep = {"id": 999, "name": "Berry Jr.", "breed": "Merino", "sex": "ram"}
    response = client.put("/sheep/2", json=updated_sheep)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["name"] == "Berry Jr."

def test_read_all_sheep():
    client.post("/sheep/10", json={"id": 10, "name": "Daisy", "breed": "Karakul", "sex": "ewe"})
    client.post("/sheep/11", json={"id": 11, "name": "Eddie", "breed": "Dorper", "sex": "ram"})
    response = client.get("/sheep/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(s["name"] == "Daisy" for s in data)
    assert any(s["name"] == "Eddie" for s in data)

