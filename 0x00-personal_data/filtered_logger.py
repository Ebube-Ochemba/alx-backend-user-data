#!/usr/bin/env python3
"""A module for log handling"""
import logging
import os
import re
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates specific fields in a log message.

    Args:
        fields (List[str]): List of strings of fields to obfuscate.
        redaction (str): String by which the field values will be replaced.
        message (str): The log line to be processed.
        separator (str): Character that separates all fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f"({'|'.join(fields)})=.*?({separator}|$)"
    return re.sub(
        pattern,
        lambda match: f"{match.group(1)}={redaction}{match.group(2)}",
        message
        )


def get_logger() -> logging.Logger:
    """ Returns a Logger Object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Set up stream handler with the RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a MySQL database connection."""
    # Retrieve credentials from environment variables
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # Connect to the MySQL database
    db_connection = mysql.connector.connection.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return db_connection


def main():
    """Main function to retrieve and log user data."""
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users;")
    for row in cursor.fetchall():
        name, email, phone, ssn, password, ip, last_login, user_agent = row
        log_message = (
            f"name={name}; email={email}; phone={phone}; ssn={ssn}; "
            f"password={password}; ip={ip}; last_login={last_login}; "
            f"user_agent={user_agent};"
        )
        logger.info(log_message)

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with redacted fields."""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


if __name__ == '__main__':
    main()
