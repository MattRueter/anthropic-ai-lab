import json
from pprint import pprint
from pathlib import Path
from gapped_sentences import generate_gapped_sentences

#get json file and unpack "example_requests list.
req_json = Path("single_req.json").read_text(encoding="utf-8")
req_json = json.loads(req_json)
req_json = req_json["example_requests"]
#req_json = json.dumps(req_json)


#get system prompt
prompt_path = Path(__file__).resolve().parent /"system.txt"
prompt = prompt_path.read_text(encoding="utf-8")




##################################################################
## Write helper functions here and then move to root. ----------------------------------------

def iterator(generate, prompt, reqs):
  results = []

  for req in reqs:
    
    #serialize as json for request to LLM
    req = json.dumps(req)
    response = generate(prompt, req)

    #turn back into python list
    result = json.loads(response)
    
    results.append(response)
  return results


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
  # e.g. save(results_path)

  # call evaluate_iterator and call evaluate on each iteration (use evaluate, eval_prompt, and results as args )
  # evaluation_results = evaluate_iterator(evaluate, eval_prompt, results)

  # save evaluation_results to file (save as json)
  # e.g. save(evaluation_results_path)

  # get average score. Call calculate_score (use evaluation_results as args). 
  # write score message and append to file at evaluation_results_path



run_eval_suite(prompt=prompt, req=req_json)

