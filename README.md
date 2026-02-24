# Anthropic-ai-prompt-evaluation
A prompt evaluation pipeline for evaluating AI prompts.

## Creating virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Running the environment
source .venv/bin/activate`` 

## Running a feature evaluation
Two options
1. From root run:
```
python3 -m <feature_dir>.main
```

2. or create an alias:
```bash
#e.g.
alias eval='python3 main.py'

#then from the root of the project run
eval <feature_dirname>

# This runs main.py in root of project 
# which runs the main.py file from the directory name.
```
