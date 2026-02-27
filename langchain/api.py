
from fastapi import FastAPI
from pydantic import BaseModel
from main import agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://localhost",  
    "http://127.0.0.1",
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(query: Query):
    try:
        response = agent.run(query.question)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}