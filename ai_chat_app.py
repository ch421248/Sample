import openai
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Minimal HTML UI
HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>AI Chat App</title>
  <style>
    body { font-family: Arial; margin: 40px; background: #f8f9fa; }
    h2 { color: #4caf50; }
    .chatbox { border: 1px solid #ccc; padding: 16px; background: #fff; }
    .message { margin-bottom: 12px; }
    .user { color: #2196f3; }
    .ai { color: #e91e63; }
    input[type=text] { width: 80%; padding: 8px; }
    input[type=submit] { padding: 8px 16px; }
  </style>
</head>
<body>
  <h2>AI Chat App</h2>
  <div class="chatbox" id="chatbox"></div>
  <form id="chatForm">
    <input type="text" id="userInput" autocomplete="off" placeholder="Say something..." />
    <input type="submit" value="Send" />
  </form>
<script>
const chatbox = document.getElementById('chatbox');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
let messages = [];

function render() {
    chatbox.innerHTML = messages.map(m =>
        `<div class="message"><b class="${m.role}">${m.role === "user" ? "You" : "AI"}:</b> ${m.content}</div>`
    ).join('');
}

chatForm.onsubmit = async e => {
    e.preventDefault();
    const input = userInput.value;
    messages.push({ role: "user", content: input });
    render();
    userInput.value = "";
    let res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages })
    });
    let data = await res.json();
    messages.push({ role: "ai", content: data.reply });
    render();
};
render();
</script>
</body>
</html>
"""

# Set your OpenAI API key here or as environment variable OPENAI_API_KEY
openai.api_key = os.environ.get("OPENAI_API_KEY", "sk-...")

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    # Transform messages for OpenAI API
    api_messages = [
        {"role": "user" if m["role"] == "user" else "assistant", "content": m["content"]}
        for m in messages
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=api_messages[-5:],  # Keep last 5 for context
            max_tokens=128
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Error: {e}"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)