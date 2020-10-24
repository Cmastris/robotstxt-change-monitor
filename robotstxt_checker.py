""" Download and report changes in multiple website robots.txt files.

TODO: Complete core functionality.
TODO: Develop email alerts.
TODO: Provide more details about changes using difflib.
TODO: Allow for multiple emails per website.
TODO: Add noindex checks for priority pages.
TODO: (Maybe) Use a database to manage monitored sites (creation, deletion, email changes).
"""

# TODO: Import Beautiful Soup for scraping


# List of tuples containing each monitored website name, URL, and owner email
# TODO: use CSV file instead
monitored_sites = [("https://www.example.com/", "Test Site", "test@hotmail.com"),
                   ]

# File location of master log which details check and change history
master_log = None


class ManageWebsiteChecks:
    """Manages all monitored website checks."""
    def __init__(self, sites):
        """Initialise RobotsCheck instances and store them in a list."""
        self.sites = sites

    def check_all(self):
        """Iterate over all RobotsCheck instances to run change checks and reports."""
        for site_check in self.sites:
            url, name, email = site_check
            # TODO: record date/time and pass to report
            check = RobotsCheck(url)
            check.run_check()
            print("Robots.txt checked: " + check.url)
            # TODO: Init appropriate report subclass based on check attributes
            if check.err_message:
                pass
            elif check.first_run:
                pass
            elif check.file_change:
                report = ChangeReport(check, name, email)
            else:
                report = NoChangeReport(check, name, email)

            report.create_reports()
            print("Reports complete: " + report.url)

        print("All checks and reports complete.")


class RobotsCheck:
    """Checks the robots.txt file of a single website.

    This class is used to download the robots.txt file, update the robots.txt records
    (current file and file downloaded during the previous run), and check for
    any differences between the records. The results (change, no change, first run, err)
    are assigned as attributes and the instance is returned.

    TODO: complete documentation
    Attributes:
        url (str): the absolute URL of the website homepage, with a trailing slash.
        first_run (): if this is the first check of the website's file.
    """

    def __init__(self, url):
        self.url = url
        self.err_message = None
        self.file_change = False
        # Try to assign existing files to self
        # Otherwise, if they don't exist, create/assign files and set first_run = True
        self.first_run = False
        self.log_file = "test log"
        self.old_file = "test old file"
        self.old_content = "test old content"
        self.new_file = "test new file"
        self.new_content = "test new content"

    def run_check(self):
        """Update robots.txt records and check for changes."""
        print("Method run_check called.")
        try:
            extraction = self.download_robotstxt()
        except:  # Add specific errors and messages
            self.err_message = "something"
            return self

        self.update_records(extraction)
        if not self.first_run:
            self.check_diff()

        return self

    def download_robotstxt(self):
        """Extract the contents of the current robots.txt file."""
        # Use Beautiful Soup or Requests
        # Raise any HTTP/extraction errors
        return "Test extraction"

    def update_records(self, new_extraction):
        """Update the robots.txt record files."""
        if not self.first_run:
            # Copy the contents of new_file and overwrite the contents of old_file
            pass

        # Overwrite the contents of new_file with new_extraction
        pass

    def check_diff(self):
        """Check for differences between the old and new file."""
        # Check for differences and set self.file_change to True if change
        pass


class WebsiteReport:
    """Reports the robots.txt check result for a single website.

    TODO: complete documentation
    TODO: Create subclasses for no change, change, first run, and error
    Attributes:
        name (str): the website's name identifier.
        url (str): the absolute URL of the website homepage, with a trailing slash.
        email (str): the email address of the owner, who will receive alerts.
    """
    def __init__(self, website, name, email):
        self.url = website.url
        self.file_change = website.file_change
        self.first_run = website.first_run
        self.err_message = website.err_message
        self.name = name
        self.email = email

    def create_reports(self):
        # Update the website log
        # Print result to the console
        # Update the master log
        print("Method create_reports called.")
        return self


class NoChangeReport(WebsiteReport):
    # TODO: Complete docs and class
    def __init__(self, website, name, email):
        WebsiteReport.__init__(self, website, name, email)


class ChangeReport(WebsiteReport):
    # TODO: Complete docs and class
    def __init__(self, website, name, email):
        WebsiteReport.__init__(self, website, name, email)
        self.old_content = website.old_content
        self.new_content = website.new_content


def run_checks():
    """Initialise and check all robots.txt files for changes since last run."""
    ManageWebsiteChecks(monitored_sites).check_all()


if __name__ == "__main__":
    print("__name__ equals __main__")
    run_checks()
