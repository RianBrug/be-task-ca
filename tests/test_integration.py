def test_full_shopping_flow(client):
    # Create a user
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "secret123",
        "shipping_address": "123 Main St"
    }
    user_response = client.post("/users/", json=user_data)
    assert user_response.status_code == 200
    user_id = user_response.json()["id"]
    
    # Create multiple items
    items = [
        {
            "name": f"Item {i}",
            "description": f"Description {i}",
            "price": 10.99 + i,
            "quantity": 5
        }
        for i in range(3)
    ]
    
    item_ids = []
    for item in items:
        response = client.post("/items/", json=item)
        assert response.status_code == 200
        item_ids.append(response.json()["id"])
    
    # Add items to cart
    for item_id in item_ids:
        cart_data = {
            "item_id": item_id,
            "quantity": 1
        }
        response = client.post(f"/users/{user_id}/cart", json=cart_data)
        assert response.status_code == 200
    
    # Check cart contents
    cart_response = client.get(f"/users/{user_id}/cart")
    assert cart_response.status_code == 200
    cart_items = cart_response.json()["items"]
    assert len(cart_items) == 3 