import json
##################################################################
# Helper functions
# These are all called by run_eval_suite
##################################################################
def iterator(generate, prompt, reqs):
  # takes system prompt and example request data
  # and calls the generate function for every case in request data
  # returns result of calls in a python dictionary. 
  # returned result includes both original request object and LLM response.
    metaData = reqs["meta"] #get metadata
    req_dict = reqs["data"] #get requests and ignore metadata

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
          **metaData,
          "number_of_cases": len(reqs)
        },
        "data": cases
    }

    return result

def evaluate_iterator(generate, prompt, results):
  metaData = results["meta"]
  cases = results["data"] #get the cases ignore metadata
  
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
    "meta": metaData,
    "data": evaluations,
  }

  return result

def save(data, file_path):
    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)  