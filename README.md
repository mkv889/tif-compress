# TIF Compressor

TIF Compressor is a Python application for compressing TIFF image files with a user-friendly GUI. It supports batch processing, job management, and customizable compression settings.

## Features
- Compress single or multiple TIFF files
- Batch processing for folders
- Customizable compression options
- Simple graphical user interface (GUI)
- Job management for tracking compression tasks
- Cross-platform support (Windows, macOS, Linux)

## Requirements
- Python 3.12 or higher
- Required Python packages (see `requirements.txt`)

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/mkv889/tif-compressor.git
   cd tif-compressor
   ```
2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   # Activate the environment:
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### GUI Mode
Run the main application to launch the GUI:
```sh
python main.py
```

### Command-Line Mode
You can also use the compressor via command line (if supported):
```sh
python compressor.py --input <input_path> --output <output_path> [options]
```

#### Example:
```sh
python compressor.py --input images/ --output compressed/ --quality 80
```

## Project Structure
- `main.py` — Entry point for the GUI application
- `gui.py` — GUI logic and components
- `compressor.py` — Core compression logic
- `job_manager.py` — Job management and batch processing
- `requirements.txt` — Python dependencies

## Contributing
Contributions are welcome! Please open issues or submit pull requests for bug fixes, new features, or improvements.

## License
This project is licensed under the MIT License.

## Author
- [mkv889](https://github.com/mkv889)
