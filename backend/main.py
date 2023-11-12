import asyncio
import websockets
import json
from threading import Thread
from dotenv import load_dotenv
import time
from hardware_analyzer import docker_monitor

from app import evaluation

load_dotenv()


class BridgeEvaluator():
    def __init__(self) -> None:
        self.transport = DataTransport(self)
        asyncio.get_event_loop().run_until_complete(self.transport.start_server)
        asyncio.get_event_loop().run_forever()

        # Start monitoring docker container that runs LLM
        self.monitor = docker_monitor.DockerMonitor("nginxtest-client-1")
        self.monitor.start()

    async def extract_analysis(self):
        evaluator = evaluation.LlmEvaluator()
        metric_stats = evaluator.get_average_metric_stats()

        await self.respond(dict(
            id=1, # TODO: make dynamic
            type="analysis",
            response=metric_stats
        ))

    async def get_monitored_data(self):
        while True:
            # Physical performance measurments
            total_cpu_usage = self.monitor.get_results().measurements[1].total_cpu_usage
            memory_usage = self.monitor.get_results().measurements[1].memory_usage
            read_time = self.monitor.get_results().measurements[1].read_time.isoformat()
            rx_bytes = self.monitor.get_results().measurements[1].networks["eth0"]["rx_bytes"]
            tx_bytes = self.monitor.get_results().measurements[1].networks["eth0"]["tx_bytes"]

            measurment_data = {
                "total_cpu_usage": total_cpu_usage,
                "memory_usage": memory_usage,
                "read_time": read_time,
                "rx_bytes": rx_bytes,
                "tx_bytes": tx_bytes
            }
            # Serialize to JSON before sending
            await self.respond(measurment_data)

    async def send_chat_message(self, message: str):
        # TODO: determine and extract proper model URL
        async with websockets.connect("ws://localhost:8766") as ai_websocket:
            # Choose the model to use for chat
            choose_model = {
                "type": "choose_model",
                "model_name": "orca-mini-3b-gguf2-q4_0.gguf", # TODO: make dynamic model name
                "id": "1"
            }
            await ai_websocket.send(json.dumps(choose_model))
            
            # Start the chat session
            start_chat = {
                "type": "start_chat_session",
                "system_prompt": "You are an advanced AI assistant designed to answer questions and providing supproting evidence", # TODO: make dynamic
                "prompt_template": "", # TODO: make dynamic
                "id": "1"
            }
            await ai_websocket.send(json.dumps(start_chat))

            # Start monitoring LLMs physical resources (after starting the chat?)
            async def start_monitor():
                t = Thread(target=self.get_monitored_data)
                t.start()
                while True:
                    time.sleep(1)
                    await self.get_monitored_data()

            asyncio.create_task(start_monitor())

            # Send the prompt
            ai_request = {
                "type": "prompt",
                "prompt": message,
                "max_tokens": 300, # TODO: make dynamic
                "id": "1"
            }
            await ai_websocket.send(json.dumps(ai_request))

            # Await the AI's response
            ai_response = await ai_websocket.recv()
            return ai_response
    
    async def stop_everything(self) -> None:
        await self.respond(dict(
            type="killed",
        ))
        exit()

    async def respond(self, response: dict) -> None:
        await self.transport.send_data(json.dumps(response))

    async def receive(self, message: str) -> None:
        print("Received data:", message)
        data = json.loads(message)
        await self.respond(dict(
            type="received"
        ))

        match data['type']:
            case 'send_chat_message':
                await self.send_chat_message(data['message'])
            case 'extract_analysis':
                await self.extract_analysis()
            case 'stop_everything':
                await self.stop_everything()


class DataTransport():
    def __init__(self, bridge_evaluator: BridgeEvaluator):
        self.bridge_evaluator = bridge_evaluator
        self.start_server = websockets.serve(self.server, "localhost", 8764)

    async def handle_message(self, message):
        await self.bridge_evaluator.receive(message)

    async def send_data(self, data):
        await self.websocket.send(data)

    async def server(self, websocket, path):
        while True:
            self.websocket = websocket
            message = await self.websocket.recv()
            await self.handle_message(message)


if __name__ == "__main__":
    print("Hello world!")
    bridge_evaluator = BridgeEvaluator()