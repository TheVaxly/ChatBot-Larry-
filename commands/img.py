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