from fastapi import FastAPI
from pydantic import BaseModel
from crew.zorqk_crew import process_user_query

app = FastAPI(title="🚗 Zorqk Smart Vehicle Assistant API")

class UserQuery(BaseModel):
    query: str

@app.post("/chat")
def chat_with_zorqk(req: UserQuery):
    print(req.query)
    answer = process_user_query(req.query)
    return {"response": answer}
