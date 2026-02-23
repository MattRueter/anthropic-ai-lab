import json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from create_gapped_sentences.gapped_sentences import generate_gapped_sentences
from create_gapped_sentences.evaluate_gapped_sentences import evaluate_gapped_sentences
from eval_suite.run_eval_suite import run_eval_suite

#get json file and unpack "example_requests list.
data_file = "single_req.json" # CHANGE THIS TO TEST DIFFERENT SETS OF REQUESTS.
req_json = (Path(__file__).resolve().parent / "data" / data_file).read_text(encoding="utf-8")
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
results_path = results_dir


#results of evaluation saved here
evaluation_results_dir = Path(__file__).parent / "evaluation_results"
evaluation_results_dir.mkdir(exist_ok=True) # create folder on initial run of this script
evaluation_results_path = evaluation_results_dir 



run_eval_suite(
  generate=generate_gapped_sentences,
  prompt=prompt, 
  reqs=req_dict, 
  results_path=results_path,
  evaluate=evaluate_gapped_sentences,
  eval_prompt=eval_prompt,
  evaluation_results_path=evaluation_results_path
 )

