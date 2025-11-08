# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from crew.zorqk_crew import process_user_query
import gradio as gr
import threading
import uvicorn

# ---------- FastAPI Setup ----------
app = FastAPI(title="🚗 Zorqk Smart Vehicle Assistant API")

class UserQuery(BaseModel):
    query: str

@app.post("/chat")
def chat_with_zorqk(req: UserQuery):
    answer = process_user_query(req.query)
    return {"response": answer}

# ---------- Gradio Setup ----------
chat_history = []

def gradio_interface(message, history):
    """Handle a single user message"""
    response = process_user_query(message)
    history = history or []
    history.append(("You", message))
    history.append(("Zorqk", response))
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    message = gr.Textbox(label="Ask a question")
    submit = gr.Button("Send")
    
    submit.click(
        fn=gradio_interface,
        inputs=[message, chatbot],
        outputs=[chatbot, chatbot]
    )

# ---------- Run both together ----------
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_gradio():
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

if __name__ == "__main__":
    threading.Thread(target=run_fastapi, daemon=True).start()
    run_gradio()
