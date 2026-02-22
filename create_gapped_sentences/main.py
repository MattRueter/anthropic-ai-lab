import json
from pprint import pprint
from pathlib import Path
from gapped_sentences import generate_gapped_sentences

#get json file and unpack "example_requests list.
req_json = Path("single_req.json").read_text(encoding="utf-8")
req_json = json.loads(req_json)
req_json = req_json["example_requests"]


#get system prompt
prompt_path = Path(__file__).resolve().parent /"system.txt"
prompt = prompt_path.read_text(encoding="utf-8")



##################################################################
## Write helper functions here and then move to root. ----------------------------------------

import json

def iterator(generate, prompt, reqs):
    cases = []

    for req in reqs:
        case = {
            "request": req,
            "response": {}
        }

        # serialize request for LLM
        req_json = json.dumps(req)

        # call model
        response_str = generate(prompt, req_json)

        # parse structured JSON response
        response_obj = json.loads(response_str)

        case["response"] = response_obj
        cases.append(case)

    result = {
        "meta": {
            "name": "dev",
            "number_of_requests": len(reqs)
        },
        "cases": cases
    }

    return result

def save(data, filename):
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)  # create folder if missing

    file_path = results_dir / filename

    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

###################################################################





# generation function
def run_eval_suite(
  generate=False, 
  prompt=False, 
  req=False, 
  results_path=False, 
  evaluate=False, 
  eval_prompt=False, 
  evaluation_results_path=False
  ):

  # call iterator and call generate on each iteration (use prompt, and req as args)
  # e.g. results = iterator(generate, prompt, req)
  results = iterator(generate_gapped_sentences, prompt, req_json)
  print(results)
  

  # save results to file (save as json)
  save(results, "test.json")


  # call evaluate_iterator and call evaluate on each iteration (use evaluate, eval_prompt, and results as args )
  # evaluation_results = evaluate_iterator(evaluate, eval_prompt, results)

  # save evaluation_results to file (save as json)
  # e.g. save(evaluation_results_path)

  # get average score. Call calculate_score (use evaluation_results as args). 
  # write score message and append to file at evaluation_results_path



run_eval_suite(prompt=prompt, req=req_json)

