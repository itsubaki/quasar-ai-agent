from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.agents.llm_agent import Agent
from contextlib import AsyncExitStack
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os
import datetime

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

def get_current_time(city: str, time_zone_id: str) -> dict:
    tz = ZoneInfo(time_zone_id)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )

    return {"status": "success", "report": report}

async def create_agent():
    exit_stack = AsyncExitStack()
    quasar_tools = await get_quasar_tools(exit_stack)

    agent = Agent(
        name="quasar_agent",
        model="gemini-2.0-flash",
        description=("Agent to answer questions about the Quantum Computation and Quantum Information."),
        instruction=("You are a helpful agent who can answer user questions about the Quantum Computation and Quantum Information."),
        tools=[
            *quasar_tools,
            get_current_time,
        ],
    )

    return agent, exit_stack

root_agent = create_agent()
