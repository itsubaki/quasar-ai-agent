from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search, agent_tool
from zoneinfo import ZoneInfo
import datetime

def get_current_time(city: str, time_zone_id: str) -> dict:
    tz = ZoneInfo(time_zone_id)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )

    return {"status": "success", "report": report}

def create_agent():
    quasar_agent = Agent(
        name="quasar_agent",
        model="gemini-2.0-flash",
        description=("Answers user questions about the Quantum Computation and Quantum Information."),
        instruction=("You are a helpful agent who can answer user questions about the Quantum Computation and Quantum Information."),
        tools=[
            MCPToolset(
                connection_params=StreamableHTTPConnectionParams(
                    url="http://127.0.0.1:3000/mcp",
                ),
                tool_filter=[
                    'openqasm3p0_run',
                ]
            )
        ],
    )

    search_agent = Agent(
        name='google_search_agent',
        model='gemini-2.0-flash',
        description=("Answers user questions using Google Search."),
        instruction=("You are a specialist in Google Search"),
        tools=[
            google_search,
        ],
    )

    root_agent = Agent(
        name="root_agent",
        model="gemini-2.0-flash",
        description=("Answers user questions about everything."),
        instruction=("You are a helpful agent who can answer user questions."),
        sub_agents=[
            quasar_agent,
            search_agent,
        ],
        tools=[
            get_current_time,
        ]
    )

    return root_agent

root_agent = create_agent()
