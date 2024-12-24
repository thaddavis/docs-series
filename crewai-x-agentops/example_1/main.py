from dotenv import load_dotenv
load_dotenv()
import os
import sys
from crewai import Agent, Task, LLM
from crewai.tools import tool
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException

@tool("markdown_validation_tool")
def markdown_validation_tool(file_path: str) -> str:
    """
    A tool to review files for markdown syntax errors.

    Returns:
    - validation_results: A list of validation results
    and suggestions on how to fix them.
    """

    print("\n\nValidating Markdown syntax...\n\n" + file_path)

    try:
        if not (os.path.exists(file_path)):
            return "Could not validate file. The provided file path does not exist."

        scan_result = PyMarkdownApi().scan_path(file_path.rstrip().lstrip())
        results = str(scan_result)
        return results  # Return the reviewed document
    except PyMarkdownApiException as this_exception:
        print(f"API Exception: {this_exception}", file=sys.stderr)
        return f"API Exception: {str(this_exception)}"
    
ollama_llm=LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

filename = "README.md"

general_agent = Agent(
    role="Requirements Manager",
    goal="""
      Provide a detailed list of the markdown 
      linting results. Give a summary with actionable 
      tasks to address the validation results. Write your 
      response as if you were handing it to a developer 
      to fix the issues.
      DO NOT provide examples of how to fix the issues or
      recommend other tools to use.""",
    backstory="""
      You are an expert business analyst 
			and software QA specialist. You provide high quality, 
      thorough, insightful and actionable feedback via 
      detailed list of changes and actionable tasks.
    """,
    allow_delegation=False,
    verbose=True,
    tools=[markdown_validation_tool],
    llm=ollama_llm,
)

syntax_review_task = Task(
    description=f"""
        Use the markdown_validation_tool to review 
        the file(s) at this path: {filename}
        
        Be sure to pass only the file path to the markdown_validation_tool.
        Use the following format to call the markdown_validation_tool:
        Do I need to use a tool? Yes
        Action: markdown_validation_tool
        Action Input: {filename}

        Get the validation results from the tool 
        and then summarize it into a list of changes
        the developer should make to the document.
        DO NOT recommend ways to update the document.
        DO NOT change any of the content of the document or
        add content to it. It is critical to your task to
        only respond with a list of changes.
        
        If you already know the answer or if you do not need 
        to use a tool, return it as your Final Answer.""",
    agent=general_agent,
    expected_output="A list of validation results and suggestions on how to fix them.",
)

print("\n\nStarting the task...\n\n")
syntax_review_task.execute_sync()
print("\n\nTask completed.\n\n")
