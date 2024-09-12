#!/usr/bin/env python3
"""Authentication module"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt & returns the salted hash."""

    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password


def _generate_uuid() -> str:
    """Generates a new UUID & returns its string representation."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user if the email doesn't exist."""
        try:
            # Check if the user already exists by email
            self._db.find_user_by(email=email)
            # If the user is found, raise ValueError
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If user is not found, create a new user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a new session for the user with the given email."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            # Update the user's session_id and commit the changes
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieves a user based on the session ID."""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session by setting the session ID to None."""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a password reset token for the user with the given email."""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError(f"No user found with email: {email}")

        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password of a user based on the reset_token."""
        user = self._db.find_user_by(reset_token=reset_token)

        if not user:
            raise ValueError("Invalid reset token")

        # Hash the new password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                        bcrypt.gensalt())

        # Update user's password and invalidate the reset token
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
