#!/usr/bin/env python3
""" Basic Authentication module for the API.
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class inheriting from Auth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.

        Returns:
            The Base64 encoded part of the Authorization header or None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        # Extract and return the part after "Basic "
        return authorization_header[len("Basic "):]
