import asyncio
import websockets
import json
from threading import Thread
import time

def print_hello_world():
    while True:
        print("Hello, world")
        time.sleep(3)

t = Thread(target=print_hello_world)
t.start()


suggestions = [
    {
        "of_type": "Faithfullness",
        "content": "It is wrong to cheat on your partner. Make it better!"
    },
    {
        "of_type": "Content",
        "content": "It is wrong to cheat on your partner. Make it better!"
    }
]

async def answer(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            user_name = data["role"]
            user_message = data["message"]

            # Pass the user_message to the AI_response function
            ai_response = await AI_response(user_message)

            # Create a response
            response = {
                "role": user_name,
                "message": ai_response["ai_message"],
                "suggestions": ai_response["suggestions"]
            }
            response_json = json.dumps(response)

            # Send the response to the current client
            await websocket.send(response_json)

        except json.JSONDecodeError:
            print("Received message is not valid JSON")

async def AI_response(message):
    # Implement your AI logic here to generate a response
    # For now, let's just return a dictionary with ai_message and suggestions
    ai_response = {
        "ai_message": message,
        "suggestions": suggestions
    }
    return ai_response

async def main():
    async with websockets.serve(lambda websocket, path, *args, **kwargs: answer(websocket, path), "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
