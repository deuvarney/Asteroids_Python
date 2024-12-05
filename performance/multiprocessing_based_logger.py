from .log_writer import LogWriter
import json
import multiprocessing as mp
from queue import Empty

class MultiprocessingBasedLogger(LogWriter):
    """
    Logger that uses a separate process to write to the log file.
    """
    def __init__(self, log_file_location):
        super().__init__(log_file_location)
        self.log_queue = mp.Queue()
        self.status_queue = mp.Queue()
        self.started = False
        self.process = None
        self.bootstrap_event = mp.Event()
        self.bootstrap_lock = mp.Lock()


    def write_to_log(self, log_entries):
        for entry in log_entries:
            self.log_queue.put(entry)
        self.start_logging_process()


    def start_logging_process(self):
        
        if self.started:
            return
        self.process = mp.Process(target=_write_log, args=(self.log_file_location, self.log_queue), daemon=True)
       
        self.process.daemon = True  # Ensure that the process is terminated when the main program exits.
        self.process.start()
        self.started = True
        return self.process
    
    def wait_for_bootstrap(self):
        with self.bootstrap_lock:
            if not self.bootstrap_event.is_set():
                self.bootstrap_event.wait()

    def close(self, signum = 0 , frame = 1):
        if not self.started:
           return
        self.log_queue.put(None)  # Signal end of logs
        self.process.join(timeout=1)


def _write_log(log_file_location: str, log_queue: mp.Queue):
    with open(log_file_location, 'a') as f:
        while True:
            try:
                entry = log_queue.get(timeout=1)
                if entry is None:
                    break
                json.dump(entry, f)
                f.write('\n')
                f.flush()
            except Empty:
                continue

