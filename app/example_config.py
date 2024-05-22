# The absolute path of the project root directory
PATH = r'C:\Users\ExampleUser\python\robotstxt_checker' + '\\'

# The file location of the monitored sites CSV (see 'sites_from_file()' documentation for details)
MONITORED_SITES = PATH + "monitored_sites.csv"

# The file location of the main log .txt file
MAIN_LOG = PATH + "data/main_log.txt"

# The email address of the program administrator, included as a point of contact in all emails
# This address will receive a summary report every time checks are run
ADMIN_EMAIL = "ADMIN_EMAIL@gmail.com"

# A Gmail address which will send emails
# Less secure app access must be enabled: https://support.google.com/accounts/answer/6010255
SENDER_EMAIL = "SENDER_EMAIL@gmail.com"

# Toggle ('True' or 'False') whether emails are enabled (both site admins and the program admin)
EMAILS_ENABLED = True

# User-agent string sent in request headers
USER_AGENT = "Robots.txtMonitor/1.0"
