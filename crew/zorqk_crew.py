# crew/zorqk_crew.py
from crewai import Agent, Crew, Task
from agents.chat_agent import ChatAgent

# Initialize our real orchestrator
chat_agent = ChatAgent()

# Define CrewAI Agents (conceptual roles for orchestration)
data_agent = Agent(
    role="Vehicle Data Agent",
    goal="Retrieve vehicle information from MongoDB and return structured data.",
    backstory="You look up vehicle records by registration, make, or model."
)

spec_agent = Agent(
    role="Specification Agent",
    goal="Extract and explain vehicle specs like battery size or motor power.",
    backstory="You are an expert in EV and car specifications."
)

mot_agent = Agent(
    role="MOT Agent",
    goal="Handle questions about MOT, tax, and compliance.",
    backstory="You are an expert in MOT and DVLA compliance information."
)

insight_agent = Agent(
    role="Insight Agent",
    goal="Summarize data into clear, conversational insights.",
    backstory="You craft user-friendly summaries from raw data."
)

# Assemble the Crew
zorqk_crew = Crew(
    agents=[data_agent, spec_agent, mot_agent, insight_agent],
    name="ZorqkCrew",
    goal="Collaboratively answer vehicle-related queries using structured data."
)

# Define a Task (CrewAI format)
answer_vehicle_query = Task(
    description="Answer user questions about vehicles using MongoDB and ChromaDB data.",
    expected_output="A conversational answer about the requested vehicle(s).",
    agent=insight_agent,
)

# Main entry point used by FastAPI or Gradio
def process_user_query(query: str) -> str:
    """
    Main entry point for handling user queries via CrewAI orchestration.
    Uses our ChatAgent to perform logic under the hood.
    """
    return chat_agent.handle_query(query)
