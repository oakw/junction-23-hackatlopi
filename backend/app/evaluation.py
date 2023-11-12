# import comet_llm
import os

from app.db_conn import DbConnection

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

    # comet_llm.init(comet_api_key, comet_workspace, project=comet_project)
    self.db_conn = DbConnection()

  async def describe_metrics(self, metric_list, avg_value, max_value):
    metric_list_processed = ", ".join([str(round(i, 1)) for i in metric_list])
    messages = [
      ChatMessage(
        role=MessageRole.SYSTEM, 
        content="You are a data analyst and your task is to give some comment about data, given list of values and average and maximum values. Describe the data against these values and provide some short commentary."
      ),
      ChatMessage(role=MessageRole.USER, content=f"The list of values: {metric_list_processed}, average value: {avg_value}, maximum value: {max_value}")    
    ]
    conclusion = await self.llm.achat(messages=messages)
    return conclusion.message.content

  # def log_result(self, prompt, answer):
  #   # TODO: add more data to log
  #   comet_llm.log_prompt(
  #     prompt=prompt,
  #     output=answer
  #   )

  async def give_pair_evaluation(self, prompt, answer):
    correctness_evaluator = CorrectnessEvaluator(service_context=self.service_context)
    faithfulness_evaluator = FaithfulnessEvaluator(service_context=self.service_context)

    # GUIDELINE = "The response should fully answer the query."
    # guideline_evaluator = GuidelineEvaluator(service_context=self.service_context, guidelines=GUIDELINE)
    
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
    reference = await self.llm.achat(messages=messages)
    reference = reference.message.content

    print("reference: ", reference)

    correctness_eval_res = await correctness_evaluator.aevaluate(
      query=prompt,
      response=answer,
      reference=reference
    )
    faithfulness_eval_res = await faithfulness_evaluator.aevaluate(
      query=prompt,
      response=answer,
      contexts=[reference]
    )

    # guideline_eval_res = await guideline_evaluator.aevaluate(
    #   query=prompt,
    #   response=answer,
    #   contexts=[reference]
    # )
    # guideline_eval_res.passing

    pairwise_eval_res = await pairwise_evaluator.aevaluate(
      query=prompt,
      response=answer,
      reference=reference,
      second_response=reference
      # TODO: add second response
    )
    relevancy_eval_res = await relevancy_evaluator.aevaluate(
      query=prompt,
      response=answer,
      contexts=[reference]
    )
    semantics_eval_res = await semantics_evaluator.aevaluate(
      query=prompt,
      response=answer,
      reference=reference
      # TODO: add second contexts
    )

    print("prompt: ", prompt)
    print("answer: ", answer)

    self.db_conn.add_result(
      prompt=prompt, answer=answer, reference=reference,
      correctness=correctness_eval_res.score, correctness_exp=correctness_eval_res.feedback,
      faithfulness=faithfulness_eval_res.score, faithfulnes_exp=faithfulness_eval_res.feedback,
      # guideline=guideline_eval_res.score, guideline_exp=guideline_eval_res.feedback,
      guideline=0, guideline_exp="N/A",
      pairwise=pairwise_eval_res.score, pairwise_exp=pairwise_eval_res.feedback,
      relevancy=relevancy_eval_res.score, relevancy_exp=relevancy_eval_res.feedback,
      semantics=semantics_eval_res.score, semantics_exp=semantics_eval_res.feedback
    )

  async def get_average_metric_stats(self):
    res = self.db_conn.retrieve_all()
    if len(res) == 0 or res is None:
      result = {
        "correctness": "N/A",
        "faithfulness": "N/A",
        "guideline": "N/A",
        "pairwise": "N/A",
        "relevancy": "N/A",
        "semantics": "N/A"
      }
      return result

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
      "correctness": f"{correctness_avg} / 5.0 ; {await self.describe_metrics(correctness_evals, correctness_avg, 5)}",
      "faithfulness": f"{faithfulness_avg} / 5.0 ; {await self.describe_metrics(faithfulness_evals, faithfulness_avg, 5)}",
      # "guideline": f"{guideline_avg} / 5.0 ; {self.describe_metrics(guideline_evals, guideline_avg, 5)}",
      "guideline": f"{guideline_avg} / 5.0 ; N/A",
      "pairwise": f"{pairwise_avg} / 5.0 ; {await self.describe_metrics(pairwise_evals, pairwise_avg, 5)}",
      "relevancy": f"{relevancy_avg} / 5.0 ; {await self.describe_metrics(relevancy_evals, relevancy_avg, 5)}",
      "semantics": f"{semantics_avg} / 5.0 ; {await self.describe_metrics(semantics_evals, semantics_avg, 5)}"
    }
    # result = {
    #   "correctness": f"{correctness_avg} / 5.0 ; {self.describe_metrics(correctness_evals, correctness_avg, 5)}",
    #   "faithfulness": f"{faithfulness_avg} / 5.0 ; {self.describe_metrics(faithfulness_evals, faithfulness_avg, 5)}",
    #   # "guideline": f"{guideline_avg} / 5.0 ; {self.describe_metrics(guideline_evals, guideline_avg, 5)}",
    #   "guideline": f"{guideline_avg} / 5.0 ; N/A",
    #   "pairwise": f"{pairwise_avg} / 5.0 ; {self.describe_metrics(pairwise_evals, pairwise_avg, 5)}",
    #   "relevancy": f"{relevancy_avg} / 5.0 ; {self.describe_metrics(relevancy_evals, relevancy_avg, 5)}",
    #   "semantics": f"{semantics_avg} / 5.0 ; {self.describe_metrics(semantics_evals, semantics_avg, 5)}"
    # }
    return result