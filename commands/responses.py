import openai
import os

OPENAI_API_KEY = os.getenv("ask")

openai.api_key = OPENAI_API_KEY

def send_responses(prompt):
    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )

    bot_response = response.choices[0].text.strip()
    return bot_response