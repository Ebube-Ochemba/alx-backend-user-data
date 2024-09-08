#!/usr/bin/env python3
"""
User Session model
"""
from models.base import Base
from datetime import datetime


class UserSession(Base):
    """UserSession model to store session data."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize the UserSession with user_id and session_id."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.created_at = kwargs.get('created_at', datetime.now())
