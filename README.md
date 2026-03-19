# AI Prompt Evaluation


## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Developing a New Feature](#developing-a-new-feature)
- [Evaluation & Scoring](#evaluation--scoring)


## Overview

This project is a feature-based prompt evaluation pipeline. It allows you to define use-case-specific features (a feature you may be implementing in another project which requires LLM calls), generate structured JSON outputs from LLMs, and evaluate those outputs against a separate evaluation prompt. The system ensures reproducible, schema-enforced testing of prompts, making it easier to iterate and compare performance across prompts and models.

### Motivation / Why This Exists

Prompt engineering is often ad-hoc and difficult to measure. This project provides a structured workflow for testing, validating, and scoring prompts programmatically. By enforcing JSON schemas and automating evaluation, it allows prompt designers to systematically assess performance, track improvements, and experiment with different models or prompt variations in a repeatable and measurable way.

### High Level View of Flow
1. **INITIAL CALL:** LLM is called with the `prompt` you are evaluating and a list of `data` representing user input.
2. **SAVE RESULTS:** Results are saved as a list of objects representing the original `request` and the LLM `response`.
3. **EVALUATE CALL:** LLM is called with the `evaluation prompt` and the `results`of the original call.
4. **SAVE RESULTS:** Evaluation results are saved as a list of objects each with the request id and the evaluation LLM's comments and score. An average score is also calculated and added to the evaluation result meta data.
5. **HUMAN REVIEW and PROMPT UPDATE:** You can now read the evaluation results and look at strenghts and weakness, compare AI evaluation to specific original requests/responses if you want and adjust the prompt and repeat the evaluation.

## Getting Started

### 1. Clone the Repository
Start by cloning the project repository and navigating into it:

```bash
git clone https://github.com/MattRueter/ai-prompt-evaluation.git
cd ai-prompt-evaluation/
```

### 2. Creating virtual environment
```bash
#from project root
python3 -m venv .venv
source .venv/bin/activate

#install dependencies
pip install -r requirements.txt


#terminate environment when you've finished a session.
deactivate
```

### 3. Add LLM API key to .env
This project uses Anthropic by default. This requires creating an Anthropic account and generating an API key. The .env is loaded into the project and Anthropic's Python SDK automatically looks for a `ANTHROPIC_API_KEY` variable. 
```bash
ANTHROPIC_API_KEY=<your antrhopic api key>
```
The project was designed so that within a feature's `generate.py` and `evaluate.py` files you can swap out different Anthropic models or even differen LLMs. But I haven't tested this just yet. 

The important thing is to make sure the given LLM has access to whatever creditentials are required and that it returns the data following the expected schema. 

### 4. Running a Feature Evaluation
Each feature lives in its own directory with its own `main.py`. You can run a feature in several ways:

From ***project root*** run:

Option 1. Without an alias.
```bash
#run the main.py file passing in the feature directory name
python3 main.py <feature_dir>

#run the main.py file using autocomplete 
python3 main.py features/<features_dir>
```

Option 2. Using an alias (recommended):
```bash
#e.g. the alias I use.
alias evaluate='python3 main.py'

#then run (from the root of the project)
evaluate <feature_dirname>

#OR with autocomplete
evaluate features/<feature_dirname>
```

> In any calling the main.py file in the project root in turn runs the main.py the feature file.

### 5. Running the `get_started` feature
In `features/` there is an example template feature called `get_started`. Try running `evaluate get_started` in the terminal.

You should see this...
```txt
--------------------------------------------------------
🚀 Welcome! Your feature is almost ready.
Please add some example data to '<your_feature_dir>data/starter_dataset.json'
and write your prompts in 'prompts/system.txt' to get started.
--------------------------------------------------------
```



## Developing a New Feature
Let's walk through working on a new feature from scratch.

### 1. Run the following in the CLI
```bash
python3 bootstrap_feature introductions
```
### 2. Add data. 
+ `introductions/data/starter_dataset.json`
```json
  "data": [
    {
      "user": "Hello my name is Matt. Nice to meet you."
    },
    {
      "user" : "I am building my first feature directory."
    }
  ]
```
### 3. Create system and evaluation prompts
+ `introductions/prompts/system.txt`
```
You are a friendly chatbot. If a user introduces themselves by name, respond with the following sentence.

"Hello, I am Claude. Nice to meet you."


If they haven't introduced themselves by name, then just respond with a rhyming couplet.

```
+ `introductions/prompts/evaluation.txt`
```
You are a response grading LLM in a prompte engineering pipeline. Below ar the rules for giving a score to the response you are evaluating.

<RULES FOR SCORING RESPONSES TO INTRODUCTIONS>

If the user has introduced themselves by name and the response isn't EXACTLY "Hello, I am Claude. Nice to meet you.", 
score is automatically 0

If the user has introduced themselves by name and the response is "Hello, I am Claude. Nice to meet you.",
Score is 10

</RULES FOR SCORING RESPONSES TO INTRODUCTIONS>

<RULES FOR SCORING RESPONSES TO NON INTRODUCTIONS>

If the user hasn't introduced themselves and ther response is anything else besides a rhyming couplet, 
score is automatically 0.

If response is couplet but doesn't rhyme , 
score is 5

</RULES FOR SCORING RESPONSES TO NON INTRODUCTIONS>

```

### 4. Run initial evaluation
```bash
#from root of project run
python3 main.py introductions
```
### 5. View results
+ open up the `introductions/evaluation_results` directory and there should be a file with a uuid. Open it to see the results of the evaluation and average scroe.
+ you can also view the original requests/responses in `introductions/results/`


## Output Schema
You may want output to be something other then a string. You can enforce this by updating the schema used for the generate call.
+ `<feature>/generate.py`
```python
schema = {
    "type": "object",
    "properties": {
        # replace object assigned to "llm" with properties relevant to use case
        "llm": {"type":"string"} #update this to match the output you expect.
    },
    "required": [],
    "additionalProperties": False,
}

```

## Adding Differnet Datasets and Prompt versions
The config found in /config.py uses `data/starter_dataset.json` , `prompts/system.txt` and `prompts/evaluation.txt` by default. You can overide these by changing the config in `<your_feature>/main.py`

e.g.
```python
#features/<your_feature>/main.py

config = create_eval_config(
    base_dir=Path(__file__).resolve().parent,
    data_file = "dataset_v2.json",
    prompt_file = "system_v2.txt",
    eval_prompt_file = "evaluation_v2.txt", # !This is not yet being saved in the meta data.
)
```

The meta data in your output will now include those file names for easier reference, searching, filtering etc.

```json
  "meta": {
    "file_name": "dataset_v2.json",
    "dataset_name": "dataset_v2.json",
    "prompt_file_name": "system_v2.txt",
    "number_of_cases": null,
    "average_score":null,
    "summary": "",
    "description": "Simple set of requests to test and build pipeline"
  }
```

> 📘Good to know:
>
> You may only ever want to use one dataset file and one system.txt file but the project supports 
> various dataset and prompt files for granularity.

## Future updates
Some things I'd like to add eventually:
+ sorting/filtering cli commands for better reviewing the results
+ open up a browser window to view results (with and without sorting/filtering)
+ create a package or make easier to "drop in" a workplace (so users don't have to store prompt and LLM config in two separte places). This would be nice as the prompt-eval-pipeline can live next to the project which has all of the features using LLM calls that require the testing.