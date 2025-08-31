from pytubefix import Playlist, YouTube
from tqdm import tqdm
import os
import subprocess # For running ffmpeg commands
import json       # For handling JSON configuration

# --- CONFIGURATION ---
# IMPORTANT: Replace this with the ACTUAL path to your ffmpeg.exe file.
FFMPEG_EXECUTABLE_PATH = r'C:\Development\Python\Tools\youtube_downloader\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe'
STATE_FILE = 'playlist_state.json' # Name of the file to store progress
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

def get_stream_details(yt):
    """Helper function to get the best video and audio streams."""
    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not video_stream:
        video_stream = yt.streams.filter(adaptive=True, file_extension='webm').order_by('resolution').desc().first()

    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
    if not audio_stream:
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    
    return video_stream, audio_stream

def download_and_merge(yt, video_url, video_title_sanitized, i, total_videos, download_path, video_stream, audio_stream, current_state):
    """Downloads and merges a single video, updating the state."""
    video_filename_part = os.path.join(download_path, f"{i:03d}_{video_title_sanitized}_video.{video_stream.subtype}")
    audio_filename_part = os.path.join(download_path, f"{i:03d}_{video_title_sanitized}_audio.{audio_stream.subtype}")
    output_filename = os.path.join(download_path, f"{i:03d}_{video_title_sanitized}.mp4")

    # --- Check if already completed ---
    if video_url in current_state and current_state[video_url] == 'completed':
        # print(f"  - Skipping video (already completed): {yt.title}") # Uncomment for verbose skipping
        return True # Indicate success

    # --- Update state to 'in_progress' ---
    current_state[video_url] = 'in_progress'
    save_state(STATE_FILE, current_state)

    try:
        # --- Download video stream ---
        if not os.path.exists(video_filename_part):
            print(f"  - Video Stream: {video_stream.resolution} ({video_stream.mime_type})")
            video_stream.download(output_path=download_path, filename=os.path.basename(video_filename_part))
        else:
            print(f"  - Video file already exists: {os.path.basename(video_filename_part)}")

        # --- Download audio stream ---
        if not os.path.exists(audio_filename_part):
            print(f"  - Audio Stream: {audio_stream.abr} ({audio_stream.mime_type})")
            audio_stream.download(output_path=download_path, filename=os.path.basename(audio_filename_part))
        else:
            print(f"  - Audio file already exists: {os.path.basename(audio_filename_part)}")

        # --- Merge video and audio using ffmpeg ---
        if not os.path.exists(output_filename):
            print(f"  - Merging video and audio...")
            
            merge_cmd_args = [
                FFMPEG_EXECUTABLE_PATH,
                '-i', video_filename_part,
                '-i', audio_filename_part,
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-y'
            ]

            if video_stream.subtype == 'webm':
                merge_cmd_args.insert(1, '-c:v')
                merge_cmd_args.insert(2, 'libx264')
                merge_cmd_args.insert(3, '-crf')
                merge_cmd_args.insert(4, '23')

            merge_cmd_args.append(output_filename)

            process = subprocess.run(merge_cmd_args, check=True, capture_output=True, text=True)
            print(f"  - Successfully merged: {os.path.basename(output_filename)}")
            
            if process.stderr:
                print("  - ffmpeg output (stderr):\n    " + process.stderr.replace('\n', '\n    '))

            # Clean up the individual video and audio files after successful merge
            try:
                os.remove(video_filename_part)
                os.remove(audio_filename_part)
            except OSError as e:
                print(f"  - Error cleaning up temporary files: {e}")
        else:
            print(f"  - Merged file already exists: {os.path.basename(output_filename)}. Skipping merge.")
            # Clean up temps if merged file exists but temp parts don't
            if os.path.exists(video_filename_part): os.remove(video_filename_part)
            if os.path.exists(audio_filename_part): os.remove(audio_filename_part)
        
        # --- Mark as completed ---
        current_state[video_url] = 'completed'
        save_state(STATE_FILE, current_state)
        return True # Indicate success

    except FileNotFoundError:
        print(f"\n  - Error: ffmpeg executable not found at '{FFMPEG_EXECUTABLE_PATH}'.")
        print("    Please ensure ffmpeg is correctly downloaded and the path in the script is accurate.")
        print("    You can download ffmpeg from: https://ffmpeg.org/download.html")
        current_state[video_url] = 'failed_ffmpeg_path' # Mark as failed
        save_state(STATE_FILE, current_state)
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n  - Error during ffmpeg merge for '{yt.title}':")
        print(f"    Command: {' '.join(e.cmd)}")
        print(f"    Return Code: {e.returncode}")
        print(f"    Stderr:\n    {e.stderr.strip()}")
        current_state[video_url] = 'failed_merge' # Mark as failed
        save_state(STATE_FILE, current_state)
        return False
    except Exception as e:
        print(f"\n  - An unexpected error occurred during download/merge for '{yt.title}': {e}")
        current_state[video_url] = 'failed_generic' # Mark as failed
        save_state(STATE_FILE, current_state)
        return False

def download_youtube_playlist_resumable(playlist_url, download_path='.'):
    """
    Downloads videos from a YouTube playlist, tracking progress in a JSON file
    to allow resuming.
    """
    try:
        download_path = os.path.normpath(download_path.strip())

        playlist = Playlist(playlist_url)
        print(f"Playlist Title: {playlist.title}")
        print(f"Number of videos: {len(playlist.video_urls)}")
        print("-" * 30)

        if not os.path.exists(download_path):
            os.makedirs(download_path)
            print(f"Created download directory: {download_path}")
            print("-" * 30)

        # --- Load existing state ---
        state = load_state(STATE_FILE)
        
        # --- Get all video URLs from the playlist once ---
        playlist_video_urls = list(playlist.video_urls)
        total_videos = len(playlist_video_urls)

        print("Starting download and merge process...\n")
        
        successful_downloads = 0
        failed_downloads = 0

        # Use tqdm with total, but also track progress manually from state
        # We'll iterate through the playlist URLs and check state
        
        for i, video_url in enumerate(playlist_video_urls):
            # Adjust index based on what's already in state if we want tqdm to be precise
            # For simplicity, let's just iterate and check state inside
            video_index = i + 1
            
            # Check if this video has already been completed
            if video_url in state and state[video_url] == 'completed':
                # print(f"[{video_index}/{total_videos}] Skipping video (already completed): {playlist.videos[i].title}") # Requires fetching titles again, or storing them in state
                continue

            try:
                yt = YouTube(video_url)
                video_title_sanitized = yt.title
                for char in '\\/:*?"<>|':
                    video_title_sanitized = video_title_sanitized.replace(char, '_')
                video_title_sanitized = video_title_sanitized[:100]

                video_stream, audio_stream = get_stream_details(yt)

                if video_stream and audio_stream:
                    # Pass current_state to the download function
                    if download_and_merge(yt, video_url, video_title_sanitized, video_index, total_videos, download_path, video_stream, audio_stream, state):
                        successful_downloads += 1
                    else:
                        failed_downloads += 1 # Error logged within download_and_merge

                else:
                    print(f"\n[{video_index}/{total_videos}] Skipping video: No suitable video/audio streams found for '{yt.title}'")
                    state[video_url] = 'failed_no_streams'
                    save_state(STATE_FILE, state)
                    failed_downloads += 1

            except Exception as e:
                print(f"\nError processing video URL {video_url} ({yt.title if 'yt' in locals() else 'Unknown'}): {e}")
                state[video_url] = 'failed_generic_processing'
                save_state(STATE_FILE, state)
                failed_downloads += 1
        
        # --- Final save of state after loop ---
        save_state(STATE_FILE, state)

        print("-" * 30)
        print(f"Playlist download and merge process finished.")
        print(f"Successfully processed: {successful_downloads} videos")
        print(f"Failed or skipped: {failed_downloads} videos")
        print(f"Check '{STATE_FILE}' for details on any failures.")


    except Exception as e:
        print(f"Critical Error: Could not process playlist URL '{playlist_url}'.")
        print(f"Error details: {e}")

if __name__ == "__main__":
    print("--- YouTube Playlist Downloader (Resumable) ---")
    playlist_link = input("Enter the YouTube Playlist URL: ")
    save_directory = input("Enter the directory to save videos (leave blank for current directory): ")

    if not save_directory:
        save_directory = '.'

    if FFMPEG_EXECUTABLE_PATH == r'C:\Path\To\Your\ffmpeg\bin\ffmpeg.exe':
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! IMPORTANT: Please update the FFMPEG_EXECUTABLE_PATH in the script !!!")
        print("!!! with the correct path to your ffmpeg.exe file.                 !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    else:
        download_youtube_playlist_resumable(playlist_link, save_directory)