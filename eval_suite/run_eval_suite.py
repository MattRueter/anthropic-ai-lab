from .helpers import *

def run_eval_suite(
  generate, # the func which calls the llm (func being evalutated)
  prompt,  # system prompt for the feature (prompt being evaluated)
  reqs,  # original request object as python dict
  results_path, # location to save the results
  evaluate, # evaluation function calls the LLM to compare req and responses
  eval_prompt, # evaluation prompt
  evaluation_results_path # location to save evaluation results
  ):
  
  # Append file name to path for current dataset.
  results_path = results_path / reqs["meta"]["file_name"]
  evaluation_results_path = evaluation_results_path  / reqs["meta"]["file_name"]


  # Make initial call to LLM with example data
  results = iterator(generate, prompt, reqs)
  
  # save results
  save(results, results_path)


  # Evaluate the results.
  evaluation = evaluate_iterator(evaluate, eval_prompt, results )

  ##before saving average the scores of the evaluation
  evals = evaluation["data"]
  scores = []

  for eval in evals:
    scores.append(eval["score"])
  
  score_sum = sum(scores)
  avg = score_sum / len(scores) if scores else 0
  evaluation["meta"]["average_score"] = avg
  
  # save evaluation_results to file (save as json)
  save(evaluation, evaluation_results_path)