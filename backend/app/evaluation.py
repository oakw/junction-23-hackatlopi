import comet_llm
import os

from db_conn import DbConnection

from llama_index import ServiceContext
from llama_index.llms import (
  OpenAI,
  ChatMessage,
  MessageRole
)
from llama_index.evaluation import (
  CorrectnessEvaluator,
  FaithfulnessEvaluator,
  GuidelineEvaluator,
  PairwiseComparisonEvaluator,
  RelevancyEvaluator,
  SemanticSimilarityEvaluator
)

def calclucalte_avg(nums):
  if not nums:
    return 0
  total = sum(nums)
  average = total / len(nums)
  return average

class LlmEvaluator():
  def __init__(self) -> None:
    comet_api_key = os.environ.get("COMET_API_KEY")
    comet_workspace = os.environ.get("COMET_WORKSPACE")
    comet_project = os.environ.get("COMET_PROJECT")

    self.llm = OpenAI(model="gpt-4")
    self.service_context = ServiceContext.from_defaults(llm=self.llm)

    comet_llm.init(comet_api_key, comet_workspace, project=comet_project)
    self.db_conn = DbConnection()

  def describe_metrics(self, metric_list, avg_value, max_value):
    metric_list_processed = ", ".join(metric_list)
    messages = [
      ChatMessage(
        role=MessageRole.SYSTEM, 
        content="You are a data analyst and your task is to give some comment about data, given list of values and average and maximum values. Describe the data against these values and provide some short commentary."
      ),
      ChatMessage(role=MessageRole.USER, content=f"The list of values: {metric_list_processed}, average value: {avg_value}, maximum value: {max_value}")    
    ]
    conclusion = self.llm.chat(messages=messages)
    return conclusion.message.content

  def log_result(self, prompt, answer):
    # TODO: add more data to log
    comet_llm.log_prompt(
      prompt=prompt,
      output=answer
    )

  def give_pair_evaluation(self, prompt, answer):
    correctness_evaluator = CorrectnessEvaluator(service_context=self.service_context)
    faithfulness_evaluator = FaithfulnessEvaluator(service_context=self.service_context)
    guideline_evaluator = GuidelineEvaluator(service_context=self.service_context)
    pairwise_evaluator = PairwiseComparisonEvaluator(service_context=self.service_context)
    relevancy_evaluator = RelevancyEvaluator(service_context=self.service_context)
    semantics_evaluator = SemanticSimilarityEvaluator(service_context=self.service_context)

    messages = [
      ChatMessage(
        role=MessageRole.SYSTEM, 
        content="Your task is to give a concise and high quality answer with supportive argumentation, no longer than two paragraphs"
      ),
      ChatMessage(role=MessageRole.USER, content=prompt)
    ]
    reference = self.llm.chat(messages=messages)
    reference = reference.message.content

    correctness_eval_res = correctness_evaluator.evaluate(
      query=prompt,
      response=answer,
      contexts=[reference]
    )
    faithfulness_eval_res = faithfulness_evaluator.evaluate(
      query=prompt,
      response=answer,
      contexts=[reference]
    )
    guideline_eval_res = guideline_evaluator.evaluate(
      query=prompt,
      response=answer,
      contexts=[reference]
    )
    pairwise_eval_res = pairwise_evaluator.evaluate(
      query=prompt,
      response=answer,
      contexts=[reference]
    )
    relevancy_eval_res = relevancy_evaluator.evaluate(
      query=prompt,
      response=answer,
      contexts=[reference]
    )
    semantics_eval_res = semantics_evaluator.evaluate(
      query=prompt,
      response=answer,
      contexts=[reference]
    )

    self.db_conn.add_result(
      prompt=prompt, answer=answer, reference=reference,
      correctness=correctness_eval_res.score, correctness_exp=correctness_eval_res.feedback,
      faithfulness=faithfulness_eval_res.score, faithfulnes_exp=faithfulness_eval_res.feedback,
      guideline=guideline_eval_res.score, guideline_exp=guideline_eval_res.feedback,
      pairwise=pairwise_eval_res.score, pairwise_exp=pairwise_eval_res.feedback,
      relevancy=relevancy_eval_res.score, relevancy_exp=relevancy_eval_res.feedback,
      semantics=semantics_eval_res.score, semantics_exp=semantics_eval_res.feedback
    )

  def get_average_metric_stats(self):
    res = self.db_conn.retrieve_all()
    correctness_evals = [item[3] for item in res]
    faithfulness_evals = [item[5] for item in res]
    guideline_evals = [item[7] for item in res]
    pairwise_evals = [item[9] for item in res]
    relevancy_evals = [item[11] for item in res]
    semantics_evals = [item[13] for item in res]

    correctness_avg = calclucalte_avg(correctness_evals)
    faithfulness_avg = calclucalte_avg(faithfulness_evals)
    guideline_avg = calclucalte_avg(guideline_evals)
    pairwise_avg = calclucalte_avg(pairwise_evals)
    relevancy_avg = calclucalte_avg(relevancy_evals)
    semantics_avg = calclucalte_avg(semantics_evals)

    result = {
      "correctness": f"{correctness_avg} / 5.0 ; {self.describe_metrics(correctness_evals, correctness_avg, 5)}",
      "faithfulness": f"{faithfulness_avg} / 5.0 ; {self.describe_metrics(faithfulness_evals, faithfulness_avg, 5)}",
      "guideline": f"{guideline_avg} / 5.0 ; {self.describe_metrics(guideline_evals, guideline_avg, 5)}",
      "pairwise": f"{pairwise_avg} / 5.0 ; {self.describe_metrics(pairwise_evals, pairwise_avg, 5)}",
      "relevancy": f"{relevancy_avg} / 5.0 ; {self.describe_metrics(relevancy_evals, relevancy_avg, 5)}",
      "semantics": f"{semantics_avg} / 5.0 ; {self.describe_metrics(semantics_evals, semantics_avg, 5)}"
    }
    return result