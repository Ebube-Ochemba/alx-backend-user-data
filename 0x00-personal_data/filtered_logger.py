#!/usr/bin/env python3
"""A module for log handling"""
import logging
from typing import List
import re


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
