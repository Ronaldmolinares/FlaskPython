from flask import Flask

app = Flask(__name__)


@app.route("/")
def create_app():
    return "Hello World, :) Flask is working!"


# Para ejecutar la aplicacion --> flask run
# debug en local --> flask run --debugger