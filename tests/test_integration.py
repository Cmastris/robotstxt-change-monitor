import datetime
import os
import shutil


def get_main_log_summary(main_log_path):
    """Return the latest main log summary line (if no fatal error)."""
    with open(main_log_path, 'r') as f:
        main_log_summary = f.readlines()[3]

    return main_log_summary


def get_previous_minute_timestamp():
    """Return a timestamp for the previous minute."""
    previous_min = datetime.datetime.now() - datetime.timedelta(minutes=1)

    # Formatting copied from logs.get_timestamp()
    return previous_min.strftime("%Y-%m-%d %H:%M")


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

    # Retrieve the latest main log summary line (if not fatal error)
    main_log_summary = get_main_log_summary(MAIN_LOG)

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
        site_log_summary = f.readlines()[0]

    main_log_summary = get_main_log_summary(MAIN_LOG)

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
        site_log_summary = f.readlines()[0]

    main_log_summary = get_main_log_summary(MAIN_LOG)

    # Check that the most recent log summaries are for the recent run
    assert (timestamp_now in site_log_summary) or (timestamp_prev_minute in site_log_summary)
    assert (timestamp_now in main_log_summary) or (timestamp_prev_minute in main_log_summary)

    # Check that the log summaries are accurate
    expected_site_log_summary = "No change: https://github.com/. " \
                                "No changes to robots.txt file."
    assert expected_site_log_summary in site_log_summary
    
    expected_main_log_summary = "No change: 1. Change: 0. First run: 0. Error: 0."
    assert expected_main_log_summary in main_log_summary


def test_change(monkeypatch):
    """Tests behaviour/output if there is a robots.txt change."""
    # Use modified testing variables in config.py
    monkeypatch.setenv("ROBOTS_MONITOR_ENV", "test")
    
    # Import after monkeypatch
    from app.main import main
    from app.config import MAIN_LOG, PATH
    from app.logs import get_timestamp

    # Check a single site
    site_dir = PATH + "data/www.gov.uk"
    def mock_sites_from_file(file):
        return [['https://www.gov.uk/', 'Gov UK', ''],]

    monkeypatch.setattr("app.main.sites_from_file", mock_sites_from_file)

    # Delete the existing site directory to simulate a new site
    if os.path.isdir(site_dir):
        shutil.rmtree(site_dir)

    # Generate the directories & files for a first run
    main()

    # Rename the first run snapshot file to avoid an error when trying to create 
    # another (change) snapshot file with the same timestamp and to make it easier
    # to identify/check the change snapshot file
    snapshots_dir = site_dir + "/snapshots/"
    filename = os.listdir(snapshots_dir)[0]
    original_path = snapshots_dir + filename
    new_path = snapshots_dir + "Robots.txt Snapshot First Run.txt"
    os.rename(original_path, new_path)

    # Modify new_file.txt to simulate a change and then re-run the check
    with open(site_dir + "/program_files/new_file.txt", 'a') as f:
        f.write("\nSimulating some extra content in the original file!")
    
    main()  # Should detect a change, i.e. the loss of the added content

    # Log timestamps should contain the current minute or the minute before
    timestamp_now = get_timestamp()
    timestamp_prev_minute = get_previous_minute_timestamp()

    # Retrieve log summary lines
    with open(site_dir + "/log.txt", 'r') as f:
        site_log_summary = f.readlines()[0]

    main_log_summary = get_main_log_summary(MAIN_LOG)

    # Check that the most recent log summaries are for the recent run
    assert (timestamp_now in site_log_summary) or (timestamp_prev_minute in site_log_summary)
    assert (timestamp_now in main_log_summary) or (timestamp_prev_minute in main_log_summary)

    # Check that the log summaries are accurate
    expected_site_log_summary = "Change: https://www.gov.uk/. " \
                                "Change detected in the robots.txt file"
    assert expected_site_log_summary in site_log_summary
    
    expected_main_log_summary = "No change: 0. Change: 1. First run: 0. Error: 0."
    assert expected_main_log_summary in main_log_summary

    # Check that snapshot and diff files were created
    sorted_snapshots = sorted(os.listdir(snapshots_dir))

    assert "Robots.txt Snapshot.txt" in sorted_snapshots[1]
    with open(snapshots_dir + sorted_snapshots[1], 'r') as f:
        snapshot_text = f.read()

    assert len(snapshot_text) > 1

    assert "Robots.txt Diff.html" in sorted_snapshots[0]
    with open(snapshots_dir + sorted_snapshots[0], 'r', encoding='utf-8') as f:
        diff_html = f.read()

    assert len(diff_html) > 1
    assert '<span class="diff_sub">Simulating' in diff_html


def test_check_error(monkeypatch):
    """Tests behaviour/output if a robots.txt check results in an error."""
    # Use modified testing variables in config.py
    monkeypatch.setenv("ROBOTS_MONITOR_ENV", "test")
    
    # Import after monkeypatch
    from app.main import main
    from app.config import MAIN_LOG, PATH
    from app.logs import get_timestamp

    # Check a single site
    def mock_sites_from_file(file):
        return [['http://www.goodreads.com/', 'Goodreads HTTP', ''],]

    monkeypatch.setattr("app.main.sites_from_file", mock_sites_from_file)

    # Run check against HTTP URL, which should return a non-200 status code
    # and cause the check to fail (report an error)
    main()

    # Log timestamps should contain the current minute or the minute before
    timestamp_now = get_timestamp()
    timestamp_prev_minute = get_previous_minute_timestamp()

    # Retrieve log summary lines
    with open(PATH + "data/www.goodreads.com/log.txt", 'r') as f:
        site_log_summary = f.readlines()[0]

    main_log_summary = get_main_log_summary(MAIN_LOG)

    # Check that the most recent log summaries are for the recent run
    assert (timestamp_now in site_log_summary) or (timestamp_prev_minute in site_log_summary)
    assert (timestamp_now in main_log_summary) or (timestamp_prev_minute in main_log_summary)

    # Check that the log summaries are accurate
    expected_site_log_summary = "Error: http://www.goodreads.com/."
    assert expected_site_log_summary in site_log_summary
    
    expected_main_log_summary = "No change: 0. Change: 0. First run: 0. Error: 1."
    assert expected_main_log_summary in main_log_summary
