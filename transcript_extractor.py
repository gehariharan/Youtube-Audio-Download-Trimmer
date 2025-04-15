import os
import sys
import tempfile
import whisper
import yt_dlp
import time
from pathlib import Path

# Default download folder - change this to your preferred location
DEFAULT_DOWNLOAD_FOLDER = "C:\\Users\\hariragu\\Downloads\\"
DEFAULT_MODEL_SIZE = "small"  # Options:  small, medium, large, turbo

def download_audio_for_transcription(yt_url, output_path=None):
    """Download audio from YouTube for transcription purposes"""
    try:
        # Use default download folder if none specified
        if not output_path:
            output_path = DEFAULT_DOWNLOAD_FOLDER
            
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Create a temporary directory for the downloaded audio
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_filename = os.path.join(temp_dir, 'temp_audio')
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': temp_filename,
                'quiet': False,
                'verbose': False,
                'no_warnings': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading audio from: {yt_url}")
                info = ydl.extract_info(yt_url, download=True)
                title = info.get('title', 'unknown_video')
                safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                
                # Path to the downloaded audio file (now in WAV format for Whisper)
                audio_file = f"{temp_filename}.wav"
                
                return audio_file, safe_title
                
    except Exception as e:
        print(f"Error downloading audio for transcription: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Make sure the YouTube URL is valid")
        print("3. Make sure yt-dlp is installed: pip install yt-dlp")
        print("4. Make sure FFmpeg is installed and in your PATH")
        return None, None

def transcribe_audio(audio_file, output_path, title, model_size=DEFAULT_MODEL_SIZE):
    """Transcribe the audio file using Whisper model"""
    try:
        print(f"Loading Whisper {model_size} model...")
        model = whisper.load_model(model_size)
        
        print("Starting transcription (this may take a while)...")
        start_time = time.time()
        
        # Perform transcription with Tamil and Sanskrit language detection
        # Whisper will auto-detect Tamil and Sanskrit when needed
        result = model.transcribe(
            audio_file,
            language="ta",  # Setting primary language as Tamil
            task="transcribe",
            verbose=True
        )
        
        end_time = time.time()
        print(f"Transcription completed in {end_time - start_time:.2f} seconds")
        
        # Create output file for transcript
        transcript_path = os.path.join(output_path, f"{title}_transcript.txt")
        srt_path = os.path.join(output_path, f"{title}_transcript.srt")
        
        # Save plain text transcript
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(result["text"])
        
        # Save SRT format with timestamps
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(result["segments"], 1):
                # Write SRT format: index, timestamps, text
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment['text'].strip()}\n\n")
        
        print(f"Transcript saved to: {transcript_path}")
        print(f"SRT file saved to: {srt_path}")
        
        return transcript_path, srt_path
        
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have the OpenAI Whisper package installed: pip install openai-whisper")
        print("2. Make sure you have enough disk space and RAM for the model")
        print("3. If using GPU, make sure CUDA is properly installed")
        return None, None

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def main():
    # Get YouTube URL
    yt_url = input("Enter YouTube URL (or press Enter for default): ")
    if not yt_url:
        yt_url = "https://www.youtube.com/watch?v=IFZS-sA_0cs"
        print(f"Using default URL: {yt_url}")
    
    # Ask for model size or use default
    print(f"\nWhisper model sizes:")
    print("- tiny: Fastest, least accurate (good for testing)")
    print("- base: Fast, low accuracy")
    print("- small: Balanced speed and accuracy (default)")
    print("- medium: Better accuracy, slower")
    print("- large: Best accuracy, slowest")
    model_size = input(f"Choose model size (default: {DEFAULT_MODEL_SIZE}): ").lower() or DEFAULT_MODEL_SIZE
    
    if model_size not in ["tiny", "base", "small", "medium", "large"]:
        print(f"Invalid model size. Using default: {DEFAULT_MODEL_SIZE}")
        model_size = DEFAULT_MODEL_SIZE
        
    # Ask for custom output directory or use default
    use_default = input(f"Use default download folder ({DEFAULT_DOWNLOAD_FOLDER})? (Y/n): ").lower() != 'n'
    output_dir = DEFAULT_DOWNLOAD_FOLDER if use_default else input("Enter output directory: ")
    
    # Download audio from YouTube
    print("\nStep 1: Downloading audio...")
    audio_file, title = download_audio_for_transcription(yt_url, output_dir)
    
    if audio_file:
        # Transcribe the audio
        print("\nStep 2: Transcribing audio...")
        transcript_file, srt_file = transcribe_audio(audio_file, output_dir, title, model_size)
        
        if transcript_file:
            print("\nTranscription successful!")
            print("You can now use the transcript in both TXT and SRT formats.")

if __name__ == "__main__":
    main()