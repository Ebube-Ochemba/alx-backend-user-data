#!/usr/bin/env python3
""" Session Authentication Database module for the API.
"""
from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth to handle session storage in the database."""

    def create_session(self, user_id=None):
        """Create a session and store it in the database."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save the session to the database (file)
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user ID for the given session ID from the database."""
        if session_id is None:
            return None

        try:
            # Search for UserSession with the given session_id
            user_sessions = UserSession.search({"session_id": session_id})
            if not user_sessions:
                return None

            session = user_sessions[0]
            if self.session_duration <= 0:
                return session.user_id

            created_at = session.created_at
            if created_at is None:
                return None

            expiration_time = created_at + timedelta(
                seconds=self.session_duration)
            if datetime.now() > expiration_time:
                return None

            return session.user_id
        except KeyError:
            # If no session is found, return None
            return None

    def destroy_session(self, request=None):
        """Destroy the session based on ID from the request cookie."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False

        session = user_sessions[0]
        session.remove()  # Remove the session from the database
        return True
