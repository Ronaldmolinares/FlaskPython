import os

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), "notes.sqlite")
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Note(db.Model):  # type: ignore[name-defined]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"


@app.route("/")
def home():
    role = "admin"
    notes = [
        {"id": 1, "title": "Note 1", "content": "This is the content of note 1."},
        {"id": 2, "title": "Note 2", "content": "This is the content of note 2."},
        {"id": 3, "title": "Note 3", "content": "This is the content of note 3."},
    ]
    return render_template("home.html", role=role, notes=notes)


# Para ejecutar la aplicacion --> flask run
# debug en local --> flask run --debugger


@app.route("/about")
def about():
    return "This is a simple notes app built with Flask."


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "Formulario enviado correctamente.", 201
    return "Página de contacto."


@app.route("/api/info")
def api_info():
    data = {
        "app_name": "Notes App",
        "version": "1.0",
        "description": "A simple notes application built with Flask.",
    }

    return jsonify(data), 200


@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")


@app.route("/create-note", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        note = request.form.get("note", "No encontrada")
        # return redirect(
        #     url_for("confirmation", note=note)
        # )
        return render_template("confirmation.html", note=note)

    return render_template("note_form.html")
