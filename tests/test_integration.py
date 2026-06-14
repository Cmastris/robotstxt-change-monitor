import datetime
import os
import shutil


def get_previous_minute_timestamp():
    """Return a timestamp for the previous minute."""
    previous_min = datetime.datetime.now() - datetime.timedelta(minutes=1)

    # Formatting copied from logs.get_timestamp()
    return previous_min.strftime("%d-%m-%y, %H:%M")


def test_app_runs_without_fatal_error(monkeypatch):
    """End-to-end test in the test directory.
    
    Tests the absence of fatal errors but doesn't inspect 
    any specific functionality or non-fatal errors.
    """
    # Use modified testing variables in config.py
    monkeypatch.setenv("ROBOTS_MONITOR_ENV", "test")

    # Import after monkeypatch
    from app.main import main
    from app.config import MAIN_LOG
    from app.logs import get_timestamp

    main()

    # Log timestamps should contain the current minute or the minute before
    timestamp_now = get_timestamp()
    timestamp_prev_minute = get_previous_minute_timestamp()

    # Retrieve main log summary line (if not fatal error)
    with open(MAIN_LOG, 'r') as f:
        main_log_summary = f.readlines()[-4]

    # Check that the most recent log summary is for the recent run
    # and that the main log summary is present
    assert (timestamp_now in main_log_summary) or (timestamp_prev_minute in main_log_summary)
    assert "Checks and reports complete" in main_log_summary


def test_first_run(monkeypatch):
    """Tests behaviour/output if the first robots.txt check."""
    # Use modified testing variables in config.py
    monkeypatch.setenv("ROBOTS_MONITOR_ENV", "test")
    
    # Import after monkeypatch
    from app.main import main
    from app.config import MAIN_LOG, PATH
    from app.logs import get_timestamp

    # Check a single site
    site_dir = PATH + "data/www.bbc.co.uk"
    def mock_sites_from_file(file):
        return [['https://www.bbc.co.uk/', 'The BBC', ''],]

    monkeypatch.setattr("app.main.sites_from_file", mock_sites_from_file)

    # Delete the existing site directory to simulate a new site
    if os.path.isdir(site_dir):
        shutil.rmtree(site_dir)

    main()

    # Log timestamps should contain the current minute or the minute before
    timestamp_now = get_timestamp()
    timestamp_prev_minute = get_previous_minute_timestamp()

    # Retrieve log summary lines
    with open(site_dir + "/log.txt", 'r') as f:
        site_log_summary = f.readlines()[-1]

    with open(MAIN_LOG, 'r') as f:
        main_log_summary = f.readlines()[-4]

    # Check that the most recent log summaries are for the recent run
    assert (timestamp_now in site_log_summary) or (timestamp_prev_minute in site_log_summary)
    assert (timestamp_now in main_log_summary) or (timestamp_prev_minute in main_log_summary)

    # Check that the log summaries are accurate
    expected_site_log_summary = "First run: https://www.bbc.co.uk/. " \
                                "First successful check of robots.txt file."
    assert expected_site_log_summary in site_log_summary
    
    expected_main_log_summary = "No change: 0. Change: 0. First run: 1. Error: 0."
    assert expected_main_log_summary in main_log_summary

    # Check that snapshot files were created
    assert "Snapshot.txt" in os.listdir(site_dir + "/snapshots")[0]
    sorted_program_files = sorted(os.listdir(site_dir + "/program_files"))
    assert sorted_program_files == ["new_file.txt", "old_file.txt"]

    with open(site_dir + "/program_files/new_file.txt", 'r') as f:
        new_file_text = f.read()

    assert len(new_file_text) > 0


def test_no_change(monkeypatch):
    """Tests behaviour/output if no robots.txt change."""
    # Use modified testing variables in config.py
    monkeypatch.setenv("ROBOTS_MONITOR_ENV", "test")
    
    # Import after monkeypatch
    from app.main import main
    from app.config import MAIN_LOG, PATH
    from app.logs import get_timestamp

    # Check a single site
    def mock_sites_from_file(file):
        return [['https://github.com/', 'GitHub', ''],]

    monkeypatch.setattr("app.main.sites_from_file", mock_sites_from_file)

    # Run check once as a baseline and again to test no change is reported
    # Extremely unlikely that the file would change between the two runs
    main()
    main()

    # Log timestamps should contain the current minute or the minute before
    timestamp_now = get_timestamp()
    timestamp_prev_minute = get_previous_minute_timestamp()

    # Retrieve log summary lines
    with open(PATH + "data/github.com/log.txt", 'r') as f:
        site_log_summary = f.readlines()[-1]

    with open(MAIN_LOG, 'r') as f:
        main_log_summary = f.readlines()[-4]

    # Check that the most recent log summaries are for the recent run
    assert (timestamp_now in site_log_summary) or (timestamp_prev_minute in site_log_summary)
    assert (timestamp_now in main_log_summary) or (timestamp_prev_minute in main_log_summary)

    # Check that the log summaries are accurate
    expected_site_log_summary = "No change: https://github.com/. " \
                                "No changes to robots.txt file."
    assert expected_site_log_summary in site_log_summary
    
    expected_main_log_summary = "No change: 1. Change: 0. First run: 0. Error: 0."
    assert expected_main_log_summary in main_log_summary
