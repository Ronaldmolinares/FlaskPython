from flask import Flask, request, jsonify, render_template, redirect, url_for


app = Flask(__name__)


@app.route("/")
def home():
    role = "admin"
    notes = [
        {"id": 1, "title": "Note 1", "content": "This is the content of note 1."},
        {"id": 2, "title": "Note 2", "content": "This is the content of note 2."},
        {"id": 3, "title": "Note 3", "content": "This is the content of note 3."}
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
        "description": "A simple notes application built with Flask."
    }

    return jsonify(data), 200

@app.route("/confirmation")
def confirmation():
    return "Formulario enviado correctamente.", 201

@app.route("/create-note", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        note = request.form.get("note", "No encontrada")
        return redirect(
            url_for("confirmation", note=note)
        )
    
    return render_template("note_form.html")
