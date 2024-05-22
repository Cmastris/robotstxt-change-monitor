import os
import smtplib
import time

import yagmail

import config
import logs

# A list of tuples containing email data (see 'send_emails()' documentation for details)
site_emails = []
admin_email = []


@logs.unexpected_exception_handling
def replace_angle_brackets(content):
    """Replace angle brackets with curly brackets to avoid interpretation as HTML.

    Args:
        content (str): the content containing angle brackets to replace().

    """
    return content.replace("<", "{").replace(">", "}")


@logs.unexpected_exception_handling
def get_site_email_body(main_content):
    """Return the full site admin email body content, including generic and unique content.

    Args:
        main_content (str): the unique email content to be inserted into the template.

    """
    email_link = "<a href=\"mailto:{}\">{}</a>".format(config.ADMIN_EMAIL, config.ADMIN_EMAIL)

    return "Hi there,\n\n{}\n\nThis is an automated message; please do not reply directly " \
           "to this email. If you have any questions, bug reports, or feedback, please " \
           "contact the tool administrator: {}. Thanks!\n".format(main_content, email_link)


@logs.unexpected_exception_handling
def get_admin_email_body(main_content):
    """Return the full admin email body content, including generic and unique content.

    Args:
        main_content (str): the unique email content to be inserted into the template.

    """
    if len(logs.admin_email_errors) == 0:
        return "Hi there,\n\n{}\n\nThere were no unexpected errors.".format(main_content)

    else:
        email_errs = [replace_angle_brackets(e) for e in logs.admin_email_errors.copy()]

        return "Hi there,\n\n{}\n\nErrors which may require investigation are listed below:\n\n" \
               "{}".format(main_content, "\n\n".join(email_errs))


@logs.unexpected_exception_handling
def set_email_login():
    """Save or update the 'config.SENDER_EMAIL' login details using the keyring library."""
    pw = input("Type in {} password and press Enter: ".format(config.SENDER_EMAIL))
    # A wrapper for the Python keyring library
    yagmail.register(config.SENDER_EMAIL, pw)


@logs.unexpected_exception_handling
def save_unsent_email(address, subject, body):
    """Save the key details of an email which couldn't be sent to a timestamped .txt file.

    Args:
        address (str): the destination email address.
        subject (str): the subject line of the email.
        body (str): the main body content of the email.

    """
    unsent_dir = config.PATH + 'data/_unsent_emails'
    if not os.path.isdir(unsent_dir):
        os.mkdir(unsent_dir)

    file_name = logs.get_timestamp(str_format="%d-%m-%y T %H-%M-%S") + ".txt"
    with open(unsent_dir + "/" + file_name, 'x') as f:
        f.write(address + "\n\n" + subject + "\n\n" + body)

    success_msg = "Unsent email content successfully saved in /data/_unsent_emails/."
    print(success_msg)
    logs.update_main_log(success_msg)
    # Ensure timestamp is unique
    time.sleep(1)


@logs.unexpected_exception_handling
def send_emails(emails_list):
    """Send emails based on a list of tuples in the form (address, subject, body, *attachments).

    Args:
        emails_list (list): A list of tuples, with each tuple containing the following data:
            - address (str): the destination email address.
            - subject (str): the subject line of the email.
            - body (str): the main body content of the email.
            - *attachments (str, optional): 0 or more attachment file locations.

    """
    if not config.EMAILS_ENABLED:
        return None

    # Provide sender email password as second argument if not saving via 'set_email_login()'
    with yagmail.SMTP(config.SENDER_EMAIL) as server:
        print("\nSending {} email(s)...".format(len(emails_list)))
        valid_login = True
        for address, subject, body, *attachments in emails_list:
            # Re-attempt send if login failed and password updated via 'set_email_login()'
            while valid_login:
                try:
                    server.send(to=address, subject=subject, contents=body, attachments=attachments)
                    print("Email sent to {} (subject: {}).".format(address, subject))
                    time.sleep(0.5)
                    # Break out of 'while valid_login' loop to move to next email
                    break

                except smtplib.SMTPAuthenticationError as e:
                    short_err_msg = "Email login failed. Please ensure that less secure app " \
                                    "access is 'On' for the sender email Google account and " \
                                    "that your saved login details are correct."

                    print(short_err_msg)
                    # Provide option of updating password and re-attempting send
                    answer = input("Type 'y' and press Enter to update your saved password "
                                   "and re-attempt the login: ")

                    if answer.lower().strip() == 'y':
                        set_email_login()

                    else:
                        err_msg = logs.get_err_str(e, short_err_msg + "These can be updated using "
                                                   "set_email_login().", trace=False)

                        logs.log_error(err_msg)
                        # Skip send attempts for any subsequent emails
                        valid_login = False

                # Prevent all emails failing; log error and save unsent email
                except Exception as e:
                    err_msg = logs.get_err_str(e, "Error sending email to {}.".format(address))
                    logs.log_error(err_msg)
                    save_unsent_email(address, subject, body)
                    # Break out of while loop to move to next email
                    break
