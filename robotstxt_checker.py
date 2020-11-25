""" Monitor and report changes across multiple website robots.txt files."""
# TODO: Complete core functionality
# TODO: Write tests and fix bugs
# TODO: Provide more details about changes using difflib
# TODO: Allow for multiple emails per website
# TODO: Consider using a DB to manage monitored sites (creation, deletion, email/name changes)

import datetime
import os
import requests

# TODO: Use CSV file instead and define function to convert into list of tuples
# Constant describing each monitored URL, website name, and owner email
MONITORED_SITES = [
    ["https://github.com/", "Github", "test@hotmail.com"],
    ["http://github.com/", "Github HTTP", "test@hotmail.com"],
                   ]

# File location of master log which details check and change history
master_log = "data/master_log.txt"


def get_timestamp():
    """Return the current time as a string in the form 'day-month-year, hour:minute'"""
    time = datetime.datetime.now()
    return time.strftime("%d-%m-%y, %H:%M")


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
        for site_check in self.sites:
            site_check[0] = site_check[0].strip()
            site_check[2] = site_check[2].strip()

        # If /data doesn't exist yet, create directory and master log file
        if not os.path.isdir('data'):
            os.mkdir('data')
            f = open(master_log, 'x')
            f.close()

    def check_all(self):
        """Iterate over all RobotsCheck instances to run change checks and reports."""
        with open(master_log, 'a') as f:
            f.write("{}: Starting checks on {} sites.\n".format(get_timestamp(), len(self.sites)))

        no_change, change, first, err = 0, 0, 0, 0
        for site_check in self.sites:
            url, name, email = site_check
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

        print("All checks and reports complete.")
        with open(master_log, 'a') as f:
            f.write("{}: Checks complete. No change: {}. Change: {}. First run: {}. Error: {}."
                    "\n".format(get_timestamp(), no_change, change, first, err))


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
        dir (str): the name of the directory containing website data.
        old_file (str): the file containing the previous check robots.txt content.
        old_content (str): the previous check robots.txt content.
        new_file (str): the file containing the latest check robots.txt content.
        old_content (str): the latest check robots.txt content.

    """

    def __init__(self, url):
        self.url = url
        self.first_run = False
        self.err_message = None
        self.file_change = False
        if self.url[4] == 's':
            self.dir = self.url[8:-1]
        else:
            self.dir = self.url[7:-1]
        self.log_file = "test log"
        self.old_file = "test old file"
        self.old_content = "test old content"
        self.new_file = "test new file"
        self.new_content = "test new content"
        # TODO: Check if site directory exists and create directory and site log if not

    def run_check(self):
        """Update the robots.txt file records and check for changes.

        Returns:
            The class instance representing the completed robots.txt check.
        """
        print("Method run_check called.")
        try:
            extraction = self.download_robotstxt()
            print("Successful robots.txt extraction for {}.".format(self.url))
        except:
            # Catch all to prevent fatal error; terminate current check if download unsuccessful
            # Specific errors caught in download_robotstxt() and logged in self.error
            print("Exception raised by download_robotstxt() for {}.".format(self.url))
            return self

        self.update_records(extraction)
        if not self.first_run:
            self.check_diff()

        return self

    def download_robotstxt(self):
        """Extract and return the current content (str) of the robots.txt file."""
        robots_url = self.url + "robots.txt"
        print("Fetching robots.txt file")
        try:
            r = requests.get(robots_url, allow_redirects=False, timeout=40)
        except requests.exceptions.Timeout:
            self.err_message = "{} timed out before sending a valid response.".format(robots_url)
            print(self.err_message)
            raise
        except requests.exceptions.ConnectionError as e:
            self.err_message = "There was a connection error when accessing {}. " \
                "TYPE: {} DETAILS: {}".format(robots_url, type(e), e)
            print(self.err_message)
            raise
        # Unexpected errors
        except Exception as e:
            self.err_message = "Error occurred when requesting {} during download_robotstxt(). " \
                               "TYPE: {} DETAILS: {}".format(robots_url, type(e), e)
            print(self.err_message)
            raise

        if r.status_code != 200:
            self.err_message = "{} returned a {} status code.".format(robots_url, r.status_code)
            print(self.err_message)
            raise requests.exceptions.HTTPError

        print("Returning response text for {}".format(robots_url))
        return r.text

    def update_records(self, new_extraction):
        """Update the files containing the current and previous robots.txt content.

        If the robots.txt file has been checked previously (first_run=False),
        overwrite old_file with the contents of new_file (from the previous check).
        Then, add the new robots.txt extraction content to new_file.

        Args:
            new_extraction (str): the current content of the robots.txt file.

        """
        # TODO: complete method
        # TODO: Check if files exist, if not then create and set first_run = True
        # Change to else
        if not self.first_run:
            # Copy the contents of new_file and overwrite the contents of old_file
            # Update old_content
            pass

        # Overwrite the contents of new_file with new_extraction
        # Update new_content
        pass

    def check_diff(self):
        """Check for file differences and update self.file_change."""
        if self.old_content != self.new_content:
            self.file_change = True


class Report:
    """Reports the robots.txt check result for a single website.

    Attributes:
        url (str): the absolute URL of the website homepage, with a trailing slash.
        dir (str): the name of the directory containing website data.
        name (str): the website's name identifier.
        email (str): the email address of the owner, who will receive alerts.
        timestamp (str): the (approximate) time of the check.
    """
    # TODO: complete class and method documentation
    def __init__(self, website, name, email):
        self.url = website.url
        self.dir = website.dir
        self.name = name
        self.email = email
        self.timestamp = get_timestamp()

    def create_snapshot(self):
        # TODO: populate method to record a file snapshot (called for first run and change)
        pass

    def send_email(self, subject, body):
        # TODO: populate method to send email (email content generated by subclass methods)
        pass


class NoChangeReport(Report):
    # TODO: Complete documentation and add methods
    # TODO: Add method to print results to the console
    # TODO: Add method to update the master log
    # TODO: Add method to update the website log
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super

    def create_reports(self):
        # TODO: populate method
        # Update the website log
        # Update the master log
        # Print result to the console
        print("Method create_reports called.")
        return self


class ChangeReport(Report):
    # TODO: Complete documentation and add methods
    # TODO: Add method to print results to the console
    # TODO: Add method to update the master log
    # TODO: Add method to update the website log
    # TODO: Add method to write an email report
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super
        self.old_content = website.old_content
        self.new_content = website.new_content

    def create_reports(self):
        # TODO: populate method
        # Update the website log
        # Update the master log
        # Print result to the console
        # Record snapshot
        # Write and send email
        print("Method create_reports called.")
        return self


class FirstRunReport(Report):
    # TODO: Complete documentation and add methods
    # TODO: Add method to print results to the console
    # TODO: Add method to update the master log
    # TODO: Add method to update the website log
    # TODO: Add method to write an email report
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super
        self.new_content = website.new_content

    def create_reports(self):
        # TODO: populate method
        # Update the website log
        # Update the master log
        # Print result to the console
        # Record snapshot
        # Write and send email
        print("Method create_reports called.")
        return self


class ErrorReport(Report):
    # TODO: Complete documentation and add methods
    # TODO: Add method to print results to the console
    # TODO: Add method to update the master log
    # TODO: Add method to update the website log
    # TODO: Add method to write an email report
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super
        self.err_message = website.err_message

    def create_reports(self):
        # TODO: populate method
        # Update the website log
        # Update the master log
        # Print result to the console
        # Write and send email
        print("Method create_reports called.")
        return self


if __name__ == "__main__":
    RunChecks(MONITORED_SITES).check_all()
