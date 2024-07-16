import asyncio
import websockets

# this scrip to send number of animals and regularity in seconds
async def send_input_values():
    uri = "ws://localhost:8765"  # Server URI for the generator
    async with websockets.connect(uri) as websocket:
        number_of_dots = input("Enter number of animals: ")
        regularity = input("Enter regularity (interval in seconds): ")
        
        message = f"{number_of_dots},{regularity}"
        await websocket.send(message)
        print(f"Sent: {message}")
        print("Input values sent successfully")

asyncio.run(send_input_values())