from .helpers import *

def run_eval_suite(
  generate, # the func which calls the llm (func being evalutated). Resturns results json.
  evaluate, # evaluation function calls the LLM to compare req and responses. Returns evaluation json
  config
  ):
  
  # Append file name to path for current dataset. TODO move this to config
  results_path = config.results_path / config.dataset["meta"]["file_name"]


  # Make initial call to LLM with example data
  results = iterator(generate, config.prompt, config.prompt_file, config.dataset)
  
  # save results
  save(results, results_path)

  # Evaluate the results.
  evaluation = evaluate_iterator(evaluate, config.eval_prompt, results )

  ##before saving average the scores of the evaluation
  evals = evaluation["data"]
  scores = []

  for eval in evals:
    scores.append(eval["score"])
  
  score_sum = sum(scores)
  avg = score_sum / len(scores) if scores else 0
  evaluation["meta"]["average_score"] = avg
  
  # save evaluation_results to file (save as json)
  save(evaluation, config.evaluation_results_path)