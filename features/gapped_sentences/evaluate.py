import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

schema = {
  "type": "object",
  "properties": {
    "id" : {"type" : "number"},
    "score" : {"type" : "number"},
    "comment" : {"type" : "string"}
  },
  "required" : ["id", "score", "comment"],
  "additionalProperties" : False,
}


def evaluate(prompt, req):

  print("Calling the evaluator.")

  message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    temperature=0.5,
    system= prompt,
    messages=[
        {
            "role": "user",
            "content": req
        }
    ],
    output_config={
      "format": {
        "type": "json_schema",
        "schema": schema,
      },
    }
  )
  return message.content[0].text

