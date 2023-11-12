from websocket import create_connection
import time
import json


class WebsocketClient():
    def __init__(self):
        self.websocket = create_connection("ws://localhost:8765")

    def send(self, message):
        self.websocket.send(message)

    def wait_for_response(self):
        return self.websocket.recv()


test_class = WebsocketClient()  
time.sleep(1)  
test_class.send(json.dumps((
    dict(
        model_name="orca-mini-3b-gguf2-q4_0.gguf",
        id="1",
        type="choose_model"
    )
)))
print(test_class.wait_for_response())
print(test_class.wait_for_response())

test_class.send(json.dumps((
    dict(
        type="start_chat_session",
        id="1",
        system_prompt="You are a teacher who reviews essays..",
        prompt_template="Review the message of a student: {student_message}",
    )
)))
print(test_class.wait_for_response())
print(test_class.wait_for_response())

test_class.send(json.dumps((
    dict(
        type="prompt",
        id="1",
        prompt="Hi!",
        max_tokens=35,
    )
)))
print(test_class.wait_for_response())
print(test_class.wait_for_response())

