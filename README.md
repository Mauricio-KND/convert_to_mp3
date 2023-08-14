# FLAC to MP3 Converter

A basic Python script that converts FLAC audio files to MP3 format while preserving their metadata. The script uses the `pydub` library for audio conversion and the `mutagen` library for metadata handling.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Libraries Used](#libraries-used)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)

## Features

- Converts FLAC files to MP3 format while preserving metadata.
- Processes several FLAC files in the input folder.
- Converts to MP3 format at 320 kbps bitrate.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Mauricio-KND/flac-mp3_converter.git
   
   cd flac-mp3-converter

2. Set up a virtual environment named 'venv' (optional but recommended):

   ```bash
   python3 -m venv venv

3. Activate the virtual environment:

   ```bash
   # Windows
   venv\Scripts\activate

   # macOS or Linux
   source venv/bin/activate


4. Install the required libraries:

   ```bash
   pip install pydub mutagen

## Usage

1. Place your FLAC audio files in the "file_to_convert" folder

2. Run the script:

   ```bash
   python flac_mp3_converter.py


## Libraries Used

### pydub

A Python library for audio processing. It provides a simple and convenient interface for working with audio files, including audio format conversion, audio slicing, volume adjustment, and more. In this project, we use pydub to convert the FLAC audio files to MP3 format.

### mutagen

A Python library for handling audio metadata. It allows to read and write metadata tags in various audio file formats, including FLAC and MP3. In this project, we use mutagen to extract metadata from the original FLAC files and apply them to the converted MP3 files.

## Notes

- The script finds all FLAC files present in the "file_to_convert" folder and converts them to MP3 format.
- The converted MP3 files will be saved in the "converted_file" folder with the same names as the original FLAC files (except for the extension).
- Make sure to activate the virtual environment before running the script. By using a virtual environment, you ensure that the dependencies you install and the program you run are isolated from your system-wide Python environment. This helps prevent conflicts between different projects and makes it easier to manage your project's dependencies.

## Contributing

Contributions are welcome! If you have suggestions, improvements, or bug fixes, feel free to open an issue or a pull request in the GitHub repository.

## License

This project is licensed under the MIT License.