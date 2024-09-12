#!/usr/bin/env python3
"""A simple Flask app."""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome():
    """GET route to return a welcome message in JSON format."""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
