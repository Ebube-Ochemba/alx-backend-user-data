#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """Generates a salted, hashed password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    # Check if the password matches the hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)
