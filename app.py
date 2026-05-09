from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

from utils.vector_store import load_vector_db
from utils.prompt_template import build_prompt

load_dotenv()

app = Flask(__name__)

<<<<<<< HEAD
client = genai.Client(api_key="")
=======
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

vectordb = load_vector_db()
>>>>>>> 7ddba21 (updated code)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    if not user_message:
        return jsonify({
            "reply": "Ask something 😑"
        })

    docs = vectordb.similarity_search(user_message, k=3)

    context = "\n".join([
        doc.page_content for doc in docs
    ])

    prompt = build_prompt(context, user_message)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return jsonify({
        "reply": response.text
    })


@app.route("/upload", methods=["POST"])
def upload_pdf():

    file = request.files["pdf"]

    filepath = os.path.join("uploads", file.filename)

    file.save(filepath)

    return jsonify({
        "message": "PDF uploaded successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)
