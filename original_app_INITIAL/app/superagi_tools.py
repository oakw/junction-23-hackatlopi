import os

from superagi_client import (
  Client,
  AgentConfig,
  AgentRunFilter,
  AgentUpdateConfig
)

from original_app_INITIAL.config import OriginalConfig

class SuperAGIInteractor():
  def __init__(self) -> None:
    super_agi_key = OriginalConfig.get_super_agi_key
    super_agi_url = OriginalConfig.get_super_agi_url
    self.client = Client(api_key=super_agi_key, url=super_agi_url)

  def create_agent_instance(self):
    agent_config_params = OriginalConfig.get_agent_config()

    # TODO: resolve unused config params
    agent_config = AgentConfig(
      name=agent_config_params['name'],
      description=agent_config_params['description'],
      project_id=None,
      goal=agent_config_params['goal'],
      instruction=agent_config_params['instruction'],
      agent_workflow=agent_config_params['agent_workflow'],
      constraints=agent_config_params['constraints'],
      exit=None,
      permission_type=None,
      tools=agent_config_params['tools'],
      iteration_interval=agent_config_params['iteration_interval'],
      max_iterations=agent_config_params['max_iterations'],
      model=agent_config_params['model'],
      schedule=None,
      user_timezone=None,
      knowledge=None
    )

    agent = self.client.create_agent(agent_config=agent_config)
    return agent['agent_id']
  
  def start_agent_run(self, agent_id):
    run_agent = self.client.create_agent_run(agent_id=agent_id)
    return run_agent['run_id']
  
  def retrieve_agent_status(self, agent_id, run_ids=None):
    if run_ids is None:
      run_status = self.client.get_agent_run_status(agent_id=agent_id)
    else:
      filter_config = AgentRunFilter(run_ids=run_ids)
      run_status = self.client.get_agent_run_status(agent_id=agent_id, agent_run_filter=filter_config)
    # contains 'run_id' and 'status' (RUNNING, ETC)
    return run_status
  
  def pause_agent(self, agent_id, run_id=None):
    # TODO: add check whether the agent is running
    if run_id is None:
      result = self.client.pause_agent(agent_id=agent_id)
    else:
      result = self.client.pause_agent(agent_id=agent_id, agent_run_ids=[run_id])

    if result['result'] is not 'success':
      raise Exception("Failed to pause the agent")

  def resume_agent(self, agent_id, run_id=None):
    # TODO: add check whether the agent is stopped
    if run_id is None:
      result = self.client.resume_agent(agent_id=agent_id)
    else:
      result = self.client.resume_agent(agent_id=agent_id, agent_run_ids=[run_id])

    if result['result'] is not 'success':
      raise Exception("Failed to resume the agent")

  def update_agent_config(self, agent_id, new_data: AgentUpdateConfig):
    updated_config = new_data
    self.client.update_agent(agent_id=agent_id, agent_update_config=updated_config)

  def extract_agent_run_resources(self, run_id):
    resources = self.client.get_agent_run_resources(agent_run_ids=[run_id])
    return resources