# TIF Compressor

A high-performance, modern desktop application for batch compressing TIF/TIFF images using LZW compression. Built with Python, Tkinter, and Pillow, featuring a design system inspired by the Firefox brand.

## Features

- **Modern UI**: Clean, dark-themed interface based on the Firefox design specification.
- **High Performance**: Utilizes multiprocessing (`ProcessPoolExecutor`) to compress multiple files in parallel, significantly reducing processing time for large batches.
- **Batch Processing**: Easily add individual files or entire folders to the queue.
- **Real-time Progress**: Visual progress bar and status updates for the entire batch.
- **Robust Error Handling**: Validates output directories, checks for disk space, and logs errors for failed jobs.
- **Custom Typography**: Integrated Metropolis and Inter fonts for a professional look.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/tif-compressor.git
   cd tif-compressor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `fonts/` directory is present with the required `.ttf` files.

## Usage

Run the application using:
```bash
python main.py
```

1. **Add Files/Folder**: Use the buttons in the selection area to populate the job queue.
2. **Select Output**: Choose a destination folder for the compressed files.
3. **Start**: Click "Start Compression" to begin the parallel processing.
4. **Monitor**: Watch the progress bar and status label for real-time feedback.

## Technical Details

- **Compression**: Uses `Pillow`'s `tiff_lzw` compression algorithm.
- **Concurrency**: Implemented via `concurrent.futures.ProcessPoolExecutor` to bypass the GIL and utilize multiple CPU cores.
- **Logging**: Comprehensive logging to both `tif_compressor.log` and the console.
- **Design System**:
  - **Primary Color**: `#0060E0` (Firefox Blue)
  - **Background**: `#0A214D` (Deep Navy)
  - **Surface**: `#073072` (Navy)
  - **Success**: `#3FE1B0` (Emerald)

## Requirements

- Python 3.8+
- Pillow
- Windows OS (for custom font loading via GDI32)

## License

[MIT License](LICENSE)
