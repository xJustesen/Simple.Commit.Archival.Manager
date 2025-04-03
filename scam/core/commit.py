import json
import os
import shutil
from datetime import datetime


class CommitManager:
    def __init__(self, scam_dir: str = ".scam"):
        self.scam_dir = scam_dir
        self.log_file = os.path.join(self.scam_dir, "log.jsonl")
        if not os.path.exists(self.scam_dir):
            os.makedirs(self.scam_dir)

    def commit(self, filename: str, message: str) -> str:
        """
        Commit a file to the scam directory with a timestamp and message.
        The file is copied to the scam directory with a new name that includes
        the timestamp and the original filename. The commit is logged in a
        JSONL file in the scam directory.

        :param str filename: The path to the file to commit.
        :param str message: The commit message.
        :raises FileNotFoundError: If the file does not exist.
        :return str: The path to the committed file in the scam directory.
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File '{filename}' does not exist.")

        timestamp = self.get_timestamp()
        base_name = os.path.basename(filename)
        committed_name = f"{timestamp}__{base_name}"
        committed_path = os.path.join(self.scam_dir, committed_name)

        shutil.copy2(filename, committed_path)

        self._log_commit(timestamp, message, base_name, committed_name)
        return committed_path

    @staticmethod
    def get_timestamp() -> str:
        """
        Get the current timestamp in the format YYYY-MM-DDTHH-MM-SS.

        :return str: The current timestamp.
        """
        return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    def _log_commit(self, timestamp: str, message: str, original_filename: str, committed_filename: str):
        # Log the commit details in a JSONL file. Each line is a JSON object with the commit details.
        # The log file is created if it does not exist.
        entry = {
            "timestamp": timestamp,
            "message": message,
            "original_filename": original_filename,
            "committed_filename": committed_filename,
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
