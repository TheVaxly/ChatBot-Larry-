import openai
import os

openai.api_key = "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"

input_text = input("Enter some text: ")

if os.path.exists("conversation_history.txt"):
    with open("conversation_history.txt", "r") as f:
        conversation_history = f.read()
else:
    conversation_history = ""

output = openai.Completion.create(
    engine="text-davinci-002",
    prompt=(conversation_history + input_text),
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

print(output.choices[0].text.strip())

with open("conversation_history.txt", "w") as f:
    f.write(conversation_history + input_text + output.choices[0].text)