from datetime import datetime, timezone

from flask import Blueprint, redirect, render_template, request, url_for
from models import Note, db  # type: ignore[import-not-found]

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notes")
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)


@notes_bp.route("/create-note", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        created_at = datetime.now(timezone.utc)

        note_db = Note(title=title, content=content, created_at=created_at)

        db.session.add(note_db)
        db.session.commit()

        return redirect(url_for("notes.home"))

    return render_template("note_form.html")


@notes_bp.route("/edit-note/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        note.title = title
        note.content = content

        db.session.commit()

        return redirect(url_for("notes.home"))

    return render_template("edit_note.html", note=note)


@notes_bp.route("/delete-note/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()

    return redirect(url_for("notes.home"))
