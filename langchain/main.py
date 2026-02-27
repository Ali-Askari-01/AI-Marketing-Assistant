from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType


load_dotenv()

llm = OpenAI(temperature=0)
search = SerpAPIWrapper()

search = SerpAPIWrapper()

def safe_search(query):
    full_result = search.run(query)
    return full_result[:2500] 
tools = [
    Tool(
        name="Search",
        func=safe_search,
        description="Useful for answering trending topics or current events"
    )
]


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# query = input("Ask me anything: ")
# response = agent.run(query)
# print("\n Agent Response:\n", response)

def ask_agent(question: str) -> str:
    return agent.run(question)