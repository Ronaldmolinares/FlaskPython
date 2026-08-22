import os
from datetime import datetime

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
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"


@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)


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
        title = request.form.get("title")
        content = request.form.get("content")
        created_at = datetime.now()

        note_db = Note(title=title, content=content, created_at=created_at)

        db.session.add(note_db)
        db.session.commit()

        return render_template("home.html")

    return render_template("note_form.html")
