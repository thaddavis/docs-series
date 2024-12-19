import os
from openai import OpenAI
from dotenv import load_dotenv
import agentops
from dotenv import load_dotenv
load_dotenv()

AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
agentops.init(AGENTOPS_API_KEY, auto_start_session=False)

client = OpenAI()

prompts = [
  "Write a 4 line poem about ponies.",
  "What is the capital of the United States?",
]

agentops.start_session(tags=["openai-loop-example"])

for prompt in prompts:
  print(f"PROMPT: {prompt}")

  try:
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        stream=True,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
  except Exception as e:
    pass

  for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)

  print('\n')

agentops.end_session('Success')