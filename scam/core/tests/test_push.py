from scam.core.push import MockPushStrategy, PushManager


# Test 1: push logs file actions with mock strategy
def test_pushmanager_logs_pushed_files(tmp_path):
    scam_dir = tmp_path / ".scam"
    scam_dir.mkdir()

    # Create dummy committed files
    (scam_dir / "2025-04-03T10-00-00__file1.txt").write_text("File 1 contents")
    (scam_dir / "2025-04-03T10-01-00__file2.txt").write_text("File 2 contents")

    pm = PushManager(scam_dir=str(scam_dir), strategy=MockPushStrategy())
    pm.push()

    log_file = scam_dir / "push.log"
    assert log_file.exists()

    with open(log_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 2
    assert all("Pushed: " in line for line in lines)


# Test 2: push when there are no committed files
def test_pushmanager_logs_nothing_to_push(tmp_path):
    scam_dir = tmp_path / ".scam"
    scam_dir.mkdir()

    pm = PushManager(scam_dir=str(scam_dir), strategy=MockPushStrategy())
    pm.push()

    log_file = scam_dir / "push.log"
    assert log_file.exists()

    with open(log_file, "r") as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert "Nothing to push" in lines[0]
