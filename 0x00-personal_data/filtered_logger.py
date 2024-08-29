#!/usr/bin/env python3
"""A module for log handling"""
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
    for field in fields:
        remix = re.sub(f'{field}=.*?{separator}',
                       f'{field}={redaction}{separator}', message)
    return remix
