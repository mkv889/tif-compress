import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from job_manager import JobManager
from compressor import compress_tif

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TIF Compressor")
        self.geometry("600x400")
        self.output_path = ""
        self.job_manager = JobManager(self.update_ui_on_completion)
        self.create_widgets()

    def create_widgets(self):
        # Frames
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        middle_frame = ttk.Frame(self)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)

        # Top Frame Widgets
        self.add_files_button = ttk.Button(top_frame, text="Add Files", command=self.add_files)
        self.add_files_button.pack(side=tk.LEFT, padx=5)

        self.add_folder_button = ttk.Button(top_frame, text="Add Folder", command=self.add_folder)
        self.add_folder_button.pack(side=tk.LEFT, padx=5)

        self.output_folder_button = ttk.Button(top_frame, text="Output Folder", command=self.select_output_folder)
        self.output_folder_button.pack(side=tk.LEFT, padx=5)

        # Middle Frame Widgets
        self.job_listbox = tk.Listbox(middle_frame)
        self.job_listbox.pack(fill=tk.BOTH, expand=True)

        # Progress Bar
        self.progress = ttk.Progressbar(middle_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, pady=5)

        # Bottom Frame Widgets
        self.start_button = ttk.Button(bottom_frame, text="Start Compression", command=self.start_compression)
        self.start_button.pack(side=tk.RIGHT, padx=5)

        self.output_path_label = ttk.Label(bottom_frame, text="Output: Not Selected")
        self.output_path_label.pack(side=tk.LEFT, padx=5)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select TIF files",
            filetypes=(("TIF files", "*.tif *.tiff"), ("All files", "*.*"))
        )
        for file in files:
            self.job_listbox.insert(tk.END, file)

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select folder with TIF files")
        if folder:
            for item in os.listdir(folder):
                if item.lower().endswith((".tif", ".tiff")):
                    full_path = os.path.join(folder, item)
                    self.job_listbox.insert(tk.END, full_path)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_path = folder
            self.output_path_label.config(text=f"Output: {self.output_path}")

    def start_compression(self):
        if not self.output_path:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        files_to_process = self.job_listbox.get(0, tk.END)
        if not files_to_process:
            messagebox.showinfo("Info", "No files to compress.")
            return

        self.progress['maximum'] = len(files_to_process)
        self.progress['value'] = 0
        self.completed_jobs = 0
        self.total_jobs = len(files_to_process)

        # Clear any previous jobs in JobManager
        self.job_manager.job_queue.queue.clear()

        for file_path in files_to_process:
            file_name = os.path.basename(file_path)
            output_file_path = os.path.join(self.output_path, file_name)
            self.job_manager.add_job(file_path, output_file_path)

        self.start_button.config(state=tk.DISABLED)
        self.job_manager.start(compress_tif)

    def update_ui_on_completion(self, input_path, success, error_msg):
        # This will be called from the main thread (via after)
        if success:
            # Find and remove the item from listbox
            for i, item in enumerate(self.job_listbox.get(0, tk.END)):
                if item == input_path:
                    self.job_listbox.delete(i)
                    break
        else:
            messagebox.showerror("Compression Error", f"Failed to compress {input_path}:\n{error_msg}")

        # Update progress bar
        if not hasattr(self, 'completed_jobs'):
            self.completed_jobs = 0
        self.completed_jobs += 1
        self.progress['value'] = self.completed_jobs

        # Re-enable start button when done
        if self.completed_jobs >= getattr(self, 'total_jobs', 0):
            self.start_button.config(state=tk.NORMAL)
