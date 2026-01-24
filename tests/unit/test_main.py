def test_sites_from_file(monkeypatch):
    # Use modified test path (i.e. test CSV) in config.py
    monkeypatch.setenv("ROBOTS_MONITOR_ENV", "test")

    import app.config as config
    from app.main import sites_from_file

    sites_data = sites_from_file(config.MONITORED_SITES)

    expected_sites_data = [
        ['http://www.reddit.com/', 'Reddit HTTP', ''],
        ['https://github.com/', 'GitHub', 'test1@example.com'],
        ['https://www.theguardian.com/', 'The Guardian', 'test2@example.com'],
    ]
    
    assert sites_data == expected_sites_data
