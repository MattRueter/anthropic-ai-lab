import json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from gapped_sentences import generate_gapped_sentences
from evaluate_gapped_sentences import evaluate_gapped_sentences


#get json file and unpack "example_requests list.
data_file = "single_req.json"
req_json = Path("data/"+data_file).read_text(encoding="utf-8")
req_dict = json.loads(req_json)
req_dict = req_dict["example_requests"]


#get system prompt
prompt_file = "system.txt"
prompt_path = Path(__file__).resolve().parent / "prompts" / prompt_file
prompt = prompt_path.read_text(encoding="utf-8")

# evaluation prompt
eval_prompt_file = "evaluation.txt"
eval_prompt_path = Path(__file__).resolve().parent / "prompts" / eval_prompt_file
eval_prompt = eval_prompt_path.read_text(encoding="utf-8")

#results of intitial call saved here
results_dir = Path(__file__).parent / "results"
results_dir.mkdir(exist_ok=True)  # create folder if missing on initial run of this script.
results_path = results_dir / "test.json"



#results of evaluation saved here
evaluation_results_dir = Path(__file__).parent / "evaluation_results"
evaluation_results_dir.mkdir(exist_ok=True) # create folder on initial run of this script
evaluation_results_path = evaluation_results_dir / "test.json"

##################################################################
# Helper functions
# These will eventually be moved into a separate file at root.
##################################################################
def iterator(generate, prompt, reqs):
  # takes system prompt and example request data
  # and calls the generate function for every case in request data
  # returns result of calls in a python dictionary. 
  # returned result includes both original request object and LLM response.

    counter = 0
    cases = []

    for req in reqs:
        case = {
            "id" :counter,
            "request": req,
            "response": {}
        }

        # serialize request for LLM
        req_json = json.dumps(req)

        # call LLM model
        response_str = generate(prompt, req_json)

        # parse structured JSON response
        response_obj = json.loads(response_str)

        case["response"] = response_obj
        cases.append(case)

        counter +=1

    result = {
        "meta": {
            "name": "dev",
            "number_of_requests": len(reqs)
        },
        "cases": cases
    }

    return result

def evaluate_iterator(generate, prompt, reqs):
  results = []
  for req in reqs:
    # serialize request for LLM
    req_json = json.dumps(req)

    # call LLM model
    response_str = generate(prompt, req_json)

    # parse structured JSON response
    response_obj = json.loads(response_str)
    results.append(response_obj)
  
  result = {
    "meta":{
      "score" : 0,
      "number_of_cases" :len(reqs),
    },
    "eval_results": results,
  }

  return result

def save(data, file_path):
    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#########################//////################################




###############################################################
# Main function for running the evaluation. 
###############################################################
def run_eval_suite(
  generate=False, # the func which calls the llm
  prompt=False,  # system prompt for the feature (prompt being evaluated)
  reqs=False,  # original request object as python dict
  results_path=False, # location to save the results
  evaluate=False, # evaluation function calls the LLM to compare req and responses
  eval_prompt=False, # evaluation prompt
  evaluation_results_path=False # location to save evaluation results
  ):

  # Make initial call to LLM with example data
  results = iterator(generate_gapped_sentences, prompt, reqs)
  print(results)
  
  # save results
  save(results, results_path)


  # Evaluate the results.
  results = results["cases"] #get the cases ignore metadata
  evaluation = evaluate_iterator(evaluate_gapped_sentences, eval_prompt, results )

  ##before saving do the following:
  # 1. average score and update evaluation["meta"]["score"]
  # 2. get a overall comment and update evaluation["meta"]["summary"]  
  evals = evaluation["eval_results"]
  scores = []
  for eval in evals:
    scores.append(eval["score"])
  
  score_sum = sum(scores)
  avg = score_sum / len(scores)
  

  evaluation["meta"]["score"] = avg



  # get average score. Call calculate_score (use evaluation_results as args). 
  #  - 
  # write score message and append to file at evaluation_results_path
  
  # save evaluation_results to file (save as json)
  save(evaluation, evaluation_results_path)



run_eval_suite(
  generate=generate_gapped_sentences,
  prompt=prompt, 
  reqs=req_dict, 
  results_path=results_path,
  evaluate=evaluate_gapped_sentences,
  eval_prompt=eval_prompt,
  evaluation_results_path=evaluation_results_path
 )

