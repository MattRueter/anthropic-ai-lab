import json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from create_gapped_sentences.gapped_sentences import generate_gapped_sentences
from create_gapped_sentences.evaluate_gapped_sentences import evaluate_gapped_sentences
from eval_suite.run_eval_suite import run_eval_suite
from eval_suite.config import create_eval_config

prompt_file = "system_v2.txt"
config = create_eval_config(
    base_dir=Path(__file__).resolve().parent,
    prompt_file = prompt_file
)

# TODO decide how best to...
# ...unpack variables.
req_dict = config.req_dict
prompt = config.prompt
eval_prompt = config.eval_prompt
results_path = config.results_path
evaluation_results_path = config.evaluation_results_path


run_eval_suite(
  generate=generate_gapped_sentences,
  prompt=prompt,
  prompt_file=prompt_file,
  reqs=req_dict, 
  results_path=results_path,
  evaluate=evaluate_gapped_sentences,
  eval_prompt=eval_prompt,
  evaluation_results_path=evaluation_results_path
 )

