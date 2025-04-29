from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.agents.llm_agent import Agent
from contextlib import AsyncExitStack
from dotenv import load_dotenv
import os

load_dotenv()

async def get_quasar_tools(exit_stack):
    tools, _ = await MCPToolset.from_server(
        connection_params=StdioServerParameters(
            command=os.getenv("COMMAND"),
            args=[],
            env={
                "BASE_URL": os.getenv("BASE_URL"),
                "GCLOUD_PATH": os.getenv("GCLOUD_PATH"),
            },
            async_exit_stack=exit_stack,
        ),
    )

    return tools

async def create_agent():
    exit_stack = AsyncExitStack()
    quasar_tools = await get_quasar_tools(exit_stack)

    agent = Agent(
        name="quasar_agent",
        model="gemini-2.0-flash",
        description=("Agent to answer questions about the Quantum Computation and Quantum Information."),
        instruction=("You are a helpful agent who can answer user questions about the Quantum Computation and Quantum Information."),
        tools=quasar_tools,
    )

    return agent, exit_stack

root_agent = create_agent()
