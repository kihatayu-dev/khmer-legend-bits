from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

places = []
COMMENTS_FILE = "comments.json"

def load_comments():
    if not os.path.exists(COMMENTS_FILE):
        return []
    with open(COMMENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_comments(comments):
    with open(COMMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    comments = load_comments()
    return render_template("index.html", places=places, comments=comments)

@app.route("/add_comment", methods=["POST"])
def add_comment():
    data = request.get_json()
    name = data.get("name", "").strip()
    text = data.get("text", "").strip()
    if not name or not text:
        return jsonify({"error": "Missing name or text"}), 400

    comment = {
        "name": name,
        "text": text,
        "time": datetime.now().strftime("%b %d, %Y · %I:%M %p")
    }

    comments = load_comments()
    comments.insert(0, comment)   # newest first
    save_comments(comments)

    return jsonify(comment)

@app.route("/place/<int:place_id>")
def place(place_id):
    p = next((p for p in places if p["id"] == place_id), None)
    return render_template("place.html", place=p)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)