import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
import pytest
from app import app
from inventory import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory.clear()
    inventory.extend([
        {
            "id": 1,
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "category": "Plant Based Milk",
            "ingredients_text": "Filtered water, almonds",
            "barcode": "123456789",
            "quantity": 20,
            "price": 4.99
        }
    ])

def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["product_name"] == "Organic Almond Milk"



def test_get_single_inventory(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1

def test_get_missing_inventory(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Inventory item not found"

def test_create_inventory(client):
    new_item = {
        "product_name": "Apple Juice",
        "brands": "Tree Top",
        "category": "Drink",
        "ingredients_text": "Apple juice",
        "barcode": "555555",
        "quantity": 10,
        "price": 3.99
    }

    response = client.post(
        "/inventory",
        json=new_item
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Apple Juice"

def test_update_inventory(client):
    response = client.patch(
        "/inventory/1",
        json={
            "quantity": 50,
            "price": 5.99
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["quantity"] == 50
    assert data["price"] == 5.99

def test_delete_inventory(client):
    response = client.delete(
        "/inventory/1"
    )
    assert response.status_code == 200
    assert len(inventory) == 0