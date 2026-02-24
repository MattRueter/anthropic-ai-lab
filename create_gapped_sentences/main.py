import json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from create_gapped_sentences.gapped_sentences import generate_gapped_sentences
from create_gapped_sentences.evaluate_gapped_sentences import evaluate_gapped_sentences
from eval_suite.run_eval_suite import run_eval_suite
from eval_suite.config import create_eval_config

config = create_eval_config(
    base_dir=Path(__file__).resolve().parent,
    # data_file: str = #defaults to --> "starter_dataset.json",
    # prompt_file: str = #defaults to --> "system.txt",
    # eval_prompt_file: str = #defaults to --> "evaluation.txt",
)

run_eval_suite(
  generate=generate_gapped_sentences,
  prompt=config.prompt,
  prompt_file=config.prompt_file,
  reqs=config.req_dict, 
  results_path=config.results_path,
  evaluate=evaluate_gapped_sentences,
  eval_prompt=config.eval_prompt,
  evaluation_results_path=config.evaluation_results_path
 )

