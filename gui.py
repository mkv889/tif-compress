import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import logging
import shutil
import ctypes
from typing import List, Optional
from job_manager import JobManager
from compressor import compress_tif

logger = logging.getLogger(__name__)

# --- Theme Constants ---
BG_MAIN = "#0A214D"
BG_SURFACE = "#073072"
PRIMARY = "#0060E0"
SECONDARY = "#068989"
TEXT_PRIMARY = "#FFFFFF"
TEXT_SECONDARY = "#B3FFE3"
SUCCESS = "#3FE1B0"
ERROR = "#FF505F"
WARNING = "#FF7139"

FONT_TITLE = ("Metropolis", 18, "bold")
FONT_SECTION = ("Metropolis", 12, "bold")
FONT_BODY = ("Inter", 10)
FONT_CAPTION = ("Inter", 9)

def load_fonts():
    """Load custom fonts using Windows GDI32 API."""
    try:
        gdi32 = ctypes.WinDLL('gdi32')
        # Metropolis
        metropolis_path = os.path.abspath("fonts/Metropolis-r11/Fonts/TrueType/Metropolis-Regular.ttf")
        metropolis_bold_path = os.path.abspath("fonts/Metropolis-r11/Fonts/TrueType/Metropolis-Bold.ttf")
        gdi32.AddFontResourceExW(metropolis_path, 0x10, 0)
        gdi32.AddFontResourceExW(metropolis_bold_path, 0x10, 0)
        
        # Inter
        inter_path = os.path.abspath("fonts/Inter-4.1/extras/ttf/Inter-Regular.ttf")
        inter_bold_path = os.path.abspath("fonts/Inter-4.1/extras/ttf/Inter-Bold.ttf")
        gdi32.AddFontResourceExW(inter_path, 0x10, 0)
        gdi32.AddFontResourceExW(inter_bold_path, 0x10, 0)
    except Exception as e:
        logger.warning(f"Could not load custom fonts: {e}")

class App(tk.Tk):
    def __init__(self) -> None:
        load_fonts()
        super().__init__()
        self.title("TIF Compressor")
        self.geometry("800x600")
        self.configure(bg=BG_MAIN)
        
        self.output_path: str = ""
        self.job_manager: JobManager = JobManager(self.update_ui_on_completion_safe)
        self.completed_jobs: int = 0
        self.total_jobs: int = 0
        
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main Frame
        style.configure("TFrame", background=BG_MAIN)
        style.configure("Surface.TFrame", background=BG_SURFACE)
        
        # Labels
        style.configure("TLabel", background=BG_MAIN, foreground=TEXT_PRIMARY, font=FONT_BODY)
        style.configure("Header.TLabel", font=FONT_TITLE, padding=10)
        style.configure("Section.TLabel", background=BG_SURFACE, font=FONT_SECTION)
        style.configure("Path.TLabel", background=BG_SURFACE, foreground=TEXT_SECONDARY, font=FONT_CAPTION)
        
        # Buttons
        style.configure("TButton", font=FONT_BODY, padding=5)
        style.configure("Primary.TButton", background=PRIMARY, foreground=TEXT_PRIMARY)
        style.map("Primary.TButton", background=[('active', '#0050C0')])
        
        style.configure("Secondary.TButton", background=SECONDARY, foreground=TEXT_PRIMARY)
        style.map("Secondary.TButton", background=[('active', '#057878')])

        # Progress Bar
        style.configure("Success.Horizontal.TProgressbar", 
                        troughcolor=BG_SURFACE, 
                        background=SUCCESS, 
                        thickness=8)

    def create_widgets(self) -> None:
        # Main container with 24px padding
        main_container = ttk.Frame(self, padding=24)
        main_container.pack(fill=tk.BOTH, expand=True)

        # --- Header Frame ---
        self.header = ttk.Frame(main_container)
        self.header.pack(fill=tk.X, pady=(0, 16))
        
        # Dot + Title
        title_container = ttk.Frame(self.header)
        title_container.pack(side=tk.LEFT)
        
        # Decorative Dot (Canvas for rounded shape)
        dot = tk.Canvas(title_container, width=12, height=12, bg=BG_MAIN, highlightthickness=0)
        dot.pack(side=tk.LEFT, padx=(0, 8))
        dot.create_oval(2, 2, 10, 10, fill=PRIMARY, outline="")
        
        ttk.Label(title_container, text="TIF Compressor", style="Header.TLabel").pack(side=tk.LEFT)

        # --- Selection Frame ---
        self.selection_frame = ttk.Frame(main_container, style="Surface.TFrame", padding=16)
        self.selection_frame.pack(fill=tk.X, pady=(0, 16))
        
        btn_container = ttk.Frame(self.selection_frame, style="Surface.TFrame")
        btn_container.pack(fill=tk.X)
        
        ttk.Button(btn_container, text="Add Files", style="Secondary.TButton", command=self.add_files).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_container, text="Add Folder", style="Secondary.TButton", command=self.add_folder).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_container, text="Select Output", style="Secondary.TButton", command=self.select_output_folder).pack(side=tk.LEFT)
        ttk.Button(btn_container, text="Clear", command=self.clear_list).pack(side=tk.RIGHT)

        self.output_path_label = ttk.Label(self.selection_frame, text="Output: Not Selected", style="Path.TLabel")
        self.output_path_label.pack(fill=tk.X, pady=(8, 0))

        # --- Queue Frame ---
        self.queue_frame = ttk.Frame(main_container, style="Surface.TFrame", padding=8)
        self.queue_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))
        
        ttk.Label(self.queue_frame, text="Job Queue", style="Section.TLabel").pack(anchor=tk.W, padx=8, pady=4)
        
        list_container = ttk.Frame(self.queue_frame, style="Surface.TFrame")
        list_container.pack(fill=tk.BOTH, expand=True)
        
        self.job_list_var = tk.Variable(value=[])
        self.job_listbox = tk.Listbox(
            list_container, 
            listvariable=self.job_list_var,
            bg=BG_SURFACE,
            fg=TEXT_PRIMARY,
            font=FONT_BODY,
            borderwidth=0,
            highlightthickness=0,
            selectbackground=PRIMARY
        )
        self.job_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.job_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.job_listbox.config(yscrollcommand=scrollbar.set)

        # --- Footer Frame ---
        self.footer = ttk.Frame(main_container)
        self.footer.pack(fill=tk.X)
        
        self.progress = ttk.Progressbar(self.footer, orient="horizontal", mode="determinate", style="Success.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(0, 16))
        
        action_container = ttk.Frame(self.footer)
        action_container.pack(fill=tk.X)
        
        self.status_label = ttk.Label(action_container, text="Ready", font=FONT_CAPTION)
        self.status_label.pack(side=tk.LEFT)
        
        self.start_button = ttk.Button(action_container, text="Start Compression", style="Primary.TButton", command=self.start_compression)
        self.start_button.pack(side=tk.RIGHT, padx=(8, 0))
        
        self.cancel_button = ttk.Button(action_container, text="Cancel", command=self.cancel_compression, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.RIGHT)

    def add_files(self) -> None:
        files = filedialog.askopenfilenames(
            title="Select TIF files",
            filetypes=(("TIF files", "*.tif *.tiff"), ("All files", "*.*"))
        )
        current_files = list(self.job_list_var.get())
        for file in files:
            if file not in current_files:
                current_files.append(file)
        self.job_list_var.set(current_files)

    def add_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select folder with TIF files")
        if folder:
            current_files = list(self.job_list_var.get())
            for item in os.listdir(folder):
                if item.lower().endswith((".tif", ".tiff")):
                    full_path = os.path.join(folder, item)
                    if full_path not in current_files:
                        current_files.append(full_path)
            self.job_list_var.set(current_files)

    def clear_list(self) -> None:
        self.job_list_var.set([])

    def select_output_folder(self) -> None:
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_path = folder
            self.output_path_label.config(text=f"Output: {self.output_path}")

    def validate_output_dir(self, path: str) -> bool:
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                logger.error(f"Could not create output directory: {e}")
                messagebox.showerror("Error", f"Could not create output directory:\n{e}")
                return False
        
        if not os.access(path, os.W_OK):
            logger.error(f"Output directory is not writable: {path}")
            messagebox.showerror("Error", "Output directory is not writable.")
            return False

        total, used, free = shutil.disk_usage(path)
        if free < 100 * 1024 * 1024: # 100MB minimum
            logger.warning(f"Low disk space on {path}: {free / (1024*1024):.2f} MB free")
            if not messagebox.askyesno("Warning", "Low disk space detected. Continue?"):
                return False
        
        return True

    def start_compression(self) -> None:
        if not self.output_path:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        if not self.validate_output_dir(self.output_path):
            return

        files_to_process = self.job_list_var.get()
        if not files_to_process:
            messagebox.showinfo("Info", "No files to compress.")
            return

        self.total_jobs = len(files_to_process)
        self.completed_jobs = 0
        self.progress['maximum'] = self.total_jobs
        self.progress['value'] = 0
        self.status_label.config(text=f"Processing 0/{self.total_jobs}...")

        jobs = []
        for file_path in files_to_process:
            file_name = os.path.basename(file_path)
            output_file_path = os.path.join(self.output_path, file_name)
            jobs.append((file_path, output_file_path))

        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.job_manager.start(compress_tif, jobs)

    def cancel_compression(self) -> None:
        self.job_manager.cancel()
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.status_label.config(text="Cancelled")
        logger.info("Compression cancelled by user.")
        messagebox.showinfo("Cancelled", "Compression process has been cancelled.")

    def update_ui_on_completion_safe(self, input_path: str, success: bool, error_msg: Optional[str]) -> None:
        self.after(0, self.update_ui_on_completion, input_path, success, error_msg)

    def update_ui_on_completion(self, input_path: str, success: bool, error_msg: Optional[str]) -> None:
        if success:
            current_files = list(self.job_list_var.get())
            if input_path in current_files:
                current_files.remove(input_path)
                self.job_list_var.set(current_files)
        else:
            logger.error(f"Failed to compress {input_path}: {error_msg}")

        self.completed_jobs += 1
        self.progress['value'] = self.completed_jobs
        self.status_label.config(text=f"Processing {self.completed_jobs}/{self.total_jobs}...")

        if self.completed_jobs >= self.total_jobs:
            self.start_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            self.status_label.config(text="Done")
            logger.info("All jobs completed.")
            messagebox.showinfo("Done", "Compression process finished.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = App()
    app.mainloop()
