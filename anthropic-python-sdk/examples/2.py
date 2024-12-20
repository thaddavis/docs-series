from dotenv import load_dotenv
load_dotenv()
import asyncio
from anthropic import AsyncAnthropic
import os

client = AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

async def main() -> None:
    stream = await client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": "What is the meaning of life?"
            }],
            stream=True
        )
    content_accum = ""
    async for event in stream:
        if (event.type == "message_start"):
            pass
        elif (event.type == "message_delta"):
            pass
        elif (event.type == "content_block_start"):
            pass
        elif (event.type == "content_block_delta"):
            if event.delta.type == "text_delta":
                content_accum += event.delta.text
                print(event.delta.text, end="", flush=True)
            else:
                pass
        elif (event.type == "content_block_stop"):
            pass
        elif (event.type == "message_stop"):
            pass
        elif (event.type == "stream_stop"):
            pass        
        else:
            print("Unknown event type")
            pass

asyncio.run(main())
