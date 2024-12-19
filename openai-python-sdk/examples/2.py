import os
from openai import AsyncOpenAI
import agentops
import asyncio
from dotenv import load_dotenv
load_dotenv()

AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
agentops.init(AGENTOPS_API_KEY, auto_start_session=False)

async def main():
    client = AsyncOpenAI()

    stream = await client.chat.completions.create(
        model="gpt-4o-mini",
        stream=True,
        messages=[{
            "role": "user",
            "content": "Write a haiku about AI and humans working together"
        }],
    )

    async for chunk in stream:
      print(chunk.choices[0].delta.content or "", end="", flush=True)

try:
    agentops.start_session(tags=["openai-async-completion"])
    asyncio.run(main())
    agentops.end_session('Success')
except Exception as e:
    agentops.end_session('Fail')