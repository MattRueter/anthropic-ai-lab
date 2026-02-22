import json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from gapped_sentences import generate_gapped_sentences
from evaluate_gapped_sentences import evaluate_gapped_sentences


#get json file and unpack "example_requests list.
data_file = "single_req.json"
req_json = Path("data/"+data_file).read_text(encoding="utf-8")
req_json = json.loads(req_json)
req_json = req_json["example_requests"]


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
  # returns result of calls in a python dictionary
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
      "score" : 0, #will be averaged later on.
      "number_of_cases" :len(reqs),
    },
    "results": results,
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
  generate=False, #the func which calls the llm
  prompt=False,  #system prompt for the feature
  req=False,  # request object
  results_path=False, 
  evaluate=False, 
  eval_prompt=False, 
  evaluation_results_path=False
  ):

  # call iterator and call generate on each iteration (use prompt, and req as args)
  results = iterator(generate_gapped_sentences, prompt, req_json)
  print(results)
  
  # save results to file (save as json)
  save(results, results_path)


  # call evaluate_iterator and call evaluate on each iteration (use evaluate, eval_prompt, and results as args )
  reqs_json = results["cases"] #get the cases ignore metadata
  evaluation = evaluate_iterator(evaluate_gapped_sentences, eval_prompt, reqs_json )

  # save evaluation_results to file (save as json)
  save(evaluation, evaluation_results_path)

  # get average score. Call calculate_score (use evaluation_results as args). 
  # write score message and append to file at evaluation_results_path



run_eval_suite(
  generate=generate_gapped_sentences,
  prompt=prompt, 
  req=req_json, 
  results_path=results_path,
  evaluate=evaluate_gapped_sentences,
  eval_prompt=eval_prompt,
  evaluation_results_path=evaluation_results_path
  )

