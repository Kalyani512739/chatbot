from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from google import genai
from dotenv import load_dotenv
import os

# -----------------------------------
# PDF AI Imports
# -----------------------------------

from utils.pdf_loader import extract_text_from_pdf
from utils.text_splitter import split_text
from utils.vector_store import (
    create_vector_db,
    load_vector_db
)
from utils.prompt_template import build_prompt

# -----------------------------------
# Flask App Setup
# -----------------------------------

app = Flask(__name__)

app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# -----------------------------------
# Load Environment Variables
# -----------------------------------

load_dotenv()

# -----------------------------------
# Gemini AI Client
# -----------------------------------

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -----------------------------------
# Database Model
# -----------------------------------

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )

# -----------------------------------
# Home Route
# -----------------------------------

@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    return render_template("index.html")

# -----------------------------------
# Register Route
# -----------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return "User already exists 😑"

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        new_user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# -----------------------------------
# Login Route
# -----------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and bcrypt.check_password_hash(
            user.password,
            password
        ):

            session["user"] = username

            return redirect("/")

        return "Invalid username or password 😑"

    return render_template("login.html")

# -----------------------------------
# Logout Route
# -----------------------------------

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")

# -----------------------------------
# Upload PDF Route
# -----------------------------------

@app.route("/upload", methods=["POST"])
def upload_pdf():

    if "user" not in session:
        return jsonify({
            "message": "Login required 😑"
        })

    if "pdf" not in request.files:
        return jsonify({
            "message": "No PDF uploaded 😑"
        })

    file = request.files["pdf"]

    if file.filename == "":
        return jsonify({
            "message": "Choose a PDF 😑"
        })

    # -----------------------------------
    # Create Upload Folder
    # -----------------------------------

    os.makedirs("uploads", exist_ok=True)

    filepath = os.path.join(
        "uploads",
        file.filename
    )

    # Save PDF
    file.save(filepath)

    try:

        # -----------------------------------
        # Extract Text
        # -----------------------------------

        text = extract_text_from_pdf(filepath)

        # -----------------------------------
        # Split Into Chunks
        # -----------------------------------

        chunks = split_text(text)

        # -----------------------------------
        # Store In Vector DB
        # -----------------------------------

        create_vector_db(chunks)

        return jsonify({
            "message": "PDF uploaded & trained successfully 😎"
        })

    except Exception as e:

        print("UPLOAD ERROR:", e)

        return jsonify({
            "message": "Failed to process PDF 😑"
        })

# -----------------------------------
# Chat Route
# -----------------------------------

@app.route("/chat", methods=["POST"])
@app.route("/chat", methods=["POST"])
def chat():

    if "user" not in session:
        return jsonify({
            "reply": "Please login first 😑"
        })

    user_message = request.json.get("message")

    if not user_message:
        return jsonify({
            "reply": "Ask something 😑"
        })

    try:

        # Load vector DB
        vectordb = load_vector_db()

        # Search with scores
        results = vectordb.similarity_search_with_score(
            user_message,
            k=4
        )

        relevant_docs = []

        for item in results:
            doc = item[0]
            score = item[1]

            print("Score:", score)

            if score < 0.5:
                relevant_docs.append(doc)

        # Use PDF if relevant content found
        if relevant_docs:

            context = "\n\n".join([
                doc.page_content
                for doc in relevant_docs
            ])

            final_prompt = build_prompt(
                context,
                user_message
            )

            print("Using PDF context")

        else:

            final_prompt = user_message

            print("Using normal Gemini")

        # Gemini response
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=final_prompt
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:

        print("CHAT ERROR:", e)

        return jsonify({
            "reply": "Something went wrong 😑"
        })
# -----------------------------------
# Create Database
# -----------------------------------

with app.app_context():
    db.create_all()

# -----------------------------------
# Run App
# -----------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )