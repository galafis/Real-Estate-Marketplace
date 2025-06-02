#!/usr/bin/env python3
"""
Real Estate Marketplace
Complete real estate platform with property listings, search, and user management.
Built with Flask, SQLite, and modern web technologies.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import json
import uuid

app = Flask(__name__)
app.secret_key = 'real_estate_secret_2024'

# In-memory storage for demo
properties = []
users = []
favorites = []

# Initialize sample data
def initialize_sample_data():
    global properties, users
    
    # Sample properties
    properties.extend([
        {
            'id': 1,
            'title': 'Modern Downtown Apartment',
            'description': 'Luxury 2-bedroom apartment in the heart of downtown with stunning city views',
            'price': 450000,
            'type': 'apartment',
            'bedrooms': 2,
            'bathrooms': 2,
            'area': 1200,
            'address': '123 Main St, Downtown',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'agent': 'Sarah Johnson',
            'agent_phone': '+1-555-0123',
            'agent_email': 'sarah@realestate.com',
            'images': ['/static/images/apt1.jpg', '/static/images/apt1_2.jpg'],
            'features': ['Parking', 'Gym', 'Pool', 'Balcony'],
            'status': 'available',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 2,
            'title': 'Suburban Family House',
            'description': 'Beautiful 4-bedroom house perfect for families with large backyard',
            'price': 650000,
            'type': 'house',
            'bedrooms': 4,
            'bathrooms': 3,
            'area': 2500,
            'address': '456 Oak Avenue',
            'city': 'Suburbia',
            'state': 'CA',
            'zip_code': '90210',
            'agent': 'Mike Chen',
            'agent_phone': '+1-555-0456',
            'agent_email': 'mike@realestate.com',
            'images': ['/static/images/house1.jpg'],
            'features': ['Garden', 'Garage', 'Fireplace', 'Deck'],
            'status': 'available',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 3,
            'title': 'Luxury Penthouse',
            'description': 'Exclusive penthouse with panoramic views and premium amenities',
            'price': 1200000,
            'type': 'penthouse',
            'bedrooms': 3,
            'bathrooms': 3,
            'area': 2000,
            'address': '789 Sky Tower',
            'city': 'Manhattan',
            'state': 'NY',
            'zip_code': '10002',
            'agent': 'Emily Davis',
            'agent_phone': '+1-555-0789',
            'agent_email': 'emily@realestate.com',
            'images': ['/static/images/penthouse1.jpg'],
            'features': ['Concierge', 'Rooftop', 'Wine Cellar', 'Smart Home'],
            'status': 'available',
            'created_at': datetime.now().isoformat()
        }
    ])
    
    # Sample users
    users.extend([
        {
            'id': 1,
            'username': 'john_buyer',
            'email': 'john@email.com',
            'name': 'John Smith',
            'phone': '+1-555-1234',
            'type': 'buyer',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': 2,
            'username': 'agent_sarah',
            'email': 'sarah@realestate.com',
            'name': 'Sarah Johnson',
            'phone': '+1-555-0123',
            'type': 'agent',
            'created_at': datetime.now().isoformat()
        }
    ])

initialize_sample_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/properties', methods=['GET'])
def get_properties():
    # Filter properties based on query parameters
    filtered_properties = properties.copy()
    
    # Price range filter
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    if min_price:
        filtered_properties = [p for p in filtered_properties if p['price'] >= min_price]
    if max_price:
        filtered_properties = [p for p in filtered_properties if p['price'] <= max_price]
    
    # Property type filter
    property_type = request.args.get('type')
    if property_type:
        filtered_properties = [p for p in filtered_properties if p['type'] == property_type]
    
    # Bedrooms filter
    bedrooms = request.args.get('bedrooms', type=int)
    if bedrooms:
        filtered_properties = [p for p in filtered_properties if p['bedrooms'] >= bedrooms]
    
    # City filter
    city = request.args.get('city')
    if city:
        filtered_properties = [p for p in filtered_properties if city.lower() in p['city'].lower()]
    
    return jsonify(filtered_properties)

@app.route('/api/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    property_data = next((p for p in properties if p['id'] == property_id), None)
    if property_data:
        return jsonify(property_data)
    return jsonify({'error': 'Property not found'}), 404

@app.route('/api/properties', methods=['POST'])
def create_property():
    data = request.get_json()
    new_property = {
        'id': len(properties) + 1,
        'title': data.get('title'),
        'description': data.get('description'),
        'price': data.get('price'),
        'type': data.get('type'),
        'bedrooms': data.get('bedrooms'),
        'bathrooms': data.get('bathrooms'),
        'area': data.get('area'),
        'address': data.get('address'),
        'city': data.get('city'),
        'state': data.get('state'),
        'zip_code': data.get('zip_code'),
        'agent': data.get('agent'),
        'agent_phone': data.get('agent_phone'),
        'agent_email': data.get('agent_email'),
        'images': data.get('images', []),
        'features': data.get('features', []),
        'status': 'available',
        'created_at': datetime.now().isoformat()
    }
    properties.append(new_property)
    return jsonify(new_property), 201

@app.route('/api/search', methods=['GET'])
def search_properties():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    results = []
    for prop in properties:
        if (query in prop['title'].lower() or 
            query in prop['description'].lower() or 
            query in prop['city'].lower() or 
            query in prop['address'].lower()):
            results.append(prop)
    
    return jsonify(results)

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify([])
    
    user_favorites = [f['property_id'] for f in favorites if f['user_id'] == user_id]
    favorite_properties = [p for p in properties if p['id'] in user_favorites]
    return jsonify(favorite_properties)

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    user_id = data.get('user_id')
    property_id = data.get('property_id')
    
    # Check if already favorited
    existing = next((f for f in favorites if f['user_id'] == user_id and f['property_id'] == property_id), None)
    if existing:
        return jsonify({'message': 'Already in favorites'}), 400
    
    new_favorite = {
        'id': len(favorites) + 1,
        'user_id': user_id,
        'property_id': property_id,
        'created_at': datetime.now().isoformat()
    }
    favorites.append(new_favorite)
    return jsonify(new_favorite), 201

@app.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
def remove_favorite(favorite_id):
    global favorites
    favorites = [f for f in favorites if f['id'] != favorite_id]
    return jsonify({'message': 'Favorite removed'})

@app.route('/api/contact', methods=['POST'])
def contact_agent():
    data = request.get_json()
    # In a real app, this would send an email or notification
    contact_request = {
        'id': str(uuid.uuid4()),
        'property_id': data.get('property_id'),
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'message': data.get('message'),
        'created_at': datetime.now().isoformat()
    }
    return jsonify({'message': 'Contact request sent successfully', 'request': contact_request})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total_properties = len(properties)
    available_properties = len([p for p in properties if p['status'] == 'available'])
    avg_price = sum(p['price'] for p in properties) / len(properties) if properties else 0
    
    # Property types distribution
    type_counts = {}
    for prop in properties:
        prop_type = prop['type']
        type_counts[prop_type] = type_counts.get(prop_type, 0) + 1
    
    # Price ranges
    price_ranges = {
        'under_300k': len([p for p in properties if p['price'] < 300000]),
        '300k_600k': len([p for p in properties if 300000 <= p['price'] < 600000]),
        '600k_1m': len([p for p in properties if 600000 <= p['price'] < 1000000]),
        'over_1m': len([p for p in properties if p['price'] >= 1000000])
    }
    
    return jsonify({
        'total_properties': total_properties,
        'available_properties': available_properties,
        'average_price': avg_price,
        'type_distribution': type_counts,
        'price_ranges': price_ranges
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

