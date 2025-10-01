
import pytest
from real_estate_marketplace.src.app import app, properties, users, favorites

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data

def test_get_properties(client):
    response = client.get('/api/properties')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_property_by_id(client):
    # Assuming there's at least one property
    if properties:
        prop_id = properties[0]['id']
        response = client.get(f'/api/properties/{prop_id}')
        assert response.status_code == 200
        assert response.json['id'] == prop_id
    else:
        # Handle case where no properties exist (e.g., if initialize_sample_data() is not called)
        response = client.get('/api/properties/999') # Non-existent ID
        assert response.status_code == 404

def test_create_property(client):
    new_property_data = {
        'title': 'New Test House',
        'price': 300000,
        'type': 'house',
        'bedrooms': 3,
        'bathrooms': 2,
        'city': 'Testville'
    }
    response = client.post('/api/properties', json=new_property_data)
    assert response.status_code == 201
    assert response.json['title'] == 'New Test House'

def test_create_property_missing_fields(client):
    new_property_data = {
        'title': 'Incomplete Property',
        'price': 100000
    }
    response = client.post('/api/properties', json=new_property_data)
    assert response.status_code == 400
    assert 'Missing fields' in response.json['error']

def test_search_properties(client):
    response = client.get('/api/search?q=apartment')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_add_favorite(client):
    # Ensure there's a user and a property to favorite
    if users and properties:
        user_id = users[0]['id']
        property_id = properties[0]['id']
        response = client.post('/api/favorites', json={'user_id': user_id, 'property_id': property_id})
        assert response.status_code in [201, 409] # 201 for created, 409 for already exists
    else:
        # If no users or properties, this test might need to be skipped or data initialized
        pass

def test_contact_agent(client):
    contact_data = {
        'property_id': 1,
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '123-456-7890',
        'message': 'I am interested in this property.'
    }
    response = client.post('/api/contact', json=contact_data)
    assert response.status_code == 202
    assert 'Contact request received' in response.json['message']

def test_get_stats(client):
    response = client.get('/api/stats')
    assert response.status_code == 200
    assert 'total_properties' in response.json
    assert 'average_price' in response.json


