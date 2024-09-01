# Personal data

> This project was Personal data handling.

## Summary

I learnt about `Personally Identifiable Information` (**PII**), how to implement a log filter that will obfuscate **PII** fields, how to encrypt a password and check the validity of an input password, and how to authenticate to a database using environment variables

## Files

> Each file contains the solution to a task in the project.

- [filtered_logger.py](https://github.com/Ebube-Ochemba/alx-backend-user-data/blob/main/0x00-personal_data/filtered_logger.py): Multiple task:
    - [x] **#0**: A function called `filter_datum` that returns the log message obfuscated.
    - [x] **#1**: Add this code:
    ```
    class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
    ```
    - Update the class to accept a list of strings `fields` constructor argument.
    - Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for `fields` in fields should be filtered.
    - DO NOT extrapolate `FORMAT` manually. The `format` method should be less than 5 lines long.
    - [] **#2**: Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object.
    - [] **#3**: 
- [encrypt_password.py](https://github.com/Ebube-Ochemba/alx-backend-user-data/blob/main/0x00-personal_data/encrypt_password.py):

> [test_files](): A folder of test files. Provided by Alx.
