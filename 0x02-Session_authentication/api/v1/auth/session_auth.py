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
