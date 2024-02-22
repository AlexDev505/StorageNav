import hashlib
import hmac
from functools import wraps
from urllib.parse import unquote

from flask import Blueprint, jsonify, session

from app import config
from .utils import parse_args


api = Blueprint("api_v1", __name__)


def login():
    session["logged"] = True


def logout():
    session.pop("logged")


def login_required(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        if not session.get("logged"):
            return jsonify(status="fail", message="unauthorized")
        return func(*args, **kwargs)

    return _wrapper


@api.route("/login", methods=["GET", "POST"])
@parse_args
def start_session(hash_string: str, data: str):
    try:
        init_data = sorted(
            [
                chunk.split("=")
                for chunk in unquote(data).split("&")
                if chunk[: len("hash=")] != "hash="
            ],
            key=lambda x: x[0],
        )
        init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])

        secret_key = hmac.new(
            "WebAppData".encode(), config.tg_bot.token.encode(), hashlib.sha256
        ).digest()
        must_be_hash = hmac.new(
            secret_key, init_data.encode(), hashlib.sha256
        ).hexdigest()

        assert must_be_hash == hash_string
    except (AssertionError, IndexError):
        return jsonify(status="fail", message="forbidden")

    login()

    return jsonify(status="ok")


@api.route("/logout", methods=["GET", "POST"])
@login_required
def end_session():
    logout()


@api.route("/test", methods=["GET", "POST"])
@login_required
@parse_args
def test():
    return jsonify(status="ok")
