from config import Config
from flask import Flask, render_template, request
from flask_migrate import Migrate
from models import db
from notes.routes_notes import notes_bp
from users.routes_users import users_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(notes_bp)
app.register_blueprint(users_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "Formulario enviado correctamente.", 201
    return "Página de contacto."
