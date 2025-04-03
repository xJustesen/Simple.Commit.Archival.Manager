from abc import ABC, abstractmethod
from datetime import datetime


class PushStrategy(ABC):
    @abstractmethod
    def push(self, files: list[str], scam_dir: str) -> list[str]:
        """Performs the push. Returns log lines describing the action."""
        pass


class MockPushStrategy(PushStrategy):
    """
    A mock push strategy that simulates the push process.
    """

    def push(self, files, scam_dir) -> list[str]:
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        return [f"[{timestamp}] Pushed: {f}" for f in files] if files else [f"[{timestamp}] Nothing to push."]
