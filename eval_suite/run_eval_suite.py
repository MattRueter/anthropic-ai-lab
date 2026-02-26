from .eval_helpers import *

def run_eval_suite(
  generate, # the func which calls the llm (func being evalutated). Resturns results json.
  evaluate, # evaluation function calls the LLM to compare req and responses. Returns evaluation json
  config
  ):
  #Check example data has been created
  data = config.dataset["data"]
  if len(data) == 0 or (len(data) > 0 and data[0]["user"] == "remind me to create some data."):
    print(
      "--------------------------------------------------------\n"
      "🚀 Welcome! Your feature is almost ready.\n"
      "Please add some example data to '<your_feature_dir>data/starter_dataset.json' \n"
      "and write your prompts in 'prompts/system.txt' to get started.\n"
      "--------------------------------------------------------"
    )
    return

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