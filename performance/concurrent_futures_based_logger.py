from datetime import datetime
from .log_writer import LogWriter
import concurrent.futures
import json
from queue import Empty, Queue
import threading

class DaemonThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    """
    A subclass of ThreadPoolExecutor which creates all threads as daemon threads.
    This is useful when using the executor as a context manager, as it allows the
    program to exit even if the executor is still running tasks.

    Note that this executor does not support the `shutdown` method, as it is not
    necessary when using daemon threads.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._threads = set()

    def submit(self, fn, *args, **kwargs):
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            finally:
                self._threads.discard(threading.current_thread())
        thread = threading.Thread(target=wrapper, args=args, kwargs=kwargs, daemon=True)
        self._threads.add(thread)
        thread.start()
        return concurrent.futures.Future()


class ConcurrentFuturesBasedLogger(LogWriter):
    def __init__(self, log_file, ):
        super().__init__(log_file)
        self.max_workers = 1
        self.started = False

    def write_to_log(self, log_entries):
        if not self.started:
            self.queue = Queue()
            self.executor = DaemonThreadPoolExecutor(max_workers=self.max_workers)
            self.future = self.executor.submit(writer_task, self.log_file_location, self.queue)
            self.started = True

        update_log_entries = log_entries
        for log_message in update_log_entries:
            self.queue.put(log_message)

    def close(self):
        return self.closed()

    def closed(self):

        if not self.started:
            return
        
        self.queue.put(None)
        
        try:
            # Thread will hang without this timeout
            self.future.result(timeout=1)
        except Exception as e:
            print(e)
        self.executor.shutdown(wait=True)

def writer_task(filepath: str, my_queue: Queue):
    with open(filepath, 'a') as f:
        while True:
            try:
                text = my_queue.get(timeout=1)
                if text is None:
                    return "Done"
                json.dump(text, f)
                f.write('\n')
                f.flush()
            except Empty:
                continue