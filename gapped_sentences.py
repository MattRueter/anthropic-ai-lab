import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=300,
    temperature=0.4,
    system="Act as a language assistant who provides example sentences in Spanish. When given a word and the language it is in, return an example sentence with the word removed, replaced by a blank (____). Ensure the example sentence provides context that makes the meaning of the word clear, but without explicitly defining it. Use natural language, and ensure each sentence is suitable for learners at an intermediate level of proficiency in the language.  Don't include anything else i.e. no numbers for the sentence and no introductory explanations. Only the sentence.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "arrancar"
                }
            ]
        }
    ]
)
print(message.content[0].text)