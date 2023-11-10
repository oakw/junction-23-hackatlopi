import os
import json

class OriginalConfig():
  def load_agent_config(user_question):
    try:
      json_file_path = "agent_config.json"
      with open(json_file_path, 'r') as file:
        data = json.load(file)
        question_specified = data["goal"][0].replace("<INPUT_QUESTION>", user_question)
        data["goal"][0] = question_specified
    except:
      # TODO: provide default data
      # TODO: consider proper tool name
      data = {
        "name": "Super AI question answerer",
        "description": "This AI agent is capable of answering any user question, by also supplying resources as a support",
        "goal": [
          f"Find a precise and detailed answer to the question asked by the user: {user_question}", 
          "Supply sources and argumentation to the answer"
          ],
        "instruction": [
          "Split the question into subquestions", 
          "Use the tool \"InternetSearch\" to do an Internet search for each subquestion",
          "Summarise the insights from Internet search and add your commentary or explanations",
          "Save your response as a text file"
          ],
        "agent_workflow": "Goal Based Workflow",
        "constraints": [
          "~4000 word limit for short term memory",
          "Don't ask questions to user to specify unclarities",
          "Exclusively use the commands listed in double quotes e.g. \"command name\"",
          "Don't make assumptions without any supportive data or evidence"
          ],
        "tools": [
          {"name": "InternetSearch"}
        ],
        "iteration_interval": 500,
        "max_iterations": 10,
        "model": "gpt-4",
      }
    return data

  def __init__(self) -> None:
    self.SUPER_AGI_KEY = "SUPER_AGI_KEY"
    self.SUPER_AGI_URL = "SUPER_AGI_URL"
    
    self.SERVER_HOST = "SERVER_HOST"
    self.SERVER_PORT = "SERVER_PORT"

  @classmethod
  def get_server_data(self):
    return (
      os.environ.get(self.SERVER_HOST), 
      os.environ.get(self.SERVER_PORT)
    )

  # Super AGI specific
  @classmethod
  def get_super_agi_key(self):
    return os.environ.get(self.SUPER_AGI_KEY)
  
  @classmethod
  def get_super_agi_url(self):
    return os.environ.get(self.SUPER_AGI_URL)
  
  @classmethod
  def get_agent_config(self):
    return self.load_agent_config()
