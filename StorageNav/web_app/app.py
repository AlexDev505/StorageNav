import os.path

from flask import render_template

from app import app, config
from .api import api


SERVICE_PATH = os.path.dirname(__file__)
app.template_folder = os.path.join(SERVICE_PATH, "templates")
app.static_folder = os.path.join(SERVICE_PATH, "static")
app.secret_key = config.tg_bot.webhook.secret_key


@app.route("/index")
def index():
    return render_template("index.html")


app.register_blueprint(api, url_prefix="/api/v1")
