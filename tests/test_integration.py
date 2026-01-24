def test_app_runs_without_crash(monkeypatch):
    """End-to-end test in the test directory.
    
    Tests the absence of fatal errors but doesn't inspect 
    any specific functionality or non-fatal errors.
    """
    # Use modified testing variables in config.py
    monkeypatch.setenv("ROBOTS_MONITOR_ENV", "test")

    from app.main import main
    main()
