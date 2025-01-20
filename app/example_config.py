# The absolute path of the project root directory
PATH = r'C:\Users\ExampleUser\python\robotstxt-change-monitor' + '\\'

# The location of the monitored sites CSV file
# Refer to the main.py `sites_from_file()` function documentation for more details
MONITORED_SITES = PATH + "monitored_sites.csv"

# The file location of the main log .txt file
MAIN_LOG = PATH + "data/main_log.txt"

# The email address of the program administrator, included as a point of contact in all emails
# This address will receive a summary report every time checks are run
ADMIN_EMAIL = "ADMIN_EMAIL@example.com"

# The email address that will send emails
SENDER_EMAIL = "SENDER_EMAIL@example.com"

# Toggle ('True' or 'False') whether emails are enabled (both site admins and the program admin)
# This requires implementing email sending functionality in the emails.py `send_emails()` function
EMAILS_ENABLED = False

# User-agent string sent in request headers
USER_AGENT = "Robots.txtMonitor/1.0"
