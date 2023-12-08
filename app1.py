from openai import OpenAI
import gradio as gr
from flask import Flask, render_template_string

app = Flask(__name__)

client = OpenAI(api_key="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")

messagesList = [{"role": "system", "content": "BVRaju, your Virtual Assistant"}]

def CustomChatGPT(user_input):
    messagesList.append({"role": "user", "content": user_input})
    
    chat_completion = client.chat.completions.create(
        messages= messagesList,
        model="gpt-3.5-turbo",
    )

    answer = chat_completion.choices[0].message.content
    messagesList.append({"role": "assistant", "content": answer})
    return answer

gradioUI = gr.Interface(fn=CustomChatGPT, inputs = [gr.Textbox(label="Ask Your Question:")], 
                    outputs = [gr.Textbox(label="My Answer:")], 
                    title = "BVRaju, your Virtual Assistant<br/> Ask me any Question", 
                    allow_flagging="never", theme = 'gradio/soft')

@app.route("/")
def home():
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gradio + Flask Integration</title>
        <script src="https://cdn.jsdelivr.net/npm/@gradio/core/dist/gradio.min.js"></script>
    </head>
    <body>
        <h1>Welcome to Gradio + Flask Integration</h1>
        {{ iface }}
    </body>
    </html>
    """
    return render_template_string(template, iface=gradioUI)

if __name__ == "__main__":
    gradioUI.launch()
