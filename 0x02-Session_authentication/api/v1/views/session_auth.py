#!/usr/bin/env python3
"""Module of Session views"""
import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'],
                 strict_slashes=False)
def auth_session():
    """Handles user login via session authentication"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the user
    from api.v1.app import auth  # To avoid circular dependency
    session_id = auth.create_session(user.id)

    # Return user data as JSON
    response = jsonify(user.to_json())

    # Set the session ID cookie
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
