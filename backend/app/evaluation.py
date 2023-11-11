import comet_llm
import os


class LlmEvaluator():
  def __init__(self) -> None:
    comet_api_key = os.environ.get("COMET_API_KEY")
    comet_workspace = os.environ.get("COMET_WORKSPACE")
    comet_project = os.environ.get("COMET_PROJECT")

    comet_llm.init(comet_api_key, comet_workspace, project=comet_project)

  def log_result(prompt, result):
    # TODO: add more data to log
    comet_llm.log_prompt(
      prompt=prompt,
      output=result
    )