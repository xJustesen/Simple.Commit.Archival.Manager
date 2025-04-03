import os
from typing import Optional

from scam.core.strategy import MockPushStrategy, PushStrategy


class PushManager:
    def __init__(self, scam_dir: str = ".scam", strategy: Optional[PushStrategy] = None):
        """
        A class to manage the push process for SCAM files.

        :param str scam_dir: The directory where SCAM files are stored, defaults to ".scam".
        :param Optional[PushStrategy] strategy:
            The strategy to use for pushing files, defaults to MockPushStrategy.
        :raises FileNotFoundError: If the SCAM directory does not exist.
        """
        self.scam_dir = scam_dir
        self.push_log_file = os.path.join(self.scam_dir, "push.log")
        if not os.path.exists(self.scam_dir):
            raise FileNotFoundError(f"SCAM directory '{self.scam_dir}' not found.")

        self.strategy = strategy or MockPushStrategy()

    def push(self) -> None:
        """Pushes files to the remote repository using the specified strategy."""
        files_to_push = self._get_files_to_push()
        entries = self.strategy.push(files_to_push, self.scam_dir)
        self._write_push_log(entries)

    def _get_files_to_push(self):
        # Returns a list of filenames in the .scam dir that should be pushed (excluding logs).
        return [
            fname
            for fname in os.listdir(self.scam_dir)
            if fname not in {"log.jsonl", "push.log"} and os.path.isfile(os.path.join(self.scam_dir, fname))
        ]

    def _write_push_log(self, entries):
        # Appends entries to the push.log file.
        with open(self.push_log_file, "a", encoding="utf-8") as f:
            for entry in entries:
                f.write(entry + "\n")
