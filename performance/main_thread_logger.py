from .log_writer import LogWriter
import json

class MainThreadBasedLogger(LogWriter):
    """
    Logger that uses the main thread to write to the log file.
    """
    def __init__(self, log_file_location):
        super().__init__(log_file_location)

    def write_to_log(self, log_entries):
        with open(self.log_file_location, 'a') as f:
            for entry in log_entries:
                json.dump(entry, f)
                f.write('\n')
    
    def close(self):
        pass
