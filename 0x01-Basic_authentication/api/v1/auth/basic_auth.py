#!/usr/bin/env python3
""" Basic Authentication module for the API.
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic authentication class inheriting from Auth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Decodes a Base64 string into its original format.

        Returns:
            Decoded UTF-8 string, or None if the input is invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode Base64 and convert to UTF-8
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value.

        Returns:
            A tuple containing the user email and password,
            or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split the string into user email and password
        email, password = decoded_base64_authorization_header.split(':', 1)

        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """
        Retrieves the User instance based on email and password.

        Returns:
            The User instance if credentials are valid, or None if invalid.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user in the database using their email
        try:
            user_list = User.search({"email": user_email})
        except Exception:
            None

        # Validate the user's password
        for user in user_list:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None):
        """
        Retrieves the User instance for a request.

        Returns:
            User: The authenticated User instance,
            or None if authentication fails.
        """
        # Get the authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract the Base64 encoded part from the Authorization header
        encoded = self.extract_base64_authorization_header(auth_header)
        if encoded is None:
            return None

        # Step 3: Decode the Base64 credentials
        decoded = self.decode_base64_authorization_header(encoded)
        if decoded is None:
            return None

        # Step 4: Extract the user email and password
        user_email, user_pwd = self.extract_user_credentials(decoded)
        if user_email is None or user_pwd is None:
            return None

        # Step 5: Retrieve the User object based on the credentials
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
