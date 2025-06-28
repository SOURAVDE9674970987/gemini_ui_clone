from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import markdown
from bs4 import BeautifulSoup

app = Flask(__name__)

genai.configure(api_key="AIzaSyAXaGtYZ8V1bLwtp1KeuTEXD35XTmOWf_E")
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def markdown_to_clean_html(md):
    html = markdown.markdown(md, extensions=["extra"])
    return str(BeautifulSoup(html, "html.parser"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_route():
    data = request.get_json()
    user_input = data.get("message")
    try:
        response = chat.send_message(user_input)
        html_response = markdown_to_clean_html(response.text)
        return jsonify({"response": html_response})
    except Exception as e:
        return jsonify({"response": f"<p style='color:red;'>Error: {str(e)}</p>"})

if __name__ == "__main__":
    app.run(debug=True)