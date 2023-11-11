import asyncio
import websockets
import json
from threading import Thread
import time

# def print_hello_world():
#     while True:
#         print("Hello, world")
#         time.sleep(3)

# t = Thread(target=print_hello_world)
# t.start()


suggestions = [
    {
        "of_type": "Faithfullness",
        "content": "It is wrong to cheat on your partner. Make it better!"
    },
    {
        "of_type": "Content",
        "content": "You should be happy with what you have. Make it better!"
    }
]

async def answer(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            role = data["role"]
            message = data["message"]


            if role == "AI":
                if "suggestions" in data:
                    response = {
                        "role": role,
                        "message": message,
                        "suggestions": data["suggestions"]
                    }
                    
                else:
                    response = {
                        "role": role,
                        "message": message,
                    }
                response_json = json.dumps(response)

                await websocket.send(response_json)

                
            elif role == "User":
                # Send the message to the AI and await its response
                ai_response = await AI_send_request(message)

                # Send the AI's response back to the user
                await websocket.send(ai_response)

        except json.JSONDecodeError:
            print("Received message is not valid JSON")

async def AI_send_request(message):
    async with websockets.connect("ws://localhost:8766") as ai_websocket:
        # Send the user's message to the AI
        ai_request = {
            "role": "User",
            "message": message
        }
        await ai_websocket.send(json.dumps(ai_request))

        # Await the AI's response
        ai_response = await ai_websocket.recv()
        return ai_response



async def main():
    async with websockets.serve(lambda websocket, path, *args, **kwargs: answer(websocket, path), "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
