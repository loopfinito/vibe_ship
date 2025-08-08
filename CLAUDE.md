# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based Ship Management API with a command-line interface. The system manages ships with positions, destinations, and speeds using in-memory storage.

## Core Components

- `main.py` - Flask REST API server with Ship dataclass model and all endpoints
- `cli.py` - Command-line interface for interacting with the API
- `tests/test_main.py` - Pytest test suite focusing on destination and speed setting functionality

## Development Commands

### Running the Application
```bash
python main.py  # Starts Flask server on localhost:5000 with debug=True
```

### Testing
```bash
pytest tests/  # Run all tests
pytest tests/test_main.py::TestSetDestination  # Run specific test class
pytest tests/test_main.py::TestSetDestination::test_set_destination_success  # Run specific test
```

### Code Quality
```bash
pylint $(git ls-files '*.py')  # Lint all Python files (used in CI)
```

### CLI Usage
```bash
python cli.py list  # List all ships
python cli.py create "Ship Name" 0.0 0.0 100.0 100.0  # Create ship
python cli.py get <ship_id>  # Get ship details
python cli.py move <ship_id> 50.0 75.0  # Move ship
python cli.py destination <ship_id> 200.0 300.0  # Set destination
python cli.py health  # Check API health
```

## Architecture

### Ship Model
The `Ship` dataclass in `main.py:8-24` contains:
- `name`, `position_x/y`, `destination_x/y`, `speed` (default 1.0)
- Auto-generated UUID `id`
- In-memory storage in global `ships` dictionary

### API Endpoints
- Ships CRUD: `/ships` (GET, POST), `/ships/<id>` (GET, PUT, DELETE)
- Ship actions: `/ships/<id>/move`, `/ships/<id>/destination`, `/ships/<id>/speed`
- Health check: `/health`

### CLI Architecture  
The `ShipCLI` class in `cli.py:13-132` provides a wrapper around HTTP requests to the API with proper error handling and formatted output.

### Testing Strategy
Tests use pytest with fixtures for Flask test client and sample ship data. Focus is on comprehensive endpoint validation including error cases and edge conditions.

## Key Patterns

- All coordinates accept float values including negative numbers and zero
- Speed must be positive (> 0)
- API returns JSON with appropriate HTTP status codes
- CLI provides formatted output and handles connection errors
- In-memory storage means data is lost on server restart