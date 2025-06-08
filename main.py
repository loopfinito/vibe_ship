from flask import Flask, request, jsonify
from dataclasses import dataclass, asdict
from typing import Dict, Optional
import uuid

app = Flask(__name__)

@dataclass
class Ship:
    """Ship model with name, position, and destination"""
    name: str
    position_x: float
    position_y: float
    destination_x: float
    destination_y: float
    id: str = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
    
    def to_dict(self):
        return asdict(self)

# In-memory storage for ships
ships: Dict[str, Ship] = {}

@app.route('/ships', methods=['GET'])
def get_all_ships():
    """Get all ships"""
    return jsonify([ship.to_dict() for ship in ships.values()])

@app.route('/ships/<ship_id>', methods=['GET'])
def get_ship(ship_id):
    """Get a specific ship by ID"""
    ship = ships.get(ship_id)
    if not ship:
        return jsonify({'error': 'Ship not found'}), 404
    return jsonify(ship.to_dict())

@app.route('/ships', methods=['POST'])
def create_ship():
    """Create a new ship"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'position_x', 'position_y', 'destination_x', 'destination_y']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        ship = Ship(
            name=data['name'],
            position_x=float(data['position_x']),
            position_y=float(data['position_y']),
            destination_x=float(data['destination_x']),
            destination_y=float(data['destination_y'])
        )
        ships[ship.id] = ship
        return jsonify(ship.to_dict()), 201
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid data format'}), 400

@app.route('/ships/<ship_id>', methods=['PUT'])
def update_ship(ship_id):
    """Update an existing ship"""
    ship = ships.get(ship_id)
    if not ship:
        return jsonify({'error': 'Ship not found'}), 404
    
    data = request.get_json()
    
    try:
        # Update only provided fields
        if 'name' in data:
            ship.name = data['name']
        if 'position_x' in data:
            ship.position_x = float(data['position_x'])
        if 'position_y' in data:
            ship.position_y = float(data['position_y'])
        if 'destination_x' in data:
            ship.destination_x = float(data['destination_x'])
        if 'destination_y' in data:
            ship.destination_y = float(data['destination_y'])
        
        return jsonify(ship.to_dict())
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid data format'}), 400

@app.route('/ships/<ship_id>', methods=['DELETE'])
def delete_ship(ship_id):
    """Delete a ship"""
    ship = ships.get(ship_id)
    if not ship:
        return jsonify({'error': 'Ship not found'}), 404
    
    del ships[ship_id]
    return jsonify({'message': 'Ship deleted successfully'})

@app.route('/ships/<ship_id>/move', methods=['POST'])
def move_ship(ship_id):
    """Move ship to a new position"""
    ship = ships.get(ship_id)
    if not ship:
        return jsonify({'error': 'Ship not found'}), 404
    
    data = request.get_json()
    
    if 'x' not in data or 'y' not in data:
        return jsonify({'error': 'Missing x or y coordinates'}), 400
    
    try:
        ship.position_x = float(data['x'])
        ship.position_y = float(data['y'])
        return jsonify(ship.to_dict())
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid coordinate format'}), 400

@app.route('/ships/<ship_id>/destination', methods=['POST'])
def set_destination(ship_id):
    """Set a new destination for the ship"""
    ship = ships.get(ship_id)
    if not ship:
        return jsonify({'error': 'Ship not found'}), 404
    
    data = request.get_json()
    
    if 'x' not in data or 'y' not in data:
        return jsonify({'error': 'Missing x or y coordinates'}), 400
    
    try:
        ship.destination_x = float(data['x'])
        ship.destination_y = float(data['y'])
        return jsonify(ship.to_dict())
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid coordinate format'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'ships_count': len(ships)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)