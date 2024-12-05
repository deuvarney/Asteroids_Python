from .log_writer import LogWriter
import threading
import json

class ThreadingBasedLogger(LogWriter):
    """
    Logger that uses a separate thread to write to the log file.
    """
    def __init__(self, log_file_location):
        super().__init__(log_file_location)
        self.thread = None

    def write_to_log(self, log_entries):
        self.thread = threading.Thread(target=self._write_log, args=(log_entries,))
        self.thread.start()

    def _write_log(self, log_entries):
        with open(self.log_file_location, 'a') as f:
            for entry in log_entries:
                json.dump(entry, f)
                f.write('\n')

    def close(self):
        if self.thread is not None:
            self.thread.join()
