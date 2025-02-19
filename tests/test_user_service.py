def test_create_user(client):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "secret123",
        "shipping_address": "123 Main St"
    }
    
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert "id" in data

def test_create_duplicate_user(client):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "secret123",
        "shipping_address": "123 Main St"
    }
    
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    
    # Try to create the same user again
    response = client.post("/users/", json=user_data)
    assert response.status_code == 409

def test_add_item_to_cart(client):
    # First create a user
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "secret123",
        "shipping_address": "123 Main St"
    }
    user_response = client.post("/users/", json=user_data)
    user_id = user_response.json()["id"]
    
    # Create an item
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "quantity": 5
    }
    item_response = client.post("/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    # Add item to cart
    cart_data = {
        "item_id": item_id,
        "quantity": 2
    }
    response = client.post(f"/users/{user_id}/cart", json=cart_data)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1 