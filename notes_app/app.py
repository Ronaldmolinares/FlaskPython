from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("/")
def create_app():
    return "Hello World, :) Flask is working!"


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