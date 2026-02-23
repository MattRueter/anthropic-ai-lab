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
results_path = results_dir / "response.json"


#results of evaluation saved here
evaluation_results_dir = Path(__file__).parent / "evaluation_results"
evaluation_results_dir.mkdir(exist_ok=True) # create folder on initial run of this script
evaluation_results_path = evaluation_results_dir / "evaluation.json"

##################################################################
# Helper functions
# These will eventually be moved into a separate file at root.
##################################################################
def iterator(generate, prompt, reqs):
  # takes system prompt and example request data
  # and calls the generate function for every case in request data
  # returns result of calls in a python dictionary. 
  # returned result includes both original request object and LLM response.
    req_dict = reqs["example_requests"] #get requests and ignore metadata
    counter = 0
    cases = []

    for req in req_dict:
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
            "dataset_name": reqs["meta"]["dataset_name"],
            "number_of_requests": len(reqs)
        },
        "cases": cases
    }

    return result

def evaluate_iterator(generate, prompt, results):
  cases = results["cases"] #get the cases ignore metadata
  evaluations = []
  for case in cases:
    # serialize request for LLM
    case_json = json.dumps(case)

    # call LLM model
    response_str = generate(prompt, case_json)

    # parse structured JSON response
    response_obj = json.loads(response_str)
    evaluations.append(response_obj)
  
  result = {
    "meta":{
      "dataset_name": results["meta"]["dataset_name"],
      "score" : 0,
      "number_of_cases" :len(cases),
    },
    "eval_results": evaluations,
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
  generate, # the func which calls the llm
  prompt,  # system prompt for the feature (prompt being evaluated)
  reqs,  # original request object as python dict
  results_path, # location to save the results
  evaluate, # evaluation function calls the LLM to compare req and responses
  eval_prompt, # evaluation prompt
  evaluation_results_path # location to save evaluation results
  ):

  # Make initial call to LLM with example data
  results = iterator(generate, prompt, reqs)
  
  # save results
  save(results, results_path)


  # Evaluate the results.
  evaluation = evaluate_iterator(evaluate, eval_prompt, results )

  ##before saving average the scores of the evaluation
  evals = evaluation["eval_results"]
  scores = []

  for eval in evals:
    scores.append(eval["score"])
  
  score_sum = sum(scores)
  avg = score_sum / len(scores)
  evaluation["meta"]["score"] = avg #update the metadata with the average score.
  
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

