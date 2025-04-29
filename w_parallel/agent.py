from google.adk.agents.parallel_agent import ParallelAgent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

APP_NAME = "parallel_research_app"
USER_ID = "research_user_01"
SESSION_ID = "parallel_research_session_with_merge"

researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model="gemini-2.0-flash",
    description="Researches renewable energy sources.",
    instruction="""You are an AI Research Assistant specializing in energy.
Research the latest advancements in 'renewable energy sources'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    tools=[google_search],
    output_key="renewable_energy_result"
)

researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model="gemini-2.0-flash",
    description="Researches electric vehicle technology.",
    instruction="""You are an AI Research Assistant specializing in transportation.
Research the latest developments in 'electric vehicle technology'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    tools=[google_search],
    output_key="ev_technology_result"
)

researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model="gemini-2.0-flash",
    description="Researches carbon capture methods.",
    instruction="""You are an AI Research Assistant specializing in climate solutions.
Research the current state of 'carbon capture methods'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    tools=[google_search],
    output_key="carbon_capture_result"
)

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    description="Runs multiple research agents in parallel to gather information.",
    sub_agents=[
        researcher_agent_1,
        researcher_agent_2,
        researcher_agent_3,
    ],
)

merger_agent = LlmAgent(
    name="SynthesisAgent",
    model="gemini-2.0-flash",
    description="Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs.",
    instruction="""You are an AI Assistant responsible for combining research findings into a structured report.

Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas. Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.

**Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

**Input Summaries:**

*   **Renewable Energy:**
    {renewable_energy_result}

*   **Electric Vehicles:**
    {ev_technology_result}

*   **Carbon Capture:**
    {carbon_capture_result}

**Output Format:**

## Summary of Recent Sustainable Technology Advancements

### Renewable Energy Findings
(Based on RenewableEnergyResearcher's findings)
[Synthesize and elaborate *only* on the renewable energy input summary provided above.]

### Electric Vehicle Findings
(Based on EVResearcher's findings)
[Synthesize and elaborate *only* on the EV input summary provided above.]

### Carbon Capture Findings
(Based on CarbonCaptureResearcher's findings)
[Synthesize and elaborate *only* on the carbon capture input summary provided above.]

### Overall Conclusion
[Provide a brief (1-2 sentence) concluding statement that connects *only* the findings presented above.]

Output *only* the structured report following this format. Do not include introductory or concluding phrases outside this structure, and strictly adhere to using only the provided input summary content.
""",
)

sequential_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    description="Coordinates parallel research and synthesizes the results.",
    sub_agents=[
        parallel_research_agent,
        merger_agent,
    ],
)

root_agent = sequential_pipeline_agent
