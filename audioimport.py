import sys
import os
import yt_dlp
import subprocess
from datetime import timedelta

# Default download folder - change this to your preferred location
DEFAULT_DOWNLOAD_FOLDER = "C:\\Users\\hariragu\\Downloads\\"

# downloads yt_url to the configured download directory with optional trimming
def download_audio(yt_url, output_path=None, start_time=None, end_time=None):
    try:
        # Use default download folder if none specified
        if not output_path:
            output_path = DEFAULT_DOWNLOAD_FOLDER
            
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        # Generate a unique temporary filename for the initial download
        temp_filename = 'temp_download'
        temp_output_template = os.path.join(output_path, f'{temp_filename}.%(ext)s')
        
        # Final filename will include info about trim if applied
        trim_info = ""
        if start_time is not None or end_time is not None:
            start_str = f"{start_time}s" if start_time is not None else "start"
            end_str = f"{end_time}s" if end_time is not None else "end"
            trim_info = f"_trim_{start_str}_to_{end_str}"
        
        final_output_template = os.path.join(output_path, f'%(title)s{trim_info}.%(ext)s')
            
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_output_template,
            'quiet': False,
            'verbose': False,
            'no_warnings': False,
        }
        
        # If no trimming is needed, use normal postprocessing
        if start_time is None and end_time is None:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            ydl_opts['outtmpl'] = final_output_template
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from: {yt_url}")
            info = ydl.extract_info(yt_url, download=True)
            
            # If we need to trim, use ffmpeg directly
            if start_time is not None or end_time is not None:
                print(f"Trimming audio from {start_time if start_time is not None else 0}s to {end_time if end_time is not None else 'end'}s")
                
                # Get the downloaded file path
                downloaded_file = os.path.join(output_path, f"{temp_filename}.{info['ext']}")
                title = info['title']
                safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                
                # Create the final output file path
                final_file = os.path.join(output_path, f"{safe_title}{trim_info}.mp3")
                
                # Prepare ffmpeg command for trimming
                ffmpeg_cmd = ['ffmpeg', '-i', downloaded_file]
                
                if start_time is not None:
                    ffmpeg_cmd.extend(['-ss', str(start_time)])
                
                if end_time is not None:
                    ffmpeg_cmd.extend(['-to', str(end_time)])
                
                ffmpeg_cmd.extend([
                    '-acodec', 'libmp3lame',
                    '-q:a', '2',
                    '-y',  # Overwrite output file if it exists
                    final_file
                ])
                
                # Execute ffmpeg command
                subprocess.run(ffmpeg_cmd, check=True)
                
                # Remove the temporary file
                os.remove(downloaded_file)
                
                print(f"Trimmed audio saved to: {final_file}")
            else:
                print("Download completed successfully!")
            
    except Exception as e:
        print(f"Error downloading or trimming audio: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Make sure the YouTube URL is valid")
        print("3. Make sure yt-dlp is installed: pip install yt-dlp")
        print("4. Make sure FFmpeg is installed and in your PATH")
        print("   - Windows: Download from https://www.gyan.dev/ffmpeg/builds/")
        print("   - macOS: brew install ffmpeg")
        print("   - Linux: apt/dnf/pacman install ffmpeg")
        
def format_time_input(time_str):
    """Convert time string in various formats to seconds."""
    if not time_str:
        return None
        
    # If it's already a number, return it as float
    try:
        return float(time_str)
    except ValueError:
        pass
        
    # Try to parse time in format MM:SS or HH:MM:SS
    try:
        parts = time_str.split(':')
        if len(parts) == 2:  # MM:SS
            return int(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:  # HH:MM:SS
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except (ValueError, IndexError):
        print(f"Invalid time format: {time_str}. Please use seconds (e.g., 120) or MM:SS (e.g., 2:00) or HH:MM:SS (e.g., 1:02:30)")
        return None
        
def main():
    yt_url = input("Enter YouTube URL (or press Enter for default): ")
    if not yt_url:
        yt_url = "https://www.youtube.com/watch?v=IFZS-sA_0cs"
        print(f"Using default URL: {yt_url}")
    
    # Get start and end times for trimming
    start_time_input = input("Enter start time (e.g., 120, 2:00, or 1:02:30) or press Enter to start from beginning: ")
    end_time_input = input("Enter end time (e.g., 240, 4:00, or 1:04:30) or press Enter to use full length: ")
    
    # Convert time inputs to seconds
    start_time = format_time_input(start_time_input)
    end_time = format_time_input(end_time_input)
    
    # Ask for custom output directory or use default
    use_default = input(f"Use default download folder ({DEFAULT_DOWNLOAD_FOLDER})? (Y/n): ").lower() != 'n'
    output_dir = DEFAULT_DOWNLOAD_FOLDER if use_default else input("Enter output directory: ")
    
    download_audio(yt_url, output_dir, start_time, end_time)

if __name__ == "__main__":
    main()
