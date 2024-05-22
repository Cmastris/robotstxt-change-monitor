# Robots.txt Monitor
### Never miss a robots.txt change again.
An accidental "Disallow: /" can happen to anyone, but it doesn't need to linger unnoticed.
Whether you're a webmaster, developer, or SEO, this tool can help you quickly discover unwelcome robots.txt changes.

## Contents
- **[Key features](#key-features)**
- **[How it works](#how-it-works)**
- **[Setup](#setup)**
- **[FAQs](#faqs)**

## Key features
- **Easily check results.** Robots.txt check results are printed, logged, and optionally emailed (see below).
- **Snapshots.** The robots.txt content is saved following the first check and whenever the file changes. 
- **Diffs.** A diff file is created after every change to help you view the difference at a glance. 
- **Email alerts (optional).** Automatically notify site watchers about changes and send a summary email to the tool admin after every run. No need to run and check everything manually.
- **Designed for reliability.** Errors such as a mistyped URL or connection issue are handled gracefully and won't break other robots.txt checks. Unexpected issues are caught and logged.
- **Comprehensive logging.** Check results and any errors are recorded in a main log and website log (where relevant), so you can refer back to historic data and investigate if anything goes wrong.

## How it works
1. A /data directory is created/accessed to store robots.txt file data and logs.
2. All monitored robots.txt files are downloaded and compared against the previous version.
3. The check result is logged/printed and categorised as either "first run", "no change", "change", or "error".
4. Timestamped snapshots ("first run" and "change") and diffs ("change") are saved in the relevant site directory.
5. If enabled, site-specific email alerts are sent out ("first run", "change", and "error").
6. If enabled, an administrative email alert is sent out detailing overall check results and any unexpected errors.


## Setup

### Environment
1. Save the project to a new directory (locally or on a server).
2. Locate the `example_config.py` file in the `/app/` directory and create a new `config.py` file in the same directory. Copy in the contents of `example_config.py` (this will be filled in properly later).
3. Install all requirements using the [Pipfile](/Pipfile). For more information, please refer to the [Pipenv documentation](https://pipenv.pypa.io/en/latest/).


### Emails disabled, local
*The quickest setup, suitable if you plan to run the tool on your local machine for sites that you're personally monitoring.*
1. Open `config.py` and set `EMAILS_ENABLED = False`.
2. Create a CSV file named "monitored_sites.csv" in the same directory as the .py files.
3. Add a header row (with column labels) and details of sites you want to monitor, as defined below:
- URL (column 1): the absolute URL of the website homepage, with a trailing slash.
- Name (column 2): the website's name identifier (letters/numbers only).
- Email (column 3): the email address of the site admin, who will receive alerts.

URL | Name | Email
----|------|-----
https://github.com/ | Github | example@gmail.com

4. Run `main.py`. The results will be printed and data/logs saved in a newly created /data subdirectory. 
   
5. Run `main.py` again whenever you want to re-check the robots.txt files. It's recommended that you check the print output or main log after every run, or at least after new sites are added, in case of unexpected errors.

### Emails enabled, local
*Slightly more setup, suitable if you plan to run the tool on your local machine for yourself and others.*
1. Add the required details to `config.py`:
- Set `ADMIN_EMAIL` to equal an email address which will receive the summary report.
- Set `SENDER_EMAIL` to equal a Gmail address which will send all emails. [Less secure app access](https://support.google.com/accounts/answer/6010255) must be enabled. It's strongly recommended that you set up a new Google account for this. 
- Ensure `EMAILS_ENABLED = True`.
2. Create a CSV file named "monitored_sites.csv" in the same directory as the .py files.
3. Add a header row (with column labels) and details of sites you want to monitor, as defined below:
- URL (column 1): the absolute URL of the website homepage, with a trailing slash.
- Name (column 2): the website's name identifier (letters/numbers only).
- Email (column 3): the email address of the site admin, who will receive alerts.

URL | Name | Email
----|------|-----
https://github.com/ | Github | example@gmail.com

4. Open `main.py`, uncomment `emails.set_email_login()`, and save the file:
```
if __name__ == "__main__":
    # Use set_email_login() to save login details on first run or if email/password changes:
    emails.set_email_login()
    main()
```

5. Run `main.py`. The results will be printed and data/logs saved in a newly created /data subdirectory. You will be prompted to enter your `SENDER_EMAIL` password, which will be saved for future use via [Keyring](https://pypi.org/project/keyring/).
   
6. Re-comment `emails.set_email_login()` and save the file:
```
if __name__ == "__main__":
    # Use set_email_login() to save login details on first run or if email/password changes:
    # emails.set_email_login()
    main()
```

7. Run `main.py` again whenever you want to re-check the robots.txt files. It's recommended that you check the main log after every run, or at least after new sites are added, in case of unexpected errors.

### Emails enabled, server cron job (recommended)
*More setup for a fully automated experience.*

Refer to "Emails enabled, local", with the following considerations:
- If [Keyring](https://pypi.org/project/keyring/) isn't compatible with your server: 
    - Open `emails.py`and locate the following line within `send_emails()`: `with yagmail.SMTP(config.SENDER_EMAIL) as server:`
    - Edit this line to include the sender email password as the second argument of `yagmail.SMTP`: `with yagmail.SMTP(config.SENDER_EMAIL, SENDER_EMAIL_PASSWORD) as server:`
    - Open `main.py` and ensure `emails.set_email_login()` is commented out.
    
- You may need to edit the shebang line at the top of `main.py`.
- You may need to edit the `PATH` variable in `config.py`.
- It's strongly recommended that you test the cron job implementation is working correctly. To test that changes are being correctly detected/reported, you can edit `new_file.txt` within the `program_files` subdirectory of a monitored site directory. On the following run, a change (versus the edited, "old" file) should be reported.


## FAQs

### How can I ask questions, report bugs, or provide feedback?
Feel free to create an issue or open a new discussion.

### What should I do if there's a connection error, non-200 status, or inaccurate content?
If the tool repeatedly reports an error or inaccurate robots.txt content for a site, but you're able to view the file via your browser, this is likely due to an invalid URL format or the tool being blocked in some way. 

Try the following: 
1. Check that the monitored URL is in the correct format.
2. Request that your IP address (or your server's IP address) is whitelisted.
3. Try adjusting the `USER_AGENT` string (e.g. to spoof a common browser) in `config.py`.
4. Troubleshoot with your IT/development teams.

### Is this project in active development?
There are no further updates/features planned, and I'm not looking for contributions, but I'll be happy to fix any (significant) bugs.
