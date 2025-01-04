import os
from dotenv import load_dotenv
import autogen
import agentops
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

agentops.init(AGENTOPS_API_KEY, default_tags=["autogen-tool-example"])

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": {
            "gpt-4o",
        }
    },
)

# 1. create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "timeout": 600,
        "seed": 42,
        "config_list": config_list,
    },
)

# 2. create the MathUserProxyAgent instance named "mathproxyagent"
# By default, the human_input_mode is "NEVER", which means the agent will not ask for human input.
mathproxyagent = MathUserProxyAgent(
    name="mathproxyagent",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
)

# given a math problem, we use the mathproxyagent to generate a prompt to be sent to the assistant as the initial message.
# the assistant receives the message and generates a response. The response will be sent back to the mathproxyagent for processing.
# The conversation continues until the termination condition is met, in MathChat, the termination condition is the detect of "\boxed{}" in the response.
math_problem = (
    "Find all $x$ that satisfy the inequality $(2x+10)(x+3)<(3x+9)(x+8)$. Express your answer in interval notation."
)

# We call `initiate_chat` to start the conversation.
# When setting `message=mathproxyagent.message_generator`, you need to pass in the problem through the `problem` parameter.
mathproxyagent.initiate_chat(assistant, message=mathproxyagent.message_generator, problem=math_problem)

agentops.end_session("Success")