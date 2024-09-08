#!/usr/bin/env python3
""" Session Authentication module for the API.
"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """Session authentication class that inherits from Auth"""

    # Class attribute to store session IDs and corresponding user IDs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a given user ID and store it in memory"""
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a unique session ID
        session_id = str(uuid.uuid4())

        # Store the session ID and corresponding user ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return the user ID based on the session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the user ID from the Class attribute storage
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Retrieves a User instance based on a session ID """
        session_id = self.session_cookie(request)
        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session / logs out"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
