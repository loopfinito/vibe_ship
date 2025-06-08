#!/usr/bin/env python3
"""
CLI for Ship Management API
Provides command-line interface to interact with the Flask ship API
"""

import argparse
import requests
import json
import sys
from typing import Optional

class ShipCLI:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
    
    def _make_request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code >= 400:
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else {'error': response.text}
                print(f"Error {response.status_code}: {error_data.get('error', 'Unknown error')}")
                sys.exit(1)
            
            return response.json()
        
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to API at {self.base_url}")
            print("Make sure the Flask server is running on the correct port.")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            sys.exit(1)
    
    def list_ships(self):
        """List all ships"""
        ships = self._make_request('GET', '/ships')
        
        if not ships:
            print("No ships found.")
            return
        
        print(f"{'ID':<36} {'Name':<20} {'Position':<15} {'Destination':<15}")
        print("-" * 86)
        
        for ship in ships:
            pos = f"({ship['position_x']:.1f}, {ship['position_y']:.1f})"
            dest = f"({ship['destination_x']:.1f}, {ship['destination_y']:.1f})"
            print(f"{ship['id']:<36} {ship['name']:<20} {pos:<15} {dest:<15}")
    
    def get_ship(self, ship_id: str):
        """Get details of a specific ship"""
        ship = self._make_request('GET', f'/ships/{ship_id}')
        
        print(f"Ship Details:")
        print(f"  ID: {ship['id']}")
        print(f"  Name: {ship['name']}")
        print(f"  Position: ({ship['position_x']}, {ship['position_y']})")
        print(f"  Destination: ({ship['destination_x']}, {ship['destination_y']})")
    
    def create_ship(self, name: str, pos_x: float, pos_y: float, dest_x: float, dest_y: float):
        """Create a new ship"""
        data = {
            'name': name,
            'position_x': pos_x,
            'position_y': pos_y,
            'destination_x': dest_x,
            'destination_y': dest_y
        }
        
        ship = self._make_request('POST', '/ships', data)
        print(f"Ship '{ship['name']}' created successfully with ID: {ship['id']}")
    
    def update_ship(self, ship_id: str, name: Optional[str] = None, 
                   pos_x: Optional[float] = None, pos_y: Optional[float] = None,
                   dest_x: Optional[float] = None, dest_y: Optional[float] = None):
        """Update an existing ship"""
        data = {}
        
        if name is not None:
            data['name'] = name
        if pos_x is not None:
            data['position_x'] = pos_x
        if pos_y is not None:
            data['position_y'] = pos_y
        if dest_x is not None:
            data['destination_x'] = dest_x
        if dest_y is not None:
            data['destination_y'] = dest_y
        
        if not data:
            print("No update fields provided.")
            return
        
        ship = self._make_request('PUT', f'/ships/{ship_id}', data)
        print(f"Ship '{ship['name']}' updated successfully.")
    
    def delete_ship(self, ship_id: str):
        """Delete a ship"""
        result = self._make_request('DELETE', f'/ships/{ship_id}')
        print(result['message'])
    
    def move_ship(self, ship_id: str, x: float, y: float):
        """Move ship to new position"""
        data = {'x': x, 'y': y}
        ship = self._make_request('POST', f'/ships/{ship_id}/move', data)
        print(f"Ship '{ship['name']}' moved to position ({x}, {y})")
    
    def set_destination(self, ship_id: str, x: float, y: float):
        """Set ship destination"""
        data = {'x': x, 'y': y}
        ship = self._make_request('POST', f'/ships/{ship_id}/destination', data)
        print(f"Ship '{ship['name']}' destination set to ({x}, {y})")
    
    def health_check(self):
        """Check API health"""
        health = self._make_request('GET', '/health')
        print(f"API Status: {health['status']}")
        print(f"Ships Count: {health['ships_count']}")

def main():
    parser = argparse.ArgumentParser(description='Ship Management CLI')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='Base URL of the ship API (default: http://localhost:5000)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List ships
    subparsers.add_parser('list', help='List all ships')
    
    # Get ship
    get_parser = subparsers.add_parser('get', help='Get ship details')
    get_parser.add_argument('ship_id', help='Ship ID')
    
    # Create ship
    create_parser = subparsers.add_parser('create', help='Create a new ship')
    create_parser.add_argument('name', help='Ship name')
    create_parser.add_argument('pos_x', type=float, help='Initial position X')
    create_parser.add_argument('pos_y', type=float, help='Initial position Y')
    create_parser.add_argument('dest_x', type=float, help='Destination X')
    create_parser.add_argument('dest_y', type=float, help='Destination Y')
    
    # Update ship
    update_parser = subparsers.add_parser('update', help='Update ship details')
    update_parser.add_argument('ship_id', help='Ship ID')
    update_parser.add_argument('--name', help='New ship name')
    update_parser.add_argument('--pos-x', type=float, help='New position X')
    update_parser.add_argument('--pos-y', type=float, help='New position Y')
    update_parser.add_argument('--dest-x', type=float, help='New destination X')
    update_parser.add_argument('--dest-y', type=float, help='New destination Y')
    
    # Delete ship
    delete_parser = subparsers.add_parser('delete', help='Delete a ship')
    delete_parser.add_argument('ship_id', help='Ship ID')
    
    # Move ship
    move_parser = subparsers.add_parser('move', help='Move ship to new position')
    move_parser.add_argument('ship_id', help='Ship ID')
    move_parser.add_argument('x', type=float, help='New X coordinate')
    move_parser.add_argument('y', type=float, help='New Y coordinate')
    
    # Set destination
    dest_parser = subparsers.add_parser('destination', help='Set ship destination')
    dest_parser.add_argument('ship_id', help='Ship ID')
    dest_parser.add_argument('x', type=float, help='Destination X coordinate')
    dest_parser.add_argument('y', type=float, help='Destination Y coordinate')
    
    # Health check
    subparsers.add_parser('health', help='Check API health')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = ShipCLI(args.url)
    
    try:
        if args.command == 'list':
            cli.list_ships()
        elif args.command == 'get':
            cli.get_ship(args.ship_id)
        elif args.command == 'create':
            cli.create_ship(args.name, args.pos_x, args.pos_y, args.dest_x, args.dest_y)
        elif args.command == 'update':
            cli.update_ship(args.ship_id, args.name, 
                           getattr(args, 'pos_x', None), getattr(args, 'pos_y', None),
                           getattr(args, 'dest_x', None), getattr(args, 'dest_y', None))
        elif args.command == 'delete':
            cli.delete_ship(args.ship_id)
        elif args.command == 'move':
            cli.move_ship(args.ship_id, args.x, args.y)
        elif args.command == 'destination':
            cli.set_destination(args.ship_id, args.x, args.y)
        elif args.command == 'health':
            cli.health_check()
    
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

if __name__ == '__main__':
    main()
