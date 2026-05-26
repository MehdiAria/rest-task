from workers.tasks import recovery_scan

def test_recovery_scan_runs() -> None:
    assert isinstance(recovery_scan(), int)
