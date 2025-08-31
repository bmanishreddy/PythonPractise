from pytubefix import Playlist, YouTube
from tqdm import tqdm
import os

def download_youtube_playlist(playlist_url, download_path='.'):
    """
    Downloads all videos from a YouTube playlist.

    Args:
        playlist_url (str): The URL of the YouTube playlist.
        download_path (str): The directory where videos will be saved.
                             Defaults to the current directory.
    """
    try:
        # Sanitize the download path to remove potential hidden characters
        # This is a more robust way to handle unexpected input
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

        # Use tqdm for a progress bar
        for i, video_url in enumerate(tqdm(playlist.video_urls, desc="Downloading Videos", unit="video")):
            try:
                yt = YouTube(video_url)

                # Filter for the highest resolution progressive stream (mp4)
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

                if stream:
                    stream.download(output_path=download_path)
                else:
                    print(f"\nWarning: No suitable progressive MP4 stream found for '{yt.title}'. Skipping.")

            except Exception as e:
                print(f"\nError downloading video {video_url}: {e}")

        print("-" * 30)
        print("Playlist download complete!")

    except Exception as e:
        print(f"Error processing playlist URL '{playlist_url}': {e}")

if __name__ == "__main__":
    print("--- YouTube Playlist Downloader ---")
    playlist_link = input("Enter the YouTube Playlist URL: ")
    save_directory = input("Enter the directory to save videos (leave blank for current directory): ")

    if not save_directory:
        save_directory = '.'

    # Download the playlist
    download_youtube_playlist(playlist_link, save_directory)