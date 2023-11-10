import os
import json

class OriginalConfig():
  def load_agent_config():
    try:
      json_file_path = "agent_config.json"
      with open(json_file_path, 'r') as file:
        data = json.load(file)
    except:
      # TODO: provide default data
      # TODO: consider proper tool name
      data = {
        "name": "Super AI question answerer",
        "description": "This AI agent is capable of answering any user question, by also supplying resources as a support",
        "goal": [
          "Find a precise and detailed answer to the question asked by the user (2 paragraphs max.)", 
          "Supply sources and argumentation to the answer"
          ],
        "instruction": [
          "Split the question into subquestions", 
          "Do a Internet search for each subquestion",
          "Summarise the insights from Internet search and add your commentary or explanations",
          "Save your response as a text file"
          ],
        "agent_workflow": "Goal Based Workflow",
        "constraints": [
          "Don't ask questions to user to specify unclarities",
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

  @classmethod
  def get_super_agi_key(self):
    return os.environ.get(self.SUPER_AGI_KEY)
  
  @classmethod
  def get_super_agi_url(self):
    return os.environ.get(self.SUPER_AGI_URL)
  
  @classmethod
  def get_agent_config(self):
    return self.load_agent_config()
