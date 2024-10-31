import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1000,
    temperature=0.3,
    system="You are a language teacher. When a user gives you a list of words or expressions in Spanish you respond with a short text of a few sentences using these words or expressions in context. The text must make use of the words or expressions in the form they are given to you by the user. i.e. if the word is an infinitive your response must use it as the infinitive. Make sure to replace the word with a blank (___) in your response.  Don't respond with anything else except the short text.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "\"Bajar del autobus\", \"comer\", \"llamé\""
                }
            ]
        }
    ]
)
print(message.content[0].text)