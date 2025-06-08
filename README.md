# Ship Management API & CLI

A Flask-based REST API for managing ships with their positions and destinations, plus a command-line interface for easy interaction.

## Features

- Create, read, update, and delete ships
- Track ship positions (x, y coordinates)
- Set and update ship destinations
- Move ships to new positions
- RESTful API with JSON responses
- Command-line interface for easy interaction

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the Flask server:
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

- `GET /ships` - List all ships
- `GET /ships/<id>` - Get specific ship details
- `POST /ships` - Create a new ship
- `PUT /ships/<id>` - Update ship details
- `DELETE /ships/<id>` - Delete a ship
- `POST /ships/<id>/move` - Move ship to new position
- `POST /ships/<id>/destination` - Set ship destination
- `GET /health` - Health check

## CLI Usage

The CLI provides an easy way to interact with the API from the command line.

### Basic Commands

List all ships:
```bash
python cli.py list
```

Create a new ship:
```bash
python cli.py create "Titanic" 0.0 0.0 100.0 100.0
```

Get ship details:
```bash
python cli.py get <ship_id>
```

Update ship name:
```bash
python cli.py update <ship_id> --name "New Name"
```

Move ship to new position:
```bash
python cli.py move <ship_id> 50.0 75.0
```

Set ship destination:
```bash
python cli.py destination <ship_id> 200.0 300.0
```

Delete a ship:
```bash
python cli.py delete <ship_id>
```

Check API health:
```bash
python cli.py health
```

### Advanced Options

Use a different API URL:
```bash
python cli.py --url http://api.example.com:8080 list
```

Update multiple ship properties:
```bash
python cli.py update <ship_id> --name "New Name" --pos-x 10.0 --pos-y 20.0 --dest-x 30.0 --dest-y 40.0
```

## Example API Usage with curl

Create a ship:
```bash
curl -X POST http://localhost:5000/ships \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Enterprise",
    "position_x": 0.0,
    "position_y": 0.0,
    "destination_x": 100.0,
    "destination_y": 100.0
  }'
```

Get all ships:
```bash
curl http://localhost:5000/ships
```

Move a ship:
```bash
curl -X POST http://localhost:5000/ships/<ship_id>/move \
  -H "Content-Type: application/json" \
  -d '{"x": 50.0, "y": 75.0}'
```

## Ship Data Structure

Each ship has the following properties:
- `id`: Unique identifier (UUID)
- `name`: Ship name (string)
- `position_x`: Current X coordinate (float)
- `position_y`: Current Y coordinate (float)
- `destination_x`: Destination X coordinate (float)
- `destination_y`: Destination Y coordinate (float)

## Error Handling

The API returns appropriate HTTP status codes and error messages:
- 200: Success
- 201: Created
- 400: Bad Request (invalid data)
- 404: Not Found
- 500: Internal Server Error

## Development

To run in development mode with debug enabled, the Flask app is already configured with `debug=True` in the main.py file.
