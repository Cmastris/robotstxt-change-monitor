# Robots.txt Monitor - Quickly Discover Unwanted Changes
**Never miss a robots.txt change again.** 
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
5. If enabled, an administrative email alert is sent out detailing overall check results and any unexpected errors encountered.


## Setup
TODO

## FAQs
TODO
Questions/contact, activate development, and contributions