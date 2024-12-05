import time
import os
from datetime import date, datetime
from dotenv import load_dotenv
import functools
import inspect
from typing import Dict
import atexit 

load_dotenv()

from performance.log_writer import LogWriter

logs_dir: str = ""
log_file: str =  f'{date.today()}.json'
log_buffer: list[Dict] = []

LOGGER: LogWriter
LOG_BUFFER_SIZE: int = int(os.getenv('LOG_BUFFER_SIZE', '5000'))

CAPTURE_PERF_LOGS = os.getenv('CAPTURE_PERFORMANCE_LOGS', '') == 'true'

LOGGER_MODULE_MAIN_THREAD = 'main_thread_based_logger'
LOGGER_MODULE_MULTIPROCESSING = 'multiprocessing_logger'
LOGGER_MODULE_CONCURRENT_FUTURES = 'concurrent_futures_based_logger'
LOGGER_MODULE_THREADING = 'threading_based_logger'

# Create the path to the log directory (if it does not exist)
if not logs_dir:
    current_file = __file__
    program_dir = os.path.dirname(current_file)
    logs_dir = os.path.join(program_dir, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

def close_logger(logger):
    flush_log_buffer(logger)
    logger.close()


def get_logger() -> LogWriter:
    logger_module_name = os.getenv('LOGGER_MODULE', LOGGER_MODULE_MAIN_THREAD)
    log_path = logs_dir + '/' + log_file
    print('LOG PATH:', log_path)

    if logger_module_name == LOGGER_MODULE_CONCURRENT_FUTURES:
        print('PERFORMANCE LOGGER: CONCURRENT FUTURES')
        from performance.concurrent_futures_based_logger import ConcurrentFuturesBasedLogger
        return ConcurrentFuturesBasedLogger(log_path)

    if logger_module_name == LOGGER_MODULE_THREADING:
        print('PERFORMANCE LOGGER: THREADING')
        from performance.threading_based_logger import ThreadingBasedLogger
        return ThreadingBasedLogger(log_path)
    
    if logger_module_name == LOGGER_MODULE_MULTIPROCESSING:
        print('PERFORMANCE LOGGER: MULTIPROCESSING')
        from performance.multiprocessing_based_logger import MultiprocessingBasedLogger
        return MultiprocessingBasedLogger(log_path)
    
    print('PERFORMANCE LOGGER: MAIN THREAD')
    from performance.main_thread_logger import MainThreadBasedLogger
    return MainThreadBasedLogger(log_file)


def flush_log_buffer(logger):
    global log_buffer
    if len(log_buffer) == 0:
        return
    logger.write_to_log(log_buffer)  # Write buffer to log file using the logger
    log_buffer = []  # Clear buffer



def performance_class_decorator(cls):
    if CAPTURE_PERF_LOGS:
        # Decorate all methods in the class with the performance function decorator
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            setattr(cls, name, performance_func_decorator(method))
    return cls


def performance_func_decorator(func):
    if not CAPTURE_PERF_LOGS:
        return func

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        if not CAPTURE_PERF_LOGS:
            print("THIS SHOULD NOT SHOW UP")
        #     print("Performance logging is disabled. Skipping...")
        #     return func

        

        start_time = time.perf_counter()
        # result = method(*args, **kwargs)
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        func_name = func.__name__
        module_name = func.__module__

        # Create a key for the performance data dictionary
        key = f"{module_name}.{func_name}"
        execution_time = end_time - start_time
        data = {
            # 'class_name': cls.__name__,
            'key': key,
            'module_name': module_name,
            'method_name': func_name,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        }


        log_buffer.append(data)
        # Write buffer to file periodically (e.g., every 100 entries)
        if len(log_buffer) >= LOG_BUFFER_SIZE:
            flush_log_buffer(LOGGER)
        return result

    return wrapper

if CAPTURE_PERF_LOGS:
    LOGGER: LogWriter = get_logger()
    atexit.register(close_logger, LOGGER)