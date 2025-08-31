from pytubefix import Playlist, YouTube
from tqdm import tqdm
import os
import subprocess
import json

# --- CONFIGURATION ---
# IMPORTANT: Replace this with the ACTUAL path to your ffmpeg.exe file.
FFMPEG_EXECUTABLE_PATH = r'C:\Development\Python\Tools\youtube_downloader\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe'
AUDIO_STATE_FILE = 'youtube_audio_state.json' # Name of the file to store audio progress
AUDIO_DOWNLOAD_DIR_SUFFIX = '_audio' # Suffix for the directory storing audio files
# ---------------------

def load_state(state_file_path):
    """Loads the download state from a JSON file."""
    if os.path.exists(state_file_path):
        try:
            with open(state_file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from {state_file_path}. Starting fresh.")
            return {}
    return {}

def save_state(state_file_path, state):
    """Saves the current download state to a JSON file."""
    try:
        with open(state_file_path, 'w') as f:
            json.dump(state, f, indent=4)
    except IOError as e:
        print(f"Error saving state to {state_file_path}: {e}")

def get_best_audio_stream(yt):
    """Helper function to get the best audio stream."""
    # Prioritize streams that pytube can more easily convert to mp3 or are already mp4 audio
    # abr = average bitrate
    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
    if not audio_stream:
        # Fallback to any audio stream if mp4 audio is not available
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    return audio_stream

def download_youtube_audio_as_mp3(yt, video_url, video_title_sanitized, i, total_videos, download_path, audio_stream, current_state):
    """Downloads and converts audio to MP3, updating the state."""
    # Define filenames for the audio download and the final MP3 output
    audio_download_filename = os.path.join(download_path, f"{i:03d}_{video_title_sanitized}_audio.{audio_stream.subtype}")
    output_mp3_filename = os.path.join(download_path, f"{i:03d}_{video_title_sanitized}.mp3")

    # --- Check if already completed ---
    if video_url in current_state and current_state[video_url] == 'completed':
        # print(f"  - Skipping audio (already completed): {yt.title}") # Uncomment for verbose skipping
        return True # Indicate success

    # --- Update state to 'in_progress' ---
    current_state[video_url] = 'in_progress'
    save_state(AUDIO_STATE_FILE, current_state) # Save state for audio

    try:
        # --- Download the audio stream ---
        if not os.path.exists(audio_download_filename):
            print(f"  - Downloading audio stream: {audio_stream.abr} ({audio_stream.mime_type})")
            audio_stream.download(output_path=download_path, filename=os.path.basename(audio_download_filename))
        else:
            print(f"  - Audio file already exists: {os.path.basename(audio_download_filename)}")

        # --- Convert audio to MP3 using ffmpeg ---
        if not os.path.exists(output_mp3_filename):
            print(f"  - Converting to MP3...")
            
            # ffmpeg command:
            # -i input_file: specifies the input audio stream
            # -vn: Disables video recording (we only want audio)
            # -acodec libmp3lame: Specifies the MP3 audio codec (lame is high quality)
            # -ab 192k: Sets the audio bitrate to 192kbps (good balance of quality and size). You can adjust this (e.g., '128k', '256k', '320k').
            # -map_metadata 0: Copies metadata from the first input.
            # -id3v2_version 3: For better compatibility with ID3 tags.
            # -y: Overwrites output file if it exists without asking.
            
            convert_cmd_args = [
                FFMPEG_EXECUTABLE_PATH,
                '-i', audio_download_filename,
                '-vn',                    # No video
                '-acodec', 'libmp3lame',  # Use MP3 codec (lame)
                '-ab', '192k',            # Audio bitrate: adjust as needed (e.g., 128k, 256k, 320k)
                '-map_metadata', '0',     # Copy metadata
                '-id3v2_version', '3',    # ID3 tag version
                '-y',
                output_mp3_filename
            ]

            process = subprocess.run(convert_cmd_args, check=True, capture_output=True, text=True)
            print(f"  - Successfully converted to MP3: {os.path.basename(output_mp3_filename)}")
            
            if process.stderr:
                print("  - ffmpeg output (stderr):\n    " + process.stderr.replace('\n', '\n    '))

            # Clean up the original downloaded audio file after successful conversion
            try:
                os.remove(audio_download_filename)
            except OSError as e:
                print(f"  - Error cleaning up temporary audio file: {e}")
        else:
            print(f"  - MP3 file already exists: {os.path.basename(output_mp3_filename)}. Skipping conversion.")
            # Clean up temp audio if MP3 exists but temp doesn't
            if os.path.exists(audio_download_filename): os.remove(audio_download_filename)
        
        # --- Mark as completed ---
        current_state[video_url] = 'completed'
        save_state(AUDIO_STATE_FILE, current_state)
        return True # Indicate success

    except FileNotFoundError:
        print(f"\n  - Error: ffmpeg executable not found at '{FFMPEG_EXECUTABLE_PATH}'.")
        print("    Please ensure ffmpeg is correctly downloaded and the path in the script is accurate.")
        print("    You can download ffmpeg from: https://ffmpeg.org/download.html")
        current_state[video_url] = 'failed_ffmpeg_path' # Mark as failed
        save_state(AUDIO_STATE_FILE, current_state)
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n  - Error during ffmpeg conversion for '{yt.title}':")
        print(f"    Command: {' '.join(e.cmd)}")
        print(f"    Return Code: {e.returncode}")
        print(f"    Stderr:\n    {e.stderr.strip()}")
        current_state[video_url] = 'failed_conversion' # Mark as failed
        save_state(AUDIO_STATE_FILE, current_state)
        return False
    except Exception as e:
        print(f"\n  - An unexpected error occurred during download/conversion for '{yt.title}': {e}")
        current_state[video_url] = 'failed_generic' # Mark as failed
        save_state(AUDIO_STATE_FILE, current_state)
        return False

def download_youtube_playlist_to_mp3_resumable(playlist_url, base_download_path='.'):
    """
    Downloads audio from a YouTube playlist as MP3, tracking progress in a JSON file
    to allow resuming.
    """
    try:
        # Create a specific directory for audio downloads
        audio_download_path = os.path.normpath(base_download_path.strip()) + AUDIO_DOWNLOAD_DIR_SUFFIX
        
        if not os.path.exists(audio_download_path):
            os.makedirs(audio_download_path)
            print(f"Created audio download directory: {audio_download_path}")
            print("-" * 30)

        playlist = Playlist(playlist_url)
        print(f"Playlist Title: {playlist.title}")
        print(f"Number of videos: {len(playlist.video_urls)}")
        print("-" * 30)

        # --- Load existing state ---
        state = load_state(AUDIO_STATE_FILE)
        
        # --- Get all video URLs from the playlist once ---
        playlist_video_urls = list(playlist.video_urls)
        total_videos = len(playlist_video_urls)

        print("Starting audio download and conversion process...\n")
        
        successful_downloads = 0
        failed_downloads = 0

        for i, video_url in enumerate(playlist_video_urls):
            video_index = i + 1
            
            # Check if this video has already been completed
            if video_url in state and state[video_url] == 'completed':
                continue

            try:
                yt = YouTube(video_url)
                video_title_sanitized = yt.title
                for char in '\\/:*?"<>|':
                    video_title_sanitized = video_title_sanitized.replace(char, '_')
                video_title_sanitized = video_title_sanitized[:100]

                audio_stream = get_best_audio_stream(yt)

                if audio_stream:
                    # Pass current_state to the download function
                    if download_youtube_audio_as_mp3(yt, video_url, video_title_sanitized, video_index, total_videos, audio_download_path, audio_stream, state):
                        successful_downloads += 1
                    else:
                        failed_downloads += 1 # Error logged within download_youtube_audio_as_mp3

                else:
                    print(f"\n[{video_index}/{total_videos}] Skipping audio: No suitable audio streams found for '{yt.title}'")
                    state[video_url] = 'failed_no_streams'
                    save_state(AUDIO_STATE_FILE, state)
                    failed_downloads += 1

            except Exception as e:
                print(f"\nError processing video URL {video_url} ({yt.title if 'yt' in locals() else 'Unknown'}): {e}")
                state[video_url] = 'failed_generic_processing'
                save_state(AUDIO_STATE_FILE, state)
                failed_downloads += 1
        
        # --- Final save of state after loop ---
        save_state(AUDIO_STATE_FILE, state)

        print("-" * 30)
        print(f"Audio download and conversion process finished.")
        print(f"Successfully processed: {successful_downloads} songs")
        print(f"Failed or skipped: {failed_downloads} songs")
        print(f"Check '{AUDIO_STATE_FILE}' for details on any failures.")


    except Exception as e:
        print(f"Critical Error: Could not process playlist URL '{playlist_url}'.")
        print(f"Error details: {e}")

if __name__ == "__main__":
    print("--- YouTube Playlist to MP3 Downloader (Resumable) ---")
    playlist_link = input("Enter the YouTube Playlist URL: ")
    # Ask for a base directory, and we'll append '_audio' to it
    base_save_directory = input("Enter the base directory to save audio files (leave blank for current directory): ")

    if not base_save_directory:
        base_save_directory = '.'

    if FFMPEG_EXECUTABLE_PATH == r'C:\Path\To\Your\ffmpeg\bin\ffmpeg.exe':
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! IMPORTANT: Please update the FFMPEG_EXECUTABLE_PATH in the script !!!")
        print("!!! with the correct path to your ffmpeg.exe file.                 !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    else:
        download_youtube_playlist_to_mp3_resumable(playlist_link, base_save_directory)