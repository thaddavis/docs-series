import agentops
import os
from typing import Annotated, Literal
from autogen import ConversableAgent, config_list_from_json, register_function
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

agentops.init(AGENTOPS_API_KEY, default_tags=["autogen-tool-example"])

Operator = Literal["+", "-", "*", "/"]

def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

# Create the agent that uses the LLM.
assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple calculations. "
    "Return 'TERMINATE' when the task is done.",
    llm_config={"config_list": config_list},
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# assistant.register_for_llm(name="calculator", description="A simple calculator")(calculator)
# user_proxy.register_for_execution(name="calculator")(calculator)

# Register the calculator function to the two agents.
# register_function(
#     calculator,
#     caller=assistant,  # The assistant agent can suggest calls to the calculator.
#     executor=user_proxy,  # The user proxy agent can execute the calculator calls.
#     name="calculator",  # By default, the function name is used as the tool name.
#     description="A simple calculator",  # A description of the tool.
# )

# Let the assistant start the conversation.  It will end when the user types "exit".
user_proxy.initiate_chat(assistant, message="What is (1423 - 123) / 3 + (32 + 23) * 5?")

agentops.end_session("Success")