from __future__ import annotations
from gpt4all import GPT4All
import json
import asyncio
import websockets
import os



AVAILABLE_MODELS = ['llama-2-13b-chat.Q4_0.gguf', 'orca-mini-3b-gguf2-q4_0.gguf']
MODEL_FOLDER = f"{os.path.dirname(os.path.abspath(__file__))}/models"

class DataTransport():
    def __init__(self, model_runner: ModelRunner):
        self.model_runner = model_runner
        self.start_server = websockets.serve(self.server, "0.0.0.0", 8765)

    async def handle_message(self, message):
        await self.model_runner.receive(message)

    async def send_data(self, data):
        await self.websocket.send(data)

    async def server(self, websocket, path):
        while True:
            self.websocket = websocket
            message = await self.websocket.recv()
            await self.handle_message(message)


class ModelRunner():

    def __init__(self):
        self.transport = DataTransport(self)
        asyncio.get_event_loop().run_until_complete(self.transport.start_server)
        asyncio.get_event_loop().run_forever()

    async def attach_model(self, model_folder: str, model_name: str, id: str) -> None:
        self.model = GPT4All(model_name, model_path=model_folder, allow_download=False)
        await self.respond(dict(
            id=id,
            type="model_attached",
        ))

    async def choose_model(self, model_name: str, id: str) -> None:
        if model_name in AVAILABLE_MODELS:
            await self.attach_model(MODEL_FOLDER, model_name, id)

    async def start_chat_session(self, system_prompt: str, prompt_template: str, id: str) -> None:
        if not self.is_model_selected():
            await self.respond(dict(
                id=id,
                type="error",
                message="No model selected",
            ))
            return
        self.chat_session = self.model.chat_session(system_prompt, prompt_template)
        await self.respond(dict(
            id=id,
            type="chat_session_started",
        ))

    async def prompt(self, prompt: str, max_tokens: int, id: str) -> str:
        if not self.is_chat_session_started():
            await self.respond(dict(
                id=id,
                type="error",
                message="No chat session started",
            ))
            return
        await self.respond(dict(
            id=id,
            type="response",
            response=self.model.generate(prompt, max_tokens=max_tokens)
        ))
    
    async def stop_everything(self) -> None:
        await self.respond(dict(
            type="killed",
        ))
        exit()

    def is_model_selected(self) -> bool:
        return hasattr(self, 'model')
    
    def is_chat_session_started(self) -> bool:
        return hasattr(self, 'chat_session')

    async def respond(self, response: dict) -> None:
        await self.transport.send_data(json.dumps(response))

    async def receive(self, message: str) -> None:
        print("Received data:", message)
        data = json.loads(message)
        await self.respond(dict(
            type="received"
        ))

        match data['type']:
            case 'choose_model':
                await self.choose_model(data['model_name'], data['id'])
            case 'start_chat_session':
                await self.start_chat_session(data['system_prompt'], data['prompt_template'], data['id'])
            case 'prompt':
                await self.prompt(data['prompt'], data['max_tokens'], data['id'])
            case 'stop_everything':
                await self.stop_everything()



if __name__ == "__main__":
    runner = ModelRunner()