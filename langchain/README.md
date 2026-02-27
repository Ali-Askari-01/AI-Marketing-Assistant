
# AI Agent with Web Search and API Integration

This project demonstrates how to create a simple AI Agent using LangChain, integrate it with search tools like SerpAPI, and expose it via a FastAPI endpoint.

---

## 🔧 Setup and Agent Creation

### 1. Clone or Create Your Project Directory

```bash
mkdir langchain-agent-app
cd langchain-agent-app
```

### 2. (Optional but Recommended) Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

> **requirements.txt**
```
fastapi
uvicorn
langchain
langchain-community
langchain-openai
python-dotenv
google-search-results
```

---

## Agent Script (main.py)

This script sets up the LangChain agent to answer questions about current events using SerpAPI and OpenAI.

```python
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType

load_dotenv()

llm = OpenAI(temperature=0)

search = SerpAPIWrapper()

tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for answering trending topics or current events"
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_agent(query: str):
    return agent.run(query)
```

---

## Run in Terminal

```bash
python main.py
```

(If you modify `main.py` to run a query directly)

---

## FastAPI Integration

Create a file named `api.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryInput(BaseModel):
    query: str

@app.post("/ask")
def ask_question(query: QueryInput):
    response = run_agent(query.query)
    return {"response": response}
```

---

## ▶️ Run the FastAPI Server

```bash
uvicorn api:app --reload
```

Now you can POST to `http://127.0.0.1:8000/ask` using a tool like Postman or a frontend app.

---

## Example cURL Request

```bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d "{"query": "What's trending in AI today?"}"
```

---

## Extend This Agent

- Save results to a `.txt` or `.csv`
- Push data into an Excel spreadsheet
- Build a front-end dashboard
- Schedule it to run daily (cron job)
- Summarize top tech news weekly via email

---

## 📁 License

MIT License