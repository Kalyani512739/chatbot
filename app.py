from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

client = genai.Client(api_key="")

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"reply": "Say something 😑"})

    try:
        chat_history.append(user_message)

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=chat_history
        )

        bot_reply = response.text

        chat_history.append(bot_reply)

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
