import threading
import time

from flask import (
  Flask, 
  jsonify, 
  request
)

from app.superagi_tools import SuperAGIInteractor

app = Flask(__name__)
super_agi_interactor = SuperAGIInteractor()

# write_response_to_file = threading.Event()

def listen_for_agent_completion(agent_id, run_id):
  while True:
    agent_status = super_agi_interactor.retrieve_agent_status(agent_id=agent_id, run_ids=[run_id])
    if agent_status[0]['status'] == 'COMPLETED':
      # TODO: write response to file
      print("Writing to file...")
      break
    time.sleep(1)

@app.route('/api/hello', methods=['GET'])
def health():
  return jsonify({'message': 'Hello, API!'})

@app.route('/api/prompt', methods=['POST'])
def prompt():
  data = request.get_json()
  if 'questions' not in data:
    return jsonify({'error': 'Provide questions'}), 400
  
  questions = data['questions']
  questions_processed = []
  for i, q in enumerate(questions):
    questions_processed.append(f"#{i}: {q}")
  questions_processed_text = "\n".join(questions_processed)

  if super_agi_interactor.is_running_agent():
    try:
      super_agi_interactor.pause_agent()
    except:
      return jsonify({'error': 'Failed to restart agent'}), 500

  agent_id = super_agi_interactor.create_agent_instance(questions_processed_text)
  run_id = super_agi_interactor.start_agent_run(agent_id=agent_id)

  write_thread = threading.Thread(target=listen_for_agent_completion, args=(agent_id, run_id))
  write_thread.start()
  # write_thread.is_alive()

  return jsonify({'message': 'Hello, API!'})