import os.path

from flask import render_template

from app import app


SERVICE_PATH = os.path.dirname(__file__)
app.template_folder = os.path.join(SERVICE_PATH, "templates")
app.static_folder = os.path.join(SERVICE_PATH, "static")


@app.route("/index")
def index():
    return render_template("index.html")
