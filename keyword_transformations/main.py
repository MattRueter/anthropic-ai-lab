import json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path

from keyword_transformations.generate import generate_keyword_transformation
from keyword_transformations.evaluate import evaluate_keyword_transformation

from eval_suite.run_eval_suite import run_eval_suite
from config import create_eval_config


config = create_eval_config(
    base_dir=Path(__file__).resolve().parent,
    data_file="starter_dataset.json",
)

# TODO decide how best to...
# ...unpack variables.
req_dict = config.req_dict
prompt = config.prompt
eval_prompt = config.eval_prompt
results_path = config.results_path
evaluation_results_path = config.evaluation_results_path

run_eval_suite(
  generate=generate_keyword_transformation,
  prompt=prompt, 
  reqs=req_dict, 
  results_path=results_path,
  evaluate=evaluate_keyword_transformation,
  eval_prompt=eval_prompt,
  evaluation_results_path=evaluation_results_path
 )

