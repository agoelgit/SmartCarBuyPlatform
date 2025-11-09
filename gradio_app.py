import gradio as gr
from crew.zorqk_crew import process_user_query

def gradio_interface(message, history):
    response = process_user_query(message)
    history = history or []
    history.append(("You", message))
    history.append(("Zorqk", response))
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    message = gr.Textbox(label="Ask a question")
    submit = gr.Button("Send")
    submit.click(fn=gradio_interface, inputs=[message, chatbot], outputs=[chatbot, chatbot])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
