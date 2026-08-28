from datetime import datetime, timezone

from config import Config
from flask import Flask, redirect, render_template, request, url_for
from models import Note, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)


@app.route("/about")
def about():
    return "This is a simple notes app built with Flask."


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "Formulario enviado correctamente.", 201
    return "Página de contacto."


@app.route("/create-note", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        created_at = datetime.now(timezone.utc)

        note_db = Note(title=title, content=content, created_at=created_at)

        db.session.add(note_db)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("note_form.html")


@app.route("/edit-note/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        note.title = title
        note.content = content

        db.session.commit()

        return redirect(url_for("home"))

    return render_template("edit_note.html", note=note)


@app.route("/delete-note/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()

    return redirect(url_for("home"))
