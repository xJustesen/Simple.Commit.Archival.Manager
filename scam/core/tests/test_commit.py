import json
import os

import pytest

from scam.core.commit import CommitManager


def test_commit_creates_versioned_file_and_log(tmp_path):
    # Create a temp file to commit
    orignal_file_name = "sample.txt"
    sample_file = tmp_path / orignal_file_name
    sample_file.write_text("This is a test file.")

    scam_dir = tmp_path / ".scam"
    cm = CommitManager(scam_dir=str(scam_dir))

    message = "Test commit message"
    committed_path = cm.commit(str(sample_file), message)

    # Check file exists in .scam directory
    assert os.path.isfile(committed_path)
    assert committed_path.startswith(str(scam_dir))

    # Check log file exists
    log_path = scam_dir / "log.jsonl"
    assert log_path.exists()

    # Check log entry is correct
    with open(log_path, "r", encoding="utf-8") as log_file:
        lines = log_file.readlines()
        assert len(lines) == 1
        entry = json.loads(lines[0])
        assert entry["message"] == message
        assert entry["original_filename"] == orignal_file_name
        assert entry["committed_filename"].endswith("__sample.txt")
        assert "timestamp" in entry


def test_commit_raises_error_on_missing_file(tmp_path):
    cm = CommitManager(scam_dir=str(tmp_path / ".scam"))
    with pytest.raises(FileNotFoundError):
        cm.commit("non_existent_file.txt", "This file does not exist")


def test_multiple_commits_append_to_log_and_create_files(tmp_path):
    # Setup
    sample_file_1 = tmp_path / "file1.txt"
    sample_file_2 = tmp_path / "file2.txt"
    sample_file_1.write_text("Content of file 1.")
    sample_file_2.write_text("Content of file 2.")

    scam_dir = tmp_path / ".scam"
    cm = CommitManager(scam_dir=str(scam_dir))

    # Commit both files
    cm.commit(str(sample_file_1), "First commit")
    cm.commit(str(sample_file_2), "Second commit")

    # Check that both files were created
    committed_files = list(os.listdir(scam_dir))
    committed_files = [f for f in committed_files if not f.endswith(".jsonl")]
    assert len(committed_files) == 2

    # Check log file has 2 entries
    log_path = scam_dir / "log.jsonl"
    assert log_path.exists()
    with open(log_path, "r", encoding="utf-8") as log_file:
        lines = log_file.readlines()
        assert len(lines) == 2

        entry1 = json.loads(lines[0])
        entry2 = json.loads(lines[1])

        assert entry1["message"] == "First commit"
        assert entry2["message"] == "Second commit"
        assert entry1["original_filename"] == "file1.txt"
        assert entry2["original_filename"] == "file2.txt"
