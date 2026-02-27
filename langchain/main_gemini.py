"""
AI Agent using Google Gemini and LangChain
This agent can answer marketing questions and provide insights
"""

from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

# Load environment variables
load_dotenv()

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Mock search tool for demo (replace with SerpAPIWrapper if you have API key)
class MockSearch:
    def run(self, query: str) -> str:
        """Mock search for demo - returns simulated marketing insights"""
        marketing_responses = {
            "social media": "Top social media trends: Short-form video content (TikTok, Reels), AI-generated content, personalized messaging, influencer partnerships, and community building.",
            "content": "Content marketing trends: Interactive content, video storytelling, user-generated content, AI-assisted writing, and multi-platform distribution.",
            "seo": "SEO best practices: Mobile-first indexing, Core Web Vitals, E-A-T (Expertise, Authority, Trust), semantic search optimization, and voice search optimization.",
            "email": "Email marketing trends: Hyper-personalization, AI-driven segmentation, interactive emails, mobile optimization, and privacy-focused strategies.",
            "trends": "Current marketing trends: AI and automation, personalization at scale, sustainability messaging, voice and visual search, and omnichannel experiences."
        }
        
        # Simple keyword matching for demo
        for keyword, response in marketing_responses.items():
            if keyword in query.lower():
                return response
        
        return f"Based on current market analysis, here are insights for '{query}': Focus on data-driven strategies, customer-centric content, and emerging technologies like AI to stay competitive."

search = MockSearch()

def safe_search(query: str) -> str:
    """Safe wrapper for search function"""
    try:
        full_result = search.run(query)
        return full_result[:2500]
    except Exception as e:
        return f"Search unavailable: {str(e)}"

# Define tools for the agent
tools = [
    Tool(
        name="MarketingInsights",
        func=safe_search,
        description="Useful for getting current marketing trends, social media insights, content strategies, and industry best practices"
    )
]

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

def ask_agent(question: str) -> str:
    """
    Main function to ask the AI agent a question
    
    Args:
        question: The question to ask the agent
        
    Returns:
        Agent's response as a string
    """
    try:
        response = agent.run(question)
        return response
    except Exception as e:
        return f"Agent Error: {str(e)}"

# Test function
if __name__ == "__main__":
    print("🤖 Gemini AI Agent Initialized!")
    print("=" * 50)
    
    test_questions = [
        "What are the top social media trends for 2026?",
        "How can I improve my email marketing campaigns?",
        "What content strategy should I use for Instagram?"
    ]
    
    for question in test_questions:
        print(f"\n📝 Question: {question}")
        print(f"💡 Answer: {ask_agent(question)}")
        print("-" * 50)
