from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
import os
import agentops

AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
agentops.init(AGENTOPS_API_KEY, auto_start_session=False)

client = OpenAI()

try:
    agentops.start_session(tags=["openai-completion"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": "Write a marketing slogan for an almond butter filled chocolate bar called Heaven"
        }]
    )
    print(response.choices[0].message.content)
    agentops.end_session('Success')
except Exception as e:
    agentops.end_session('Fail')