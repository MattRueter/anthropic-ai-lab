import json
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path

from features.keyword_transformations.generate import generate_keyword_transformation
from features.keyword_transformations.evaluate import evaluate_keyword_transformation

from eval_suite.run_eval_suite import run_eval_suite
from config import create_eval_config


config = create_eval_config(
    base_dir=Path(__file__).resolve().parent,
    data_file="starter_dataset.json",
)

run_eval_suite(
  generate=generate_keyword_transformation,
  evaluate=evaluate_keyword_transformation,
  config=config

 )

