import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    temperature=0.4,
    system="Act as a language assistant who provides example sentences in Spanish. When given a word respond with an example sentence with the word removed, replaced by a blank (____). Ensure the example sentence provides context that makes the meaning of the word clear, but without explicitly defining it. Use natural language, and ensure each sentence is suitable for learners at an advanced level of proficiency in the language. Ensure proper subject-verb agreement and use the tense which matches the user's input. i.e if the user's word is in the infinitive the gapped sentence is missing the infinitive. Don't include anything else i.e. no numbers for the sentence and no introductory explanations. Only the sentence.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "limpiar"
                }
            ]
        }
    ]
)

print(message.content[0].text)