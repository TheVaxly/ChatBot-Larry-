import openai

OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

def gen(prompt):
    response = openai.Image.create(
        prompt=prompt,
        model="image-alpha-001"
    )
    image_url = response['data'][0]['url']
    return image_url