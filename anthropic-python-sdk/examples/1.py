from dotenv import load_dotenv
load_dotenv()
from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
scratch_folder = "scratch"
scratch_file = "response.md"

message = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "What is the meaning of life?"
        }]
    )

os.makedirs(scratch_folder, exist_ok=True)
with open(os.path.join(scratch_folder, scratch_file), "w") as file:
  file.write(message.content[0].text)
print(f"Response written to {scratch_folder}/{scratch_file}")