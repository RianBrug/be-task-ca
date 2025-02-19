def test_create_item(client):
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "quantity": 5
    }
    
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["price"] == item_data["price"]
    assert "id" in data

def test_create_duplicate_item(client):
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "quantity": 5
    }
    
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    
    # Try to create the same item again
    response = client.post("/items/", json=item_data)
    assert response.status_code == 409

def test_get_all_items(client):
    # Create a few items
    items = [
        {
            "name": f"Item {i}",
            "description": f"Description {i}",
            "price": 10.99 + i,
            "quantity": 5
        }
        for i in range(3)
    ]
    
    for item in items:
        client.post("/items/", json=item)
    
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3 