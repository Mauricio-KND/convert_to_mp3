# Audio File Converter Web Application

A Flask web application that converts FLAC and WAV audio files to MP3 format while preserving metadata and cover art.

## Features

- Converts FLAC and WAV files to high-quality MP3 (320kbps)
- Preserves metadata (title, artist, album, etc.) from FLAC files
- Supports embedded cover art (JPG/PNG files with same base name)
- Batch processing of multiple files
- Clean, responsive web interface with drag-and-drop support
- Automatic cleanup of temporary files

## Requirements

- Python 3.8+
- FFmpeg (required by pydub)

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install FFmpeg:
   - On Ubuntu/Debian: `sudo apt install ffmpeg`
   - On macOS (using Homebrew): `brew install ffmpeg`
   - On Windows: Download from [FFmpeg website](https://ffmpeg.org/)

## Usage

1. Run the development server:
   ```bash
   python app.py
   ```
2. Open your browser to: http://localhost:5000
3. Drag and drop audio files (FLAC/WAV) and optionally cover art (JPG/PNG)
4. Click "Download Converted Files" when conversion is complete

For production deployment, use Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Configuration

You can configure the application by creating a `.env` file with these variables:
```
SECRET_KEY=your-secret-key-here
MAX_CONTENT_MB=100  # Max file size in MB
UPLOAD_FOLDER=temp_uploads
CONVERTED_FOLDER=temp_converted
```

## License

MIT
