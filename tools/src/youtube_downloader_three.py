from pytubefix import Playlist, YouTube
from tqdm import tqdm
import os
import subprocess # For running ffmpeg commands

# --- CONFIGURATION ---
# IMPORTANT: Replace this with the ACTUAL path to your ffmpeg.exe file.
# Example: r'C:\ffmpeg\bin\ffmpeg.exe' or r'C:\Users\YourUsername\Downloads\ffmpeg-N.N.N-essentials_build\bin\ffmpeg.exe'
# Using a raw string (r'...') is recommended for Windows paths to avoid issues with backslashes.
#FFMPEG_EXECUTABLE_PATH = r'C:\Path\To\Your\ffmpeg\bin\ffmpeg.exe' # <--- *** UPDATE THIS PATH ***
#FFMPEG_EXECUTABLE_PATH = r'C:\Development\Python\Tools\youtube_downloader\ffmpeg-8.0\bin\ffmpeg.exe'

FFMPEG_EXECUTABLE_PATH = r'C:\Development\Python\Tools\youtube_downloader\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe'


# ---------------------

def download_youtube_playlist_high_quality(playlist_url, download_path='.'):
    """
    Downloads videos from a YouTube playlist, attempting to get the highest quality
    (adaptive streams) and merges them using ffmpeg.

    Args:
        playlist_url (str): The URL of the YouTube playlist.
        download_path (str): The directory where videos will be saved.
                             Defaults to the current directory.
    """
    try:
        # Sanitize the download path to remove potential hidden characters and normalize
        download_path = os.path.normpath(download_path.strip())

        playlist = Playlist(playlist_url)
        print(f"Playlist Title: {playlist.title}")
        print(f"Number of videos: {len(playlist.video_urls)}")
        print("-" * 30)

        # Create download directory if it doesn't exist
        if not os.path.exists(download_path):
            os.makedirs(download_path)
            print(f"Created download directory: {download_path}")
            print("-" * 30)

        print("Starting download and merge process...\n")

        for i, video_url in enumerate(tqdm(playlist.video_urls, desc="Processing Videos", unit="video")):
            try:
                yt = YouTube(video_url)
                # Sanitize title for filename: replace problematic characters with underscores
                video_title = yt.title
                for char in '\\/:*?"<>|': # Invalid characters in Windows filenames
                    video_title = video_title.replace(char, '_')
                # Further clean up potential issues with long filenames or other oddities
                video_title = video_title[:100] # Limit length to avoid filesystem issues


                # --- Get the best video-only stream ---
                # filter for adaptive streams (video and audio separate), progressive=False
                # order by resolution descending, and get the first one
                video_stream = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()

                if not video_stream:
                    # If no mp4 adaptive, try webm adaptive (often higher res)
                    video_stream = yt.streams.filter(adaptive=True, file_extension='webm').order_by('resolution').desc().first()

                # --- Get the best audio-only stream ---
                # Prioritize MP4 audio streams, then fall back to any audio stream
                audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
                if not audio_stream:
                    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                if video_stream and audio_stream:
                    print(f"\n[{i+1}/{len(playlist.video_urls)}] Downloading: {yt.title}") # Show original title for clarity

                    # Define filenames for video and audio before downloading
                    # Adding index for consistent ordering and unique filenames
                    video_filename_part = os.path.join(download_path, f"{i+1:03d}_{video_title}_video.{video_stream.subtype}")
                    audio_filename_part = os.path.join(download_path, f"{i+1:03d}_{video_title}_audio.{audio_stream.subtype}")
                    output_filename = os.path.join(download_path, f"{i+1:03d}_{video_title}.mp4") # Final merged file

                    # Download video stream if it doesn't exist
                    if not os.path.exists(video_filename_part):
                        print(f"  - Video Stream: {video_stream.resolution} ({video_stream.mime_type})")
                        video_stream.download(output_path=download_path, filename=os.path.basename(video_filename_part))
                    else:
                        print(f"  - Video file already exists: {os.path.basename(video_filename_part)}")

                    # Download audio stream if it doesn't exist
                    if not os.path.exists(audio_filename_part):
                        print(f"  - Audio Stream: {audio_stream.abr} ({audio_stream.mime_type})")
                        audio_stream.download(output_path=download_path, filename=os.path.basename(audio_filename_part))
                    else:
                        print(f"  - Audio file already exists: {os.path.basename(audio_filename_part)}")

                    # --- Merge video and audio using ffmpeg ---
                    if not os.path.exists(output_filename):
                        print(f"  - Merging video and audio...")
                        try:
                            # Construct the ffmpeg command using the specified path
                            
                            merge_cmd_args = [
                                FFMPEG_EXECUTABLE_PATH,
                                '-i', video_filename_part,
                                '-i', audio_filename_part,
                                # Removed '-c:a', 'aac' and '-strict', 'experimental'
                                # Let ffmpeg determine the best audio codec or use its default
                                '-map', '0:v:0',      # Map the first video stream from the first input (video file)
                                '-map', '1:a:0',      # Map the first audio stream from the second input (audio file)
                                '-y'                  # Overwrite output file if it exists without asking
                            ]

                            # If video is not mp4 (e.g., webm), we need to re-encode video
                            if video_stream.subtype == 'webm':
                                merge_cmd_args.insert(1, '-c:v') # Add video codec argument
                                merge_cmd_args.insert(2, 'libx264') # Use H.264 for video encoding
                                merge_cmd_args.insert(3, '-crf')    # Constant Rate Factor for quality
                                merge_cmd_args.insert(4, '23')      # Typical quality setting (18-28)
                                # Optional: Add preset for encoding speed vs compression
                                # merge_cmd_args.insert(5, '-preset')
                                # merge_cmd_args.insert(6, 'medium')

                            # Add the output filename at the end
                            merge_cmd_args.append(output_filename)

                            # Execute the ffmpeg command and capture output for debugging
                            process = subprocess.run(merge_cmd_args, check=True, capture_output=True, text=True)
                            print(f"  - Successfully merged: {os.path.basename(output_filename)}")
                            
                            # Print ffmpeg's standard error for debugging if there were warnings or issues
                            if process.stderr:
                                print("  - ffmpeg output (stderr):\n    " + process.stderr.replace('\n', '\n    '))

                            # Clean up the individual video and audio files after successful merge
                            try:
                                os.remove(video_filename_part)
                                os.remove(audio_filename_part)
                                # print("  - Cleaned up temporary files.")
                            except OSError as e:
                                print(f"  - Error cleaning up temporary files: {e}")

                        except FileNotFoundError:
                            print(f"\n  - Error: ffmpeg executable not found at '{FFMPEG_EXECUTABLE_PATH}'.")
                            print("    Please ensure ffmpeg is correctly downloaded and the path in the script is accurate.")
                            print("    You can download ffmpeg from: https://ffmpeg.org/download.html")
                        except subprocess.CalledProcessError as e:
                            print(f"\n  - Error during ffmpeg merge for '{yt.title}':")
                            print(f"    Command: {' '.join(e.cmd)}")
                            print(f"    Return Code: {e.returncode}")
                            print(f"    Stderr:\n    {e.stderr.strip()}") # Use strip to clean up extra newlines
                        except Exception as e:
                            print(f"\n  - An unexpected error occurred during merging: {e}")
                    else:
                        print(f"  - Merged file already exists: {os.path.basename(output_filename)}. Skipping merge.")
                        # Optionally clean up if merged file exists but parts don't
                        if os.path.exists(video_filename_part): os.remove(video_filename_part)
                        if os.path.exists(audio_filename_part): os.remove(audio_filename_part)

            except Exception as e:
                # This catch-all is for errors during YouTube object creation or stream selection
                print(f"\nError processing video URL {video_url} ({yt.title if 'yt' in locals() else 'Unknown'}): {e}")

        print("-" * 30)
        print("Playlist download and merge process completed!")

    except Exception as e:
        # This catch-all is for errors when creating the Playlist object itself or processing the playlist
        print(f"Critical Error: Could not process playlist URL '{playlist_url}'.")
        print(f"Error details: {e}")

if __name__ == "__main__":
    print("--- YouTube Playlist Downloader (High Quality with ffmpeg) ---")
    playlist_link = input("Enter the YouTube Playlist URL: ")
    save_directory = input("Enter the directory to save videos (leave blank for current directory): ")

    if not save_directory:
        save_directory = '.'

    # Check if the ffmpeg path is set correctly before proceeding
    if FFMPEG_EXECUTABLE_PATH == r'C:\Path\To\Your\ffmpeg\bin\ffmpeg.exe':
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!! IMPORTANT: Please update the FFMPEG_EXECUTABLE_PATH in the script !!!")
        print("!!! with the correct path to your ffmpeg.exe file.                 !!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    else:
        download_youtube_playlist_high_quality(playlist_link, save_directory)