import abc # Import the 'abc' module for abstract base classes functionality
from typing import List, Dict

class LogWriter(abc.ABC):
    """Abstract base class for log writers."""
    def __init__(self, log_file_location: str):
        self.log_file_location = log_file_location

    @abc.abstractmethod
    def write_to_log(self, log_entries: List[Dict]):
        """
        Write a single log entry to the log file.

        Args:
            log_entry: The log entry to write.
        Raises:
            NotImplementedError: If not implemented by a concrete subclass.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def close(self):
        """
        Close the log writer.

        Raises:
            NotImplementedError: If not implemented by a concrete subclass.
        """
        raise NotImplementedError