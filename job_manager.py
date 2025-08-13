import queue
import threading

class JobManager:
    def __init__(self, completion_callback=None):
        self.job_queue = queue.Queue()
        self.completion_callback = completion_callback  # Called with (input_path, success, error_msg)
        self.thread = None

    def add_job(self, input_path, output_path):
        self.job_queue.put((input_path, output_path))

    def process_queue(self, compressor_func):
        while not self.job_queue.empty():
            input_path, output_path = self.job_queue.get()
            success, error_msg = compressor_func(input_path, output_path)
            if self.completion_callback:
                # Call the callback in the main thread using tkinter's after method if possible
                try:
                    import tkinter
                    root = tkinter._default_root
                    if root:
                        root.after(0, self.completion_callback, input_path, success, error_msg)
                    else:
                        self.completion_callback(input_path, success, error_msg)
                except Exception:
                    self.completion_callback(input_path, success, error_msg)
            self.job_queue.task_done()

    def start(self, compressor_func):
        self.thread = threading.Thread(target=self.process_queue, args=(compressor_func,))
        self.thread.daemon = True
        self.thread.start()
