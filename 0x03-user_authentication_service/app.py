#!/usr/bin/env python3
"""A simple Flask app."""
from flask import abort, Flask, jsonify, make_response, request, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """GET route to return a welcome message in JSON format."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """POST /users route for registering a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """POST /sessions route for user login."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)  # Unauthorized access

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """DELETE /sessions route for logging out."""
    # Retrieve session_id from the cookie
    session_id = request.cookies.get("session_id")

    if session_id is None:
        return abort(403)

    # Find the user with the session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        return abort(403)

    # Destroy the session and redirect to home page
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """GET /profile route to get user profile using session_id cookie."""
    session_id = request.cookies.get("session_id")

    if session_id is None:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        return abort(403)

    # Return the user's email in the response
    return jsonify({"email": user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
