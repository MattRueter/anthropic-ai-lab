import json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from gapped_sentences.gapped_sentences import generate_gapped_sentences
from gapped_sentences.evaluate_gapped_sentences import evaluate_gapped_sentences
from eval_suite.run_eval_suite import run_eval_suite
from config import create_eval_config

config = create_eval_config(
    base_dir=Path(__file__).resolve().parent,
    # data_file: str = #defaults to --> "starter_dataset.json",
    # prompt_file: str = #defaults to --> "system.txt",
    # eval_prompt_file: str = #defaults to --> "evaluation.txt",
)

run_eval_suite(
  generate=generate_gapped_sentences,
  evaluate=evaluate_gapped_sentences,
  config=config
 )

