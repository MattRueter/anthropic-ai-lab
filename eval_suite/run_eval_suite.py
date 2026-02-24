from .eval_helpers import *

def run_eval_suite(
  generate, # the func which calls the llm (func being evalutated). Resturns results json.
  evaluate, # evaluation function calls the LLM to compare req and responses. Returns evaluation json
  config
  ):
  
  # Make initial call to LLM with example data
  results = iterator(generate, config.prompt, config.prompt_file, config.dataset)
  
  # save results
  save(results, config.results_path)

  # Evaluate the results.
  evaluation = evaluate_iterator(evaluate, config.eval_prompt, results )

  ##before saving average the scores of the evaluation
  evaluation["meta"]["average_score"] = calculate_avg(evaluation)
  
  # save evaluation_results to file (save as json)
  save(evaluation, config.evaluation_results_path)