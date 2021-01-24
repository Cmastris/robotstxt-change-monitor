import datetime
import functools
import traceback

import config

# Errors which will be sent to 'config.ADMIN_EMAIL' to be investigated
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


def update_main_log(message, blank_before=False, timestamp=True):
    """Update the 'config.MAIN_LOG' text file with a single message.

    Args:
        message (str): the message content to be logged.
        blank_before (bool): whether a blank line is added before the message (default=False).
        timestamp (bool): whether the message starts with a timestamp (default=True).

    """
    try:
        message = message + "\n"
        if timestamp:
            message = get_timestamp() + ": " + message

        if blank_before:
            message = "\n" + message

        with open(config.MAIN_LOG, 'a') as f:
            f.write(message)

    except Exception as e:
        err_msg = get_err_str(e, "Error when updating the main log.")
        log_error(err_msg, log_in_main=False)


@unexpected_exception_handling
def get_timestamp(str_format="%d-%m-%y, %H:%M"):
    """Return the current time as a string (default: 'day-month-year, hour:minute').

    Args:
        str_format (str): a valid 'datetime.datetime.strftime' format.

    """
    current_time = datetime.datetime.now()
    return current_time.strftime(str_format)
