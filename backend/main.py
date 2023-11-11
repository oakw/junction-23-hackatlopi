import asyncio
import websockets
import json
from threading import Thread
from dotenv import load_dotenv
import time
from hardware_analyzer import docker_monitor

load_dotenv()

monitor = docker_monitor.DockerMonitor("nginxtest-client-1")
monitor.start()


async def get_monitored_data(websocket, path):
    while True:

        total_cpu_usage = monitor.get_results().measurements[1].total_cpu_usage
        memory_usage = monitor.get_results().measurements[1].memory_usage
        read_time = monitor.get_results().measurements[1].read_time.isoformat()
        rx_bytes = monitor.get_results().measurements[1].networks["eth0"]["rx_bytes"]
        tx_bytes = monitor.get_results().measurements[1].networks["eth0"]["tx_bytes"]
        
        measurment_data = {
            "total_cpu_usage": total_cpu_usage,
            "memory_usage": memory_usage,
            "read_time": read_time,
            "rx_bytes": rx_bytes,
            "tx_bytes": tx_bytes
        }
        # Serialize to JSON before sending
        await websocket.send(json.dumps(measurment_data))


async def answer(websocket, path):
    async for message in websocket:
        async def start_monitor(websocket, path):
            t = Thread(target=get_monitored_data, args=(websocket, path))
            t.start()
            while True:
                time.sleep(1)
                await get_monitored_data(websocket, path)

        asyncio.create_task(start_monitor(websocket, path))

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
