import openai

OPENAI_API_KEY = "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"

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

def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        model="image-alpha-001"
    )
    image_url = response['data'][0]['url']
    return image_url