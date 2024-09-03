#!/usr/bin/env python3
""" Authentication module for the API.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class for managing API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if a path requires authentication. """
        return False

    def authorization_header(self, request=None) -> str:
        """ Retrieves the authorization header from the request. """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the current user from the request. """
        return None
