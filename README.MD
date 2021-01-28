# Robots.txt Monitor
### Never miss a robots.txt change again.
An accidental "Disallow: /" can happen to anyone, but it doesn't need to linger unnoticed.
Whether you're a webmaster or SEO, this simple tool can help you quickly discover unwelcome robots.txt changes.

## Key features
- **Easily check results.** Robots.txt check results are printed to the console and logged.
- **Snapshots and diffs.** The robots.txt content is saved following the first check and whenever the file changes. A diff file saved after every change helps you understand the modifications at a glance. 
- **Email alerts (optional).** Want to run the monitor on a server and/or notify others about changes? No problem. Includes site-specific alerts and a summary for the tool administrator after every run. 
- **Designed for reliability.** Errors such as a mistyped URL or connection issue are handled gracefully and won't break other robots.txt checks.
- **Comprehensive logging.** The results of checks and any errors are all recorded in a main log and website log (where relevant), so you can check historic data and investigate if anything does go wrong.

## How it works
1. A /data directory is created/accessed to store robots.txt file data and logs.
2. All monitored robots.txt files are downloaded and compared against the previous version.
3. The check result is logged/printed and categorised as either "first run", "no change", "change", or "error".
4. Timestamped snapshots ("first run" and "change") and diffs ("change") are saved in the relevant site directory.
5. If enabled, site-specific email alerts are sent out ("first run", "change", and "error").
6. If enabled, an administrative email alert is sent out detailing overall check results and any unexpected errors.


## Setup

### Requirements
- [Python 3](https://www.python.org/downloads/)
- [Requests](https://pypi.org/project/requests/)
- [Yagmail](https://pypi.org/project/yagmail/)

### Emails disabled, local
*The quickest setup, suitable if you plan to run the tool on your local machine for sites that you're personally monitoring.*
1. Save the project (or just the .py files) to a new directory.
2. Open `config.py` and set `EMAILS_ENABLED = False`.
3. Create a CSV file named "monitored_sites.csv" in the same directory as the .py files.
4. Add a header row (with column labels) and details of sites you want to monitor, as defined below:
- URL (column 1): the absolute URL of the website homepage, with a trailing slash.
- Name (column 2): the website's name identifier (letters/numbers only).
- Email (column 3): the email address of the site admin, who will receive alerts.

URL | Name | Email
----|------|-----
https://github.com/ | Github | example@gmail.com

5. Run `main.py`. The results will be printed and data/logs saved in a newly created /data subdirectory. 
   
6. Run `main.py` again whenever you want to re-check the robots.txt files. It's recommended that you check the print output or main log after every run, or at least after new sites are added, in case of unexpected errors.

### Emails enabled, local
*Slightly more setup, suitable if you plan to run the tool on your local machine for yourself and others.*
1. Save the project (or just the .py files) to a new directory.
2. Add the required details to `config.py`:
- Set `ADMIN_EMAIL` to equal an email address which will receive the summary report.
- Set `SENDER_EMAIL` to equal a Gmail address which will send all emails. [Less secure app access](https://support.google.com/accounts/answer/6010255) must be enabled. It's strongly recommended that you set up a new Google account for this. 
- Ensure `EMAILS_ENABLED = True`.
3. Create a CSV file named "monitored_sites.csv" in the same directory as the .py files.
4. Add a header row (with column labels) and details of sites you want to monitor, as defined below:
- URL (column 1): the absolute URL of the website homepage, with a trailing slash.
- Name (column 2): the website's name identifier (letters/numbers only).
- Email (column 3): the email address of the site admin, who will receive alerts.

URL | Name | Email
----|------|-----
https://github.com/ | Github | example@gmail.com

5. Open `main.py`, uncomment `set_email_login()`, and save the file:
```
if __name__ == "__main__":
    # Use set_email_login() to save login details on first run or if email/password changes:
    set_email_login()
    main()
```

6. Run `main.py`. The results will be printed and data/logs saved in a newly created /data subdirectory. You will be prompted to enter your `SENDER_EMAIL` password, which will be saved for future use via [Keyring](https://pypi.org/project/keyring/).
   
7. Re-comment `set_email_login()` and save the file:
```
if __name__ == "__main__":
    # Use set_email_login() to save login details on first run or if email/password changes:
    # set_email_login()
    main()
```

8. Run `main.py` again whenever you want to re-check the robots.txt files. It's recommended that you check the main log after every run, or at least after new sites are added, in case of unexpected errors.

### Emails enabled, server cron job (recommended)
*More setup for a fully automated experience.*

Refer to "Emails enabled, local", with the following considerations:
- If [Keyring](https://pypi.org/project/keyring/) isn't compatible with your server: 
    - Open `emails.py`and locate the following line within `send_emails()`: `with yagmail.SMTP(config.SENDER_EMAIL) as server:`
    - Edit this line to include the sender email password as the second argument of `yagmail.SMTP`: `with yagmail.SMTP(config.SENDER_EMAIL, SENDER_EMAIL_PASSWORD) as server:`
    - Open `main.py` and ensure `set_email_login()` is commented out.
    
- You may need to edit the shebang line at the top of `main.py`.
- You may need to edit the `PATH` variable in `config.py`.
- It's strongly recommended that you test the cron job implementation is working correctly. To test that changes are being correctly detected/reported, you can edit `new_file.txt` within the `program_files` subdirectory of a monitored site directory. On the following run, a change (versus the edited, "old" file) should be reported.


## FAQs
TODO
Questions/contact, activate development, and contributions