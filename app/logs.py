import datetime
import functools
import os
import traceback

import config

# Errors that will be emailed (if configured) to 'ADMIN_EMAIL' in config.py
admin_email_errors = []


def unexpected_exception_handling(func):
    """Wrap the passed function in a generic try/except block and log any exception."""
    # Preserve info about the original function
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_str = "Unexpected error in function: {}.".format(func.__name__)
            if len(args) > 0:
                obj_name = type(args[0]).__name__
                if ("Report" in obj_name) or ("Check" in obj_name):
                    err_str += " Class instance: {}".format(args[0])

            err_msg = get_err_str(e, err_str)
            log_error(err_msg)

    return wrapper


@unexpected_exception_handling
def get_err_str(exception, message, trace=True):
    """Return an error string containing a message and exception details.

    Args:
        exception (obj): the exception object caught.
        message (str): the base error message.
        trace (bool): whether the traceback is included (default=True).

    """
    if trace:
        trace_str = "".join(traceback.format_tb(exception.__traceback__)).strip()
        err_str = "{}\nTYPE: {}\nDETAILS: {}\nTRACEBACK:\n\n{}\n" \
                  "".format(message, type(exception), exception, trace_str)
    else:
        err_str = "{}\nTYPE: {}\nDETAILS: {}\n".format(message, type(exception), exception)

    return err_str


def log_error(error_message, print_err=True, log_in_main=True, in_admin_email=True):
    """Log an error message via print(), update_main_log(), and in 'admin_email_errors'.

    Args:
        error_message (str): the error message to be logged.
        print_err (bool): whether the message should be printed.
        log_in_main (bool): whether the message should be logged in the main log.
        in_admin_email (bool): whether the message should be logged in 'admin_email_errors'.

    """
    if print_err:
        print(error_message)
    if log_in_main:
        update_main_log(error_message)
    if in_admin_email:
        admin_email_errors.append(error_message)


def prepend_to_file(file_path, content):
    """Prepend content (str) to a new line of a file at a specified path (str)."""
    existing_content = ""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            existing_content = f.read()

    with open(file_path, 'w') as f:
        f.write(content + "\n" + existing_content)


def update_main_log(message, blank_after=False, include_timestamp=True):
    """Update the 'config.MAIN_LOG' text file with a single message.

    Args:
        message (str): the message content (excluding timestamp) to be logged.
        blank_after (bool): whether a blank line is added after the message.
        include_timestamp (bool): whether the message should start with a timestamp.

    """
    try:
        if include_timestamp:
            message = get_timestamp() + ": " + message

        if blank_after:
            message = message + "\n"

        prepend_to_file(config.MAIN_LOG, message)

    except Exception as e:
        err_msg = get_err_str(e, "Error when updating the main log.")
        log_error(err_msg, log_in_main=False)


@unexpected_exception_handling
def get_timestamp(str_format="%Y-%m-%d %H:%M"):
    """Return the current time as a string (default: 'year-month-day hour:minute').

    Args:
        str_format (str): a valid 'datetime.datetime.strftime' format.

    """
    current_time = datetime.datetime.now()
    return current_time.strftime(str_format)
