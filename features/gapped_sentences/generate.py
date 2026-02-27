import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

schema = {
  "type": "object",
  "properties": {
    "response": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "word": { "type": "string" },
          "answer": { "type": "string" },
          "incorrect_options": {
            "type": "array",
            "items": { "type": "string" }
          },
          "sentence": { "type": "string" }
        },
        "required": ["word", "answer", "sentence"],
        "additionalProperties": False,
      }
    }
  },
  "required": ["response"],
  "additionalProperties": False,
}



def generate(prompt, req):
  # Make a call to LLM with a single prompt and requst.
  print("Calling Claude")

  message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    temperature=0.5,
    system=prompt,
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

