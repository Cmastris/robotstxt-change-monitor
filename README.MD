# Robots.txt Monitor <!-- omit in toc -->

### Never miss a robots.txt change again. <!-- omit in toc -->
An accidental "Disallow: /" can happen to anyone, but it doesn't need to remain unnoticed.
Whether you're a webmaster, developer, or SEO, this tool can help you quickly discover unwelcome robots.txt changes.

## Contents <!-- omit in toc -->

- [Key features](#key-features)
- [How it works](#how-it-works)
- [Setup](#setup)
  - [General setup (all setup options)](#general-setup-all-setup-options)
  - [Setup options](#setup-options)
    - [Local with emails disabled](#local-with-emails-disabled)
    - [Local with emails enabled](#local-with-emails-enabled)
    - [Server with emails enabled](#server-with-emails-enabled)
  - [Testing](#testing)
- [FAQs](#faqs)
  - [How can I ask questions, report bugs, or provide feedback?](#how-can-i-ask-questions-report-bugs-or-provide-feedback)
  - [What should I do if there's a connection error, non-200 status, or inaccurate content?](#what-should-i-do-if-theres-a-connection-error-non-200-status-or-inaccurate-content)
  - [Is this project in active development?](#is-this-project-in-active-development)


## Key features
- **Easily check results.** Robots.txt check results are printed to the screen, logged in files, and optionally emailed (refer to the [setup instructions](#setup)).
- **Snapshots.** The robots.txt content is saved following the first check and whenever the file changes. 
- **Diffs.** A diff file is created after every change to help you view the difference at a glance. 
- **Comprehensive logging.** Check results and any errors are recorded in a main log and website log (where relevant), so you can refer back to historic data and investigate if anything goes wrong.
- **Designed for reliability.** Errors such as a mistyped URL or connection issue are handled gracefully and won't break other robots.txt checks. Unexpected issues are caught and logged.


## How it works
1. A /data/ directory is created/accessed to store robots.txt file data and logs.
2. All monitored robots.txt files are downloaded and compared against the previous version.
3. The check result is logged/printed and categorised as either "first run", "no change", "change", or "error".
4. Timestamped snapshots ("first run" and "change") and diffs ("change") are saved in the relevant site directory.
5. If enabled, site-specific email alerts are sent out ("first run", "change", and "error").
6. If enabled, an administrative email alert is sent out detailing overall check results and any unexpected errors.


## Setup

### General setup (all setup options)
1. [Clone a local copy of this repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your computer and/or a server, depending on your chosen setup (detailed below).
2. Create a new `config.py` file in the /app/ subdirectory. Copy the contents of `example_config.py` into `config.py`. Edit the `PATH` variable to reference the location of the project root directory.
3. Install all requirements (specific versions of Python and packages) using the [uv package manager](https://docs.astral.sh/uv/guides/projects/) or another tool of your choice (based on the [pyproject file](/pyproject.toml)).
4. Create a "monitored_sites.csv" file in the top-level directory (which contains the README file). Populate the file with a header row (column labels) and details of the website(s) you want to monitor, as defined below:
- URL (column 1): the absolute URL of the website homepage, with a trailing slash.
- Name (column 2): the website's name identifier (letters/numbers only).
- Email (column 3): the email address of the website monitor, i.e. the person who will receive email notifications of errors/changes (if enabled). Note: an email header row label is required but email addresses don't need to be populated unless emails are enabled (detailed below).

URL | Name | Email
----|------|-----
https://github.com/ | Github | person@example.com
https://www.example.com/ | Example | another.person@example.com

### Setup options

#### Local with emails disabled
*The quickest setup, suitable if you plan to run the tool on your computer for sites that you're personally monitoring (or are otherwise willing to notify other people about changes/errors manually).*

1. Run `main.py` (in the /app/ subdirectory). The results should be printed to the console and the data/logs should be saved in a newly created /data/ directory.
   
2. Run `main.py` again whenever you want to re-check the robots.txt files. It's recommended that you check the print output or main log regularly, or at least after new sites are added, in case there are any unexpected errors.

#### Local with emails enabled
*More setup, suitable if you plan to run the tool on your computer for yourself and others.*

1. Edit `config.py` (in the /app/ subdirectory):
- Set `ADMIN_EMAIL` to equal an email address that will receive the summary report.
- Set `SENDER_EMAIL` to equal an address that will send all emails (unless this isn't required in your email sending functionality, e.g. if using a third-party email service).
- Set `EMAILS_ENABLED` to equal `True`.

2. Implement email sending functionality in `emails.py` (in the /app/ subdirectory) within the `send_emails()` function stub. The function stub receives all pre-created email content (as defined in the function docstring) and includes generic exception (uncaught error) handling, but it will be up to you to implement the sending of emails using your chosen package/library/email service.

3. Run `main.py`. The results should be printed to the console and the data/logs should be saved in a newly created /data/ directory. Check that emails are being sent/received as intended.

4. Run `main.py` again whenever you want to re-check the robots.txt files. It's recommended that you check the print output or main log regularly, or at least after new sites are added, in case there are any unexpected errors.

#### Server with emails enabled
*The most setup for a fully automated experience.*

Refer to ["Local with emails enabled"](#local-with-emails-enabled), with the following considerations:
- You may need to refer to your server's documentation for details of setting up a cron job to regularly run `main.py`.
- You may need to edit the shebang line at the top of `main.py`.

### Testing
In general, errors will be reported/logged if anything is clearly breaking. However, it's a good idea to review the saved website(s) data (in the /data/ directory) after running the tool for the first and second time, to check that everything is looking correct.


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
There are no major updates/features planned and I'm not looking for any substantial contributions (but you're welcome to fork your own version).

However, I plan to maintain the project by periodically upgrading to newer (actively supported) versions of Python/Requests and fixing any significant bugs.