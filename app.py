from flask import Flask, render_template

app = Flask(__name__)

places = []

@app.route("/")
def index():
    return render_template("index.html", places=places)

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
