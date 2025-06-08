import pytest
import json
from main import app, ships, Ship

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_ship():
    """Create a sample ship for testing"""
    ship = Ship(
        name="Test Ship",
        position_x=10.0,
        position_y=20.0,
        destination_x=30.0,
        destination_y=40.0
    )
    ships[ship.id] = ship
    yield ship
    # Cleanup
    ships.clear()

class TestSetDestination:
    def test_set_destination_success(self, client, sample_ship):
        """Test successfully setting a new destination"""
        new_destination = {"x": 100.0, "y": 200.0}
        
        response = client.post(
            f'/ships/{sample_ship.id}/destination',
            data=json.dumps(new_destination),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['destination_x'] == 100.0
        assert data['destination_y'] == 200.0
        assert data['id'] == sample_ship.id
        
        # Verify the ship was actually updated
        assert ships[sample_ship.id].destination_x == 100.0
        assert ships[sample_ship.id].destination_y == 200.0

    def test_set_destination_ship_not_found(self, client):
        """Test setting destination for non-existent ship"""
        destination = {"x": 100.0, "y": 200.0}
        
        response = client.post(
            '/ships/non-existent-id/destination',
            data=json.dumps(destination),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Ship not found'

    def test_set_destination_missing_x_coordinate(self, client, sample_ship):
        """Test setting destination with missing x coordinate"""
        incomplete_destination = {"y": 200.0}
        
        response = client.post(
            f'/ships/{sample_ship.id}/destination',
            data=json.dumps(incomplete_destination),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Missing x or y coordinates'

    def test_set_destination_missing_y_coordinate(self, client, sample_ship):
        """Test setting destination with missing y coordinate"""
        incomplete_destination = {"x": 100.0}
        
        response = client.post(
            f'/ships/{sample_ship.id}/destination',
            data=json.dumps(incomplete_destination),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Missing x or y coordinates'

    def test_set_destination_invalid_x_format(self, client, sample_ship):
        """Test setting destination with invalid x coordinate format"""
        invalid_destination = {"x": "invalid", "y": 200.0}
        
        response = client.post(
            f'/ships/{sample_ship.id}/destination',
            data=json.dumps(invalid_destination),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Invalid coordinate format'

    def test_set_destination_invalid_y_format(self, client, sample_ship):
        """Test setting destination with invalid y coordinate format"""
        invalid_destination = {"x": 100.0, "y": "invalid"}
        
        response = client.post(
            f'/ships/{sample_ship.id}/destination',
            data=json.dumps(invalid_destination),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Invalid coordinate format'

    def test_set_destination_string_numbers(self, client, sample_ship):
        """Test setting destination with string numbers (should work)"""
        string_destination = {"x": "150.5", "y": "250.5"}
        
        response = client.post(
            f'/ships/{sample_ship.id}/destination',
            data=json.dumps(string_destination),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['destination_x'] == 150.5
        assert data['destination_y'] == 250.5

    def test_set_destination_negative_coordinates(self, client, sample_ship):
        """Test setting destination with negative coordinates"""
        negative_destination = {"x": -50.0, "y": -75.0}
        
        response = client.post(
            f'/ships/{sample_ship.id}/destination',
            data=json.dumps(negative_destination),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['destination_x'] == -50.0
        assert data['destination_y'] == -75.0

    def test_set_destination_zero_coordinates(self, client, sample_ship):
        """Test setting destination with zero coordinates"""
        zero_destination = {"x": 0.0, "y": 0.0}
        
        response = client.post(
            f'/ships/{sample_ship.id}/destination',
            data=json.dumps(zero_destination),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['destination_x'] == 0.0
        assert data['destination_y'] == 0.0