import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()


def generate_gapped_sentences(prompt, req):
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
    ]
  )
  return message.content[0].text


