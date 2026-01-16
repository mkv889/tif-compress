import logging
import concurrent.futures
from typing import Callable, Optional, List, Tuple

logger = logging.getLogger(__name__)

class JobManager:
    def __init__(self, completion_callback: Optional[Callable[[str, bool, Optional[str]], None]] = None):
        self.completion_callback = completion_callback  # Called with (input_path, success, error_msg)
        self.executor: Optional[concurrent.futures.ProcessPoolExecutor] = None
        self.futures: List[concurrent.futures.Future] = []

    def start(self, compressor_func: Callable[[str, str], Tuple[bool, Optional[str]]], jobs: List[Tuple[str, str]]):
        """
        Starts the compression jobs using a ProcessPoolExecutor.
        """
        if self.executor:
            self.cancel()

        logger.info(f"Starting {len(jobs)} compression jobs.")
        self.executor = concurrent.futures.ProcessPoolExecutor()
        self.futures = []

        for input_path, output_path in jobs:
            future = self.executor.submit(compressor_func, input_path, output_path)
            future.add_done_callback(lambda f, ip=input_path: self._handle_completion(ip, f))
            self.futures.append(future)

    def _handle_completion(self, input_path: str, future: concurrent.futures.Future):
        try:
            success, error_msg = future.result()
        except Exception as e:
            logger.exception(f"Unexpected error in job for {input_path}")
            success, error_msg = False, str(e)

        if self.completion_callback:
            self.completion_callback(input_path, success, error_msg)

    def cancel(self):
        """
        Cancels all pending and running jobs.
        """
        if self.executor:
            logger.info("Cancelling all jobs.")
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None
            self.futures = []
