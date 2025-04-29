from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv
import os

load_dotenv()

async def get_tools():
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command=os.getenv("COMMAND"),
            args=[],
            env={
                "BASE_URL": os.getenv("BASE_URL"),
                "GCLOUD_PATH": os.getenv("GCLOUD_PATH"),
            },
        ),
    )

    return tools, exit_stack

async def create_agent():
    tools, exit_stack = await get_tools()
    agent = Agent(
        name="quasar_agent",
        model="gemini-2.0-flash",
        description=("Agent to answer questions about the Quantum Computation and Quantum Information."),
        instruction=("You are a helpful agent who can answer user questions about the Quantum Computation and Quantum Information."),
        tools=tools,
    )

    return agent, exit_stack

root_agent = create_agent()
