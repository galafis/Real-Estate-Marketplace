#!/usr/bin/env python3
"""
Real Estate Marketplace API
Author: Gabriel Demetrios Lafis; Contributions: Comet Assistant (review, docs, UX, integration)

A compact Flask backend exposing property listings, search, favorites, contact, and stats.
This demo uses in-memory storage for simplicity; swap with SQLite for persistence.
"""
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import uuid
import os

app = Flask(__name__)
app.config.update(SECRET_KEY = os.getenv("SECRET_KEY"))

# ----------------------------------------------------------------------------
# In-memory demo storage (replace with a proper DB in production)
# ----------------------------------------------------------------------------
properties = []
users = []
favorites = []


def initialize_sample_data():
    """Populate initial demo data to make the app usable out of the box."""
    global properties, users

    if not properties:
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

    if not users:
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


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------
@app.route('/')
def index():
    """Serve the single-page interface."""
    return render_template('index.html')


@app.route('/api/properties', methods=['GET'])
def get_properties():
    """Return properties filtered by optional query params.
    Query: min_price, max_price, type, bedrooms, city
    """
    filtered = list(properties)

    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    if min_price is not None:
        filtered = [p for p in filtered if p['price'] >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if p['price'] <= max_price]

    prop_type = request.args.get('type')
    if prop_type:
        filtered = [p for p in filtered if p['type'] == prop_type]

    bedrooms = request.args.get('bedrooms', type=int)
    if bedrooms is not None:
        filtered = [p for p in filtered if p['bedrooms'] >= bedrooms]

    city = request.args.get('city')
    if city:
        filtered = [p for p in filtered if city.lower() in p['city'].lower()]

    return jsonify(filtered)


@app.route('/api/properties/<int:property_id>', methods=['GET'])
def get_property(property_id: int):
    """Return a single property by ID."""
    prop = next((p for p in properties if p['id'] == property_id), None)
    return (jsonify(prop), 200) if prop else (jsonify({'error': 'Property not found'}), 404)


@app.route('/api/properties', methods=['POST'])
def create_property():
    """Create a new property. Minimal validation for demo purposes."""
    data = request.get_json(silent=True) or {}
    required = ['title', 'price', 'type', 'bedrooms', 'bathrooms', 'city']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': 'Missing fields', 'fields': missing}), 400

    new_id = max([p['id'] for p in properties], default=0) + 1
    new_property = {
        'id': new_id,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'price': int(data.get('price')),
        'type': data.get('type'),
        'bedrooms': int(data.get('bedrooms')),
        'bathrooms': int(data.get('bathrooms')),
        'area': int(data.get('area', 0)),
        'address': data.get('address', ''),
        'city': data.get('city'),
        'state': data.get('state', ''),
        'zip_code': data.get('zip_code', ''),
        'agent': data.get('agent', ''),
        'agent_phone': data.get('agent_phone', ''),
        'agent_email': data.get('agent_email', ''),
        'images': data.get('images', []),
        'features': data.get('features', []),
        'status': data.get('status', 'available'),
        'created_at': datetime.now().isoformat(),
    }
    properties.append(new_property)
    return jsonify(new_property), 201


@app.route('/api/search', methods=['GET'])
def search_properties():
    """Simple text search across title, description, city, and address."""
    query = (request.args.get('q') or '').strip().lower()
    if not query:
        return jsonify([])

    results = [
        p for p in properties
        if query in p['title'].lower()
        or query in p['description'].lower()
        or query in p['city'].lower()
        or query in p['address'].lower()
    ]
    return jsonify(results)


@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Return favorite properties for a given user_id."""
    user_id = request.args.get('user_id', type=int)
    if not user_id:
        return jsonify([])

    fav_ids = [f['property_id'] for f in favorites if f['user_id'] == user_id]
    fav_props = [p for p in properties if p['id'] in fav_ids]
    return jsonify(fav_props)


@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    """Add a property to favorites if not already present."""
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id')
    property_id = data.get('property_id')
    if not (user_id and property_id):
        return jsonify({'error': 'user_id and property_id are required'}), 400

    exists = next((f for f in favorites if f['user_id'] == user_id and f['property_id'] == property_id), None)
    if exists:
        return jsonify({'message': 'Already in favorites'}), 409

    favorites.append({
        'id': max([f['id'] for f in favorites], default=0) + 1,
        'user_id': int(user_id),
        'property_id': int(property_id),
        'created_at': datetime.now().isoformat(),
    })
    return jsonify({'message': 'Added to favorites'}), 201


@app.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
def remove_favorite(favorite_id: int):
    """Remove favorite by favorite_id."""
    global favorites
    before = len(favorites)
    favorites = [f for f in favorites if f['id'] != favorite_id]
    removed = before != len(favorites)
    return jsonify({'removed': removed})


@app.route('/api/contact', methods=['POST'])
def contact_agent():
    """Accept a contact request; in production, send email/notification."""
    data = request.get_json(silent=True) or {}
    contact_request = {
        'id': str(uuid.uuid4()),
        'property_id': data.get('property_id'),
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'message': data.get('message'),
        'created_at': datetime.now().isoformat(),
    }
    return jsonify({'message': 'Contact request received', 'request': contact_request}), 202


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Aggregate basic statistics for dashboard visualization."""
    total = len(properties)
    available = sum(1 for p in properties if p['status'] == 'available')
    avg_price = (sum(p['price'] for p in properties) / total) if total else 0

    type_counts = {}
    for p in properties:
        t = p['type']
        type_counts[t] = type_counts.get(t, 0) + 1

    price_ranges = {
        'under_300k': sum(1 for p in properties if p['price'] < 300_000),
        '300k_600k': sum(1 for p in properties if 300_000 <= p['price'] < 600_000),
        '600k_1m': sum(1 for p in properties if 600_000 <= p['price'] < 1_000_000),
        'over_1m': sum(1 for p in properties if p['price'] >= 1_000_000),
    }

    return jsonify({
        'total_properties': total,
        'available_properties': available,
        'average_price': avg_price,
        'type_distribution': type_counts,
        'price_ranges': price_ranges,
    })


if __name__ == '__main__':
    # Development server settings per README
    app.run(debug=True, host='0.0.0.0', port=5000)