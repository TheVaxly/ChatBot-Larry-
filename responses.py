import openai

DISCORD_TOKEN = "MTA4NjI4MDYzMzk3MTY1MDY0MQ.GYTMQC.zYSAX0XnPWTQV6dqChNmWXG6pfpVX4p9O4dpmk"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

def send_responses(prompt):
    response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )

    bot_response = response.choices[0].text.strip()
    return bot_response