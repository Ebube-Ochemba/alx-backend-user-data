#!/usr/bin/env python3
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns the salted hash."""
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')

    # Generate a salt
    salt = bcrypt.gensalt()

    # Generate the hash using bcrypt
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password
