from autogen import ConversableAgent, UserProxyAgent
import agentops
import os
from dotenv import load_dotenv
from IPython.core.error import (
    StdinNotImplementedError,
)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

agentops.init(AGENTOPS_API_KEY, default_tags=["autogen-tool-example"])

print("AgentOps is now running. You can view your session in the link above")

# Define model, openai api key, tags, etc in the agent configuration
config_list = [
    {
        "model": "gpt-4-turbo",
        "api_key": OPENAI_API_KEY,
        "tags": ["agentchat-example", "chat"],
    }
]

# Create the agent that uses the LLM.
assistant = ConversableAgent("agent", llm_config={"config_list": config_list})

# Create the agent that represents the user in the conversation.
user_proxy = UserProxyAgent("user", code_execution_config=False)

# Let the assistant start the conversation.  It will end when the user types "exit".
try:
    assistant.initiate_chat(user_proxy, message="How can I help you today?")
except StdinNotImplementedError:
    # This is only necessary for AgentOps testing automation which is headless and will not have user input
    print("Stdin not implemented. Skipping initiate_chat")
    agentops.end_session("Indeterminate")

# Close your AgentOps session to indicate that it completed.
agentops.end_session("Success")
print("Success! Visit your AgentOps dashboard to see the replay")