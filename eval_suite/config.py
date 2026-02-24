from dataclasses import dataclass
from pathlib import Path
import json
import uuid

@dataclass
class EvalFeatureConfig:
    req_dict: dict
    prompt: str 
    prompt_file:str
    eval_prompt: str
    results_path: Path
    evaluation_results_path: Path


def create_eval_config(
    base_dir: Path,
    data_file: str ="starter_dataset.json",
    prompt_file: str = "system.txt",
    eval_prompt_file: str = "evaluation.txt",
) -> EvalFeatureConfig:

    # --- data ---
    req_json = (base_dir / "data" / data_file).read_text(encoding="utf-8")
    req_dict = json.loads(req_json)

    # --- prompts ---
    prompt = (base_dir / "prompts" / prompt_file).read_text(encoding="utf-8")
    eval_prompt = (base_dir / "prompts" / eval_prompt_file).read_text(encoding="utf-8")

    # --- result dirs ---
    results_dir = base_dir / "results"
    results_dir.mkdir(exist_ok=True)

    #create unique id for each evaluation.
    unique_id = uuid.uuid4()
    evaluation_results_dir = base_dir / "evaluation_results"
    evaluation_results_dir.mkdir(exist_ok=True)
    evaluation_results_path = evaluation_results_dir / f"eval_{unique_id}.json"

    return EvalFeatureConfig(
        req_dict=req_dict,
        prompt=prompt,
        prompt_file= prompt_file,
        eval_prompt=eval_prompt,
        results_path=results_dir,
        evaluation_results_path=evaluation_results_path,
    )