""" Monitor and report changes across multiple website robots.txt files."""
# TODO: Complete core functionality
# TODO: Write tests and fix bugs
# TODO: Provide more details about changes using difflib
# TODO: Allow for multiple emails per website
# TODO: Consider using a DB to manage monitored sites (creation, deletion, email/name changes)


# List of tuples containing each monitored website name, URL, and owner email
# TODO: Use CSV file instead and init in ManageWebsiteChecks
monitored_sites = [
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
    """Checks the robots.txt file of a single website.

    This class is used to download the robots.txt file, update the robots.txt records
    (current file and file downloaded during the previous run), and check for
    any differences between the records. The results (change, no change, first run, err)
    are assigned as attributes and the instance is returned.

    Attributes:
        url (str): the absolute URL of the website homepage, with a trailing slash.
        first_run (): if this is the first check of the website's file.
    """
    # TODO: complete class and method documentation

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
        """Update robots.txt records and check for changes."""
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


class Report:
    """Reports the robots.txt check result for a single website.

    Attributes:
        name (str): the website's name identifier.
        url (str): the absolute URL of the website homepage, with a trailing slash.
        email (str): the email address of the owner, who will receive alerts.
    """
    # TODO: complete class and method documentation
    # TODO: Add method to get date/time
    # TODO: Add methods to print results to the console
    # TODO: Add methods to update the master log
    # TODO: Add methods to update the website log
    # TODO: Add methods to send an email report

    def __init__(self, website, name, email):
        self.url = website.url
        self.name = name
        self.email = email

    def create_reports(self):
        # Update the website log
        # Print result to the console
        # Update the master log
        print("Method create_reports called.")
        return self


class NoChangeReport(Report):
    # TODO: Complete documentation and add methods
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super


class ChangeReport(Report):
    # TODO: Complete documentation and add methods
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super
        self.old_content = website.old_content
        self.new_content = website.new_content


class FirstRunReport(Report):
    # TODO: Complete documentation and add methods
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super
        self.new_content = website.new_content


class ErrorReport(Report):
    # TODO: Complete documentation and add methods
    def __init__(self, website, name, email):
        Report.__init__(self, website, name, email)  # TODO: Change to use super
        self.err_message = website.err_message


if __name__ == "__main__":
    RunChecks(monitored_sites).check_all()
