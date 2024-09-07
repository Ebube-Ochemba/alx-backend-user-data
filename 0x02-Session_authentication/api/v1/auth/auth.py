#!/usr/bin/env python3
""" Authentication module for the API.
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class for managing API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if a path requires authentication.
        - Returns True if the path is not in excluded_paths.
        - Path and excluded_paths must be slash tolerant.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure both the path and excluded_paths end with '/'
        if path[-1] != '/':
            path += '/'

        for excluded in excluded_paths:
            if excluded.endswith('*'):
                # Check if the path starts with the portion before the '*'
                if path.startswith(excluded[:-1]):
                    return False
            else:
                if excluded[-1] != '/':
                    excluded += '/'
                if path == excluded:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Retrieves the authorization header from the request.
        Returns None if the header is missing or if request is None.
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """ Retrieves the current user from the request. """
        return None

    def session_cookie(self, request=None):
        """ Returns the value of the session cookie from the request """
        if request is None:
            return None

        # Get the session cookie name from the environment variable
        session_name = os.getenv("SESSION_NAME")

        # Use .get() to safely retrieve the cookie value
        return request.cookies.get(session_name)
