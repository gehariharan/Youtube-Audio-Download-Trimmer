# YouTube Audio Downloader

A simple Python script to download audio from YouTube videos and optionally trim them to specific timestamps.

## Features

- Download audio from any YouTube video
- Convert videos to high-quality MP3 format
- Trim audio to specific start and end times
- Support for multiple time input formats (seconds, MM:SS, HH:MM:SS)
- Configurable download location

## Requirements

- Python 3.6 or higher
- yt-dlp library
- FFmpeg (installed and available in your PATH)

## Installation

1. Make sure you have Python installed on your system
2. Install the required Python package:
   ```
   pip install yt-dlp
   ```
3. Install FFmpeg:
   - **Windows**: Download from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) and add to PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg` (Ubuntu/Debian) or equivalent for your distribution

## Usage

Before running the script - Update the DEFAULT_DOWNLOAD_FOLDER  Path
Run the script

## Disclaimer

This project is intended for educational and personal use only. Downloading copyrighted material from YouTube without permission is against YouTube's Terms of Service and may also be illegal in your country. Please ensure that you have the right to download and use the content before doing so.
