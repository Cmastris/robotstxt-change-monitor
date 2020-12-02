""" Monitor and report changes across multiple website robots.txt files."""
# TODO: Complete core functionality
# TODO: Write tests and fix bugs
# TODO: Provide more details about changes using difflib
# TODO: Allow for multiple emails per website
# TODO: Consider using a DB to manage monitored sites (creation, deletion, email/name changes)

import datetime
import os
import requests
import traceback

# TODO: Use CSV file instead and define function to convert into list of tuples
# Constant describing each monitored URL, website name, and owner email
MONITORED_SITES = [
    ["https://github.com/", "Github", "test@hotmail.com"],
    ["", "No URL", "test@hotmail.com"],
    ["http://www.reddit.com/", "Reddit HTTP", "test@hotmail.com"],
                   ]

# File location of main log which details check and change history
MAIN_LOG = "data/main_log.txt"

# Errors which should be investigated
unexpected_errors = []


def get_timestamp():
    """Return the current time as a string in the form 'day-month-year, hour:minute'"""
    time = datetime.datetime.now()
    return time.strftime("%d-%m-%y, %H:%M")


def get_trace_str(exception):
    """Return a str representation of an Exception traceback."""
    return "".join(traceback.format_tb(exception.__traceback__)).strip()


def update_main_log(message):
    """Update the main log with a single message (str)."""
    try:
        with open(MAIN_LOG, 'a') as f:
            f.write("{}: {}\n".format(get_timestamp(), message))

    # Catch all to prevent fatal error; log error to be investigated instead
    except Exception as e:
        err_msg = "Error when updating the main log. TYPE: {}, DETAILS: {}, TRACEBACK:\n\n" \
                  "{}\n".format(type(e), e, get_trace_str(e))

        print(err_msg)
        unexpected_errors.append(err_msg)


def get_email_body(main_content):
    """Return the full email body content, including generic and unique content.

    Args:
        main_content (str): the unique email content to be inserted into the template.

    """
    # TODO: populate content
    return "Hi there,\n{}\nGeneric info".format(main_content)


def send_email(address, subject, body):
    # TODO: populate function to send email
    pass


class RunChecks:
    """Run robots.txt checks across monitored websites.

    This class is used to run robots.txt checks by initialising RobotsCheck instances,
    before initialising the relevant Report subclass to generate logs and communications.

    Attributes:
        sites (list): a list of lists, with each list item in the form: [url, name, email].
            - url (str): the absolute URL of the website homepage, with a trailing slash.
            - name (str): the website's name identifier.
            - email (str): the email address of the owner, who will receive alerts.

    """

    def __init__(self, sites):
        self.sites = sites.copy()

        # If /data doesn't exist yet, create directory and main log file
        if not os.path.isdir('data'):
            os.mkdir('data')
            f = open(MAIN_LOG, 'x')
            f.close()

    def check_all(self):
        """Iterate over all RobotsCheck instances to run change checks and reports."""
        update_main_log("Starting checks on {} sites.".format(len(self.sites)))
        print("Starting checks on {} sites.".format(len(self.sites)))

        no_change, change, first, err = 0, 0, 0, 0
        for site_check in self.sites:
            try:
                url, name, email = site_check
                url = url.strip().lower()
                email = email.strip()

                check = RobotsCheck(url)
                check.run_check()

                if check.err_message:
                    report = ErrorReport(check, name, email)
                    err += 1
                elif check.first_run:
                    report = FirstRunReport(check, name, email)
                    first += 1
                elif check.file_change:
                    report = ChangeReport(check, name, email)
                    change += 1
                else:
                    report = NoChangeReport(check, name, email)
                    no_change += 1

                print("{} check complete. Initialising {}.".format(url, type(report).__name__))
                report.create_reports()

            except Exception as e:
                err_msg = "Unexpected error for site: {}. TYPE: {}, DETAILS: {}, " \
                          "TRACEBACK:\n\n{}\n".format(site_check, type(e), e, get_trace_str(e))

                print(err_msg)
                unexpected_errors.append(err_msg)
                update_main_log(err_msg)
                # TODO: send email to user
                err += 1
                # Skip current check/report if unexpected error
                continue

        print("All checks and reports complete.")
        update_main_log("Checks & reports complete. No change: {}. Change: {}. First run: {}. "
                        "Error: {}.\n\n{}\n".format(no_change, change, first, err, "-"*150))


class RobotsCheck:
    """Check a website's robots.txt file and compare to the previous recorded file.

    This class is used to download the robots.txt file, update the robots.txt records
    (current file and file downloaded during the previous run), and check for
    any differences between the records. The results (change, no change, first run, err)
    are assigned as attributes and the instance is returned.

    Attributes:
        url (str): the absolute URL of the website homepage, with a trailing slash.
        first_run (bool): if this is the first recorded check of the website's file.
        err_message (None, str): None by default, otherwise a description of the error.
        file_change (bool): if the robots.txt file has changed since the previous record.
        dir (str): the location of the directory containing website data.
        old_file (str): the file location of the previous check robots.txt content.
        new_file (str): the file location of the latest check robots.txt content.
        old_content (str): the previous check robots.txt content.
        new_content (str): the latest check robots.txt content.

    """

    def __init__(self, url):
        self.url = url
        self.first_run = False
        self.err_message = None
        self.file_change = False
        if self.url[4] == 's':
            self.dir = "data/" + self.url[8:-1]
        else:
            self.dir = "data/" + self.url[7:-1]
        self.old_file = self.dir + "/old_file.txt"
        self.new_file = self.dir + "/new_file.txt"
        self.old_content = None
        self.new_content = None

        if (self.url[:4] != "http") or (self.url[-1] != "/"):
            self.err_message = "{} is not a valid site URL. The site URL must be absolute and " \
                               "end in a slash, e.g. 'https://www.example.com/'.".format(url)

        # If URL is valid and site directory doesn't exist, create directory
        elif not os.path.isdir(self.dir):
            try:
                os.mkdir(self.dir)
            except Exception as e:
                self.err_message = "Error when creating {} directory. TYPE: {}, DETAILS: {}, " \
                                   "TRACEBACK:\n\n{}" \
                                   "\n".format(self.url, type(e), e, get_trace_str(e))

                unexpected_errors.append(self.err_message)

    def run_check(self):
        """Update the robots.txt file records and check for changes.

        Returns:
            The class instance representing the completed robots.txt check.
        """
        if self.err_message:
            # If error/invalid URL during __init__
            print(self.err_message)
            return self

        try:
            extraction = self.download_robotstxt()
            self.update_records(extraction)
            if not self.first_run:
                self.check_diff()

        except Exception as e:
            # Anticipated errors caught in download_robotstxt() and logged in self.err_message
            if not self.err_message:
                self.err_message = "Unexpected error during {} check. TYPE: {}, DETAILS: {}, " \
                                   "TRACEBACK:\n\n{}" \
                                   "\n".format(self.url, type(e), e, get_trace_str(e))

                unexpected_errors.append(self.err_message)

            print(self.err_message)

        return self

    def download_robotstxt(self):
        """Extract and return the current content (str) of the robots.txt file."""
        robots_url = self.url + "robots.txt"
        try:
            r = requests.get(robots_url, allow_redirects=False, timeout=40)

        except requests.exceptions.Timeout:
            self.err_message = "{} timed out before sending a valid response.".format(robots_url)
            raise

        except requests.exceptions.ConnectionError as e:
            self.err_message = "There was a connection error when accessing {}. " \
                "TYPE: {} DETAILS: {}".format(robots_url, type(e), e)
            raise

        if r.status_code != 200:
            self.err_message = "{} returned a {} status code.".format(robots_url, r.status_code)
            raise requests.exceptions.HTTPError

        return r.text

    def update_records(self, new_extraction):
        """Update the files containing the current and previous robots.txt content.

        If the robots.txt file has been successfully checked previously,
        overwrite old_file with the contents of new_file (from the previous check).
        Otherwise, create the content files and set first_run = True.
        Then, add the new robots.txt extraction content to new_file.

        Args:
            new_extraction (str): the current content of the robots.txt file.

        """
        if os.path.isfile(self.new_file):
            # Overwrite the contents of old_file with the contents of new_file
            with open(self.old_file, 'w') as old, open(self.new_file, 'r') as new:
                self.old_content = new.read()
                old.write(self.old_content)

        else:
            # Create robots.txt content files if they don't exist (first non-error run)
            with open(self.old_file, 'x'), open(self.new_file, 'x'):
                pass

            self.first_run = True

        # Overwrite the contents of new_file with new_extraction
        self.new_content = new_extraction
        with open(self.new_file, 'w') as new:
            new.write(self.new_content)

    def check_diff(self):
        """Check for file differences and update self.file_change."""
        if self.old_content != self.new_content:
            self.file_change = True


class Report:
    """Report/log the results of a single robots.txt check.

    This is a base class; more specific child classes should be instantiated.

    Attributes:
        url (str): the absolute URL of the website homepage, with a trailing slash.
        dir (str): the name of the directory containing website data.
        new_content (str): the latest check robots.txt content.
        name (str): the website's name identifier.
        email (str): the email address of the owner, who will receive alerts.
        timestamp (str): the (approximate) time of the check.

    """

    def __init__(self, website, name, email):
        self.url = website.url
        self.dir = website.dir
        self.new_content = website.new_content
        self.name = name
        self.email = email
        self.timestamp = get_timestamp()

    def update_site_log(self, message):
        """Update the site log with a single message (str)."""
        try:
            log_file = self.dir + "/log.txt"
            # Append or create file if it doesn't exist
            with open(log_file, 'a+') as f:
                f.write("{}: {}\n".format(self.timestamp, message))

        except Exception as e:
            err_msg = "Error when updating the site log. TYPE: {}, DETAILS: {}, TRACEBACK:\n\n" \
                      "{}\n".format(type(e), e, get_trace_str(e))

            print(err_msg)
            unexpected_errors.append(err_msg)
            update_main_log(err_msg)

    def create_snapshot(self):
        """Create a unique text file containing the latest robots.txt content."""
        file_name = self.timestamp.replace(",", " T").replace(":", "-") + ".txt"
        snapshot_file = self.dir + "/snapshots/" + file_name
        if not os.path.isdir(self.dir + "/snapshots"):
            os.mkdir(self.dir + "/snapshots")

        with open(snapshot_file, 'x') as f:
            f.write(self.new_content)


class NoChangeReport(Report):
    """Log and print the result (no change) of a single robots.txt check."""

    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super

    def create_reports(self):
        """Update the site log and print result."""
        content = "No changes to {} robots.txt file.".format(self.url)
        self.update_site_log(content)
        print(content)


class ChangeReport(Report):
    # TODO: Complete documentation and add methods
    # TODO: Add method to print results to the console
    # TODO: Add method to write an email report
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super
        self.old_content = website.old_content

    def create_reports(self):
        # TODO: populate method
        # Update the website log
        # Update the main log
        # Print result to the console
        # Record snapshot
        # Write and send email
        print("Method create_reports called.")
        self.create_snapshot()
        return self


class FirstRunReport(Report):
    # TODO: Complete documentation and add methods
    # TODO: Add method to print results to the console
    # TODO: Add method to write an email report
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super

    def create_reports(self):
        # TODO: populate method
        # Update the website log
        # Update the main log
        # Print result to the console
        # Record snapshot
        # Write and send email
        print("Method create_reports called.")
        self.create_snapshot()
        return self


class ErrorReport(Report):
    """Log, print, and email the result (error) of a single robots.txt check.

    Attributes:
        err_message (str): A description of the error logged during RobotsCheck.

    """

    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super
        self.err_message = website.err_message

    def create_reports(self):
        """Update site log, update main log, print result, and send email."""
        if os.path.isdir(self.dir):
            self.update_site_log(self.err_message)
        update_main_log(self.err_message)
        print(self.err_message)
        email_subject = "{} Robots.txt Check Error".format(self.name)
        email_body = get_email_body(self.err_message)  # TODO: update content
        send_email(self.email, email_subject, email_body)


if __name__ == "__main__":
    try:
        RunChecks(MONITORED_SITES).check_all()
        # TODO: email program owner with summary & unexpected errors
    except Exception as fatal_err:
        # Fatal error during RunChecks init
        fatal_err_msg = "Fatal error. TYPE: {}, DETAILS: {}, TRACEBACK:\n\n" \
                        "{}\n".format(type(fatal_err), fatal_err, get_trace_str(fatal_err))

        print(fatal_err_msg)
        update_main_log(fatal_err_msg)
        # TODO: email program owner
