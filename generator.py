import asyncio
import websockets
import random
import json
import shutil
from math import radians, cos

# Get the width of the terminal
terminal_width = shutil.get_terminal_size().columns

number_of_dots = 0
regularity = 0
start_sending = False
previous_coordinates = {}
# assumed speed of an animal
speed = 0.25 # m/s this is speed along axes

# to simulate asynchronous positions tracking generate list of ids 
def generate_coordinate_senders(number_of_dots):
    if number_of_dots < 1:
        return []
    
    # Create a list of ids from 1 to the given number (inclusive)
    num_list = list(range(1, number_of_dots + 1))
    
    # Shuffle the list to randomize the order
    random.shuffle(num_list)
    
    # Select a random number of elements from the shuffled list
    list_length = random.randint(1, number_of_dots)
    random_list = num_list[:list_length]
    
    # Sort the selected elements to make the list ascending
    random_list.sort()
    
    return random_list

# to generate next position from the previous
def generate_next_position(previous_coordinate, regularity):
    x_prev, y_prev = previous_coordinate
    return (x_prev + random.uniform(0,1) * speed * regularity, y_prev + random.uniform(0,1) * speed * regularity)

# convert to WSG84
turin_lat = 45.0703
turin_lon = 7.6869

def convert_to_wsg(xy):
    x, y = xy
    # Conversion factors (approximate, adjust as needed based on actual local area)
    # 1 degree of latitude ~= 111 km
    # 1 degree of longitude ~= 111 km * cos(latitude)
    lat_offset = y / 111000.0
    lon_offset = x / (111000.0 * cos(radians(turin_lat)))

    # Calculate WGS84 coordinates
    new_lat = turin_lat + lat_offset
    new_lon = turin_lon + lon_offset
    return (new_lat, new_lon)

async def send_coordinates_periodically():
    global start_sending, number_of_dots, regularity, previous_coordinates
    uri = "ws://localhost:8766"  # URI for the analytics
    async with websockets.connect(uri) as websocket:
        while True:
            if start_sending:
                animals_id = generate_coordinate_senders(number_of_dots)
                coordinates = {}
                for id in animals_id:
                    coordinates[id] = generate_next_position(previous_coordinates[id], regularity)
                coordinates_wsg = {}
                for id, xy in coordinates.items():
                    coordinates_wsg[id] = convert_to_wsg(xy) 
                # print(f"Previous coordinates: \n {json.dumps(previous_coordinates, indent=4)}")
                print(f"Generated coordinates for {len(animals_id)} items: \n {json.dumps(coordinates_wsg, indent=4)}")
                
                await websocket.send(json.dumps(coordinates_wsg))
                print(f"Sent coordinates to analytics")
                print('-' * terminal_width)
                for id, current in coordinates.items():
                    previous_coordinates[id] = current
                
            await asyncio.sleep(regularity)

async def handle_message(websocket):
    global number_of_dots, regularity, start_sending, previous_coordinates
    async for message in websocket:
        print(f"Received: {message}")
        number_of_dots, regularity = map(int, message.split(","))
        print(f"Number of animals: {number_of_dots}, Regularity: {regularity} seconds")
        start_sending = True
        for i in list(range(1,number_of_dots+1)):
            previous_coordinates[i] = (random.uniform(0, speed*regularity), random.uniform(0, speed * regularity))

async def handler(websocket, path):
    await handle_message(websocket)

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("Server started on ws://localhost:8765")
    
    # Start the task to send coordinates periodically
    asyncio.create_task(send_coordinates_periodically())
    
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())