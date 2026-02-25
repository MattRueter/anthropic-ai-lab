import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

schema = {
    "type": "object",
    "properties": {
        # replace 'response' with properties relevant to use case
        "data": {"type":"string"}
    },
    "required": [],
    "additionalProperties": False,
}


def generate(prompt, req):
    print("Calling Claude")
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        temperature=0.5,
        system=prompt,
        messages=[{"role": "user", "content": req}],
        output_config={
            "format": {"type": "json_schema", "schema": schema},
        }
    )
    return message.content[0].text
