import anthropic
from dotenv import load_dotenv
import json
from pathlib import Path

load_dotenv()

client = anthropic.Anthropic()

req_json = Path("single_req.json").read_text(encoding="utf-8")

prompt_path = Path(__file__).resolve().parent /"system.txt"
prompt = prompt_path.read_text(encoding="utf-8")


def create_gapped_sentences(prompt, req):
  print("make call to LLM with a single prompt and requst-----------------")

  message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    temperature=0,
    system=prompt,
    messages=[
        {
            "role": "user",
            "content": req
        }
    ]
  )
  print(message.content)

create_gapped_sentences(prompt,req_json)

