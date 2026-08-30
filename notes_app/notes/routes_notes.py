from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from models import Note, db  # type: ignore[import-not-found]

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notes")
def home():
    if "user_id" not in session:
        return redirect(url_for("index"))

    notes = (
        Note.query.filter_by(user_id=session["user_id"])
        .order_by(Note.created_at.desc())
        .all()
    )
    return render_template("home.html", notes=notes)


@notes_bp.route("/create-note", methods=["GET", "POST"])
def create_note():
    if "user_id" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        created_at = datetime.now(timezone.utc)

        note_db = Note(
            title=title,
            content=content,
            created_at=created_at,
            user_id=session["user_id"],
        )

        db.session.add(note_db)
        db.session.commit()

        flash("Nota creada exitosamente.", "success")
        return redirect(url_for("notes.home"))

    return render_template("note_form.html")


@notes_bp.route("/edit-note/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    note = Note.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        note.title = title
        note.content = content

        db.session.commit()

        flash("Nota actualizada exitosamente.", "success")
        return redirect(url_for("notes.home"))

    return render_template("edit_note.html", note=note)


@notes_bp.route("/delete-note/<int:id>", methods=["POST"])
def delete_note(id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    note = Note.query.filter_by(id=id, user_id=session["user_id"]).first_or_404()
    db.session.delete(note)
    db.session.commit()

    flash("Nota eliminada exitosamente.", "success")
    return redirect(url_for("notes.home"))
