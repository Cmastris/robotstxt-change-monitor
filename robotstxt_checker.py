""" Monitor and report changes across multiple website robots.txt files."""
# TODO: Complete core functionality
# TODO: Write tests and fix bugs
# TODO: Provide more details about changes using difflib
# TODO: Allow for multiple emails per website
# TODO: Consider using a DB to manage monitored sites (creation, deletion, email/name changes)


# TODO: Use CSV file instead and init in ManageWebsiteChecks
# Constant describing each monitored URL, website name, and owner email
MONITORED_SITES = [
    ("https://www.example.com/", "Test Site", "test@hotmail.com"),
                   ]

# File location of master log which details check and change history
# TODO: Add master log location, create file if it doesn't exist (check using os.path)
master_log = None


class RunChecks:
    """Run robots.txt checks across websites."""
    # TODO: complete class and method documentation

    def __init__(self, sites):
        """Initialise RobotsCheck instances and store them in a list."""
        self.sites = sites

    def check_all(self):
        """Iterate over all RobotsCheck instances to run change checks and reports."""
        for site_check in self.sites:
            url, name, email = site_check
            check = RobotsCheck(url)
            check.run_check()
            print("Robots.txt checked: " + check.url)
            # TODO: Init appropriate report subclass based on check attributes
            if check.err_message:
                report = ErrorReport(check, name, email)
            elif check.first_run:
                report = FirstRunReport(check, name, email)
            elif check.file_change:
                report = ChangeReport(check, name, email)
            else:
                report = NoChangeReport(check, name, email)

            report.create_reports()
            print("Report complete: " + report.url)

        print("All checks and reports complete.")


class RobotsCheck:
    """Check a website's robots.txt file and compare to the previous recorded file.

    This class is used to download the robots.txt file, update the robots.txt records
    (current file and file downloaded during the previous run), and check for
    any differences between the records. The results (change, no change, first run, err)
    are assigned as attributes and the instance is returned.

    Attributes:
        url (str): the absolute URL of the website homepage, with a trailing slash.
        err_message (None, str): None by default, otherwise a description of the error.
        file_change (bool): if the robots.txt file has changed since the previous record.
        first_run (bool): if this is the first recorded check of the website's file.
        old_file (str): the file containing the previous check robots.txt content.
        old_content (str): the previous check robots.txt content.
        new_file (str): the file containing the latest check robots.txt content.
        old_content (str): the latest check robots.txt content.

    """

    def __init__(self, url):
        self.url = url
        self.err_message = None
        self.file_change = False
        # TODO: Try to assign existing files to self
        # Otherwise, if they don't exist, create/assign files and set first_run = True
        self.first_run = False
        self.log_file = "test log"
        self.old_file = "test old file"
        self.old_content = "test old content"
        self.new_file = "test new file"
        self.new_content = "test new content"

    def run_check(self):
        """Update the robots.txt file records and check for changes.

        Returns:
            The class instance representing the completed robots.txt check.
        """
        print("Method run_check called.")
        try:
            extraction = self.download_robotstxt()
        except:  # TODO: Add specific errors and messages
            self.err_message = "something"
            return self

        self.update_records(extraction)
        if not self.first_run:
            self.check_diff()

        return self

    def download_robotstxt(self):
        """Extract and return the current content (str) of the robots.txt file."""
        # TODO: complete method
        # Use Beautiful Soup or Requests
        # Raise any HTTP/extraction errors
        return "Test extraction"

    def update_records(self, new_extraction):
        """Update the files containing the current and previous robots.txt content.

        If the robots.txt file has been checked previously (first_run=False),
        overwrite old_file with the contents of new_file (from the previous check).
        Then, add the new robots.txt extraction content to new_file.

        Args:
            new_extraction (str): the current content of the robots.txt file.

        """
        # TODO: complete method
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
        name (str): the website's name identifier.
        url (str): the absolute URL of the website homepage, with a trailing slash.
        email (str): the email address of the owner, who will receive alerts.
    """
    # TODO: complete class and method documentation
    # TODO: Add method to get date/time

    def __init__(self, website, name, email):
        self.url = website.url
        self.name = name
        self.email = email

    def send_email(self, subject, body):
        # TODO: populate method
        # Email content generated by subclass methods
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
