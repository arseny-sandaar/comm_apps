import asyncio
import websockets
import json
import shutil
from math import radians, cos, sin, sqrt, atan2

# Get the width of the terminal
terminal_width = shutil.get_terminal_size().columns

previous_coordinates = {}
total_distances = {}

def calculate_distance(coordinates):
    # Convert latitude and longitude from degrees to radians
    lat_prev, lon_prev, lat_current, lon_current = map(radians, coordinates)
    
    # Haversine formula
    dlon = lon_current - lon_prev
    dlat = lat_current - lat_prev
    a = sin(dlat/2)**2 + cos(lat_prev) * cos(lat_current) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Radius of the Earth in meters
    R = 6371000 
    
    # Calculate the distance
    distance = R * c
    
    return distance

async def calculate_distances(websocket, path):
    async for message in websocket:
        try:
            current_coordinates = json.loads(message)
            print(f"Received coordinates: {json.dumps(current_coordinates, indent=4)}")
            
            distances = {}
            for id, current in current_coordinates.items():
                if id in previous_coordinates:
                    prev = previous_coordinates[id]
                    coordinates = [prev[0], prev[1], current[0], current[1]]
                    distance = calculate_distance(coordinates)
                    distances[id] = distance
                    try:
                        total_distance_prev = total_distances[id]
                        total_distances[id] = total_distance_prev + distance
                    except KeyError:
                        total_distances[id] = distance
                        
                previous_coordinates[id] = current

            print(f"Last traveled distances (m): {json.dumps(distances, indent=4)}")
            print(f"Total distances (m): {json.dumps(dict(sorted(total_distances.items())), indent=4)}")
            print('-' * terminal_width)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"Error: {e}")

async def main():
    server = await websockets.serve(calculate_distances, "localhost", 8766)
    print("Server started on ws://localhost:8766")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())