import yt_dlp
import os
import uuid
import logging
from moviepy import VideoFileClip
from .helper import sanitize_filename,check_file_exists, clear_user_downloads

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_video(youtube_url, format_type, user_folder, title=None):
    """Download video from YouTube and return final video path."""
    job_id = str(uuid.uuid4())
    temp_filename_base = os.path.join(user_folder, f"temp_{job_id}")

    # Extract title if not provided
    if not title:
        ydl_opts_info = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'force_generic_extractor': False,
            'paths': {'home': user_folder},
            'extractor_args': {'youtube': {'player_client': ['web', 'ios']}}
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)
            raw_title = info_dict.get('title', 'download')
            title = sanitize_filename(raw_title)

    file_info = check_file_exists(title, user_folder)
    if file_info["video_exists"]:
        logging.info(f"Video already exists: {file_info['video_path']}")
        return file_info["video_path"]

    clear_user_downloads(user_folder)

    ydl_opts_download = {
        'format': 'bv*+ba/best' if format_type == 'video' else 'bestaudio/best',
        'outtmpl': f'{temp_filename_base}.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'merge_output_format': 'mp4',
        'paths': {'home': user_folder},
        'extractor_args': {'youtube': {'player_client': ['web', 'ios']}}
    }

    with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
        logging.info(f"Downloading video for {title}")
        ydl.download([youtube_url])
        logging.info(f"Download finished")

    # Detect downloaded file and rename
    final_filepath = os.path.join(user_folder, f"{title}.mp4")
    for ext in ['.mp4', '.mkv', '.webm']:
        downloaded_file = f"{temp_filename_base}{ext}"
        if os.path.exists(downloaded_file):
            os.rename(downloaded_file, final_filepath)
            return final_filepath

    raise RuntimeError("Video download failed or unknown extension.")


def convert_video_to_audio(video_path, user_folder):
    """Convert .mp4 video to .mp3 using moviepy and return audio filename."""
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_filepath = os.path.join(user_folder, f"{base_name}.mp3")

    if os.path.exists(audio_filepath):
        logging.info(f"Audio file already exists: {audio_filepath}")
        return os.path.basename(audio_filepath)

    logging.info(f"Converting {video_path} to audio...")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_filepath)
    clip.close()

    return os.path.basename(audio_filepath)


def download_and_convert(youtube_url, format_type='video', user_folder=None):
    if user_folder is None:
        raise ValueError("User folder must be provided.")

    try:
        # Step 1: Download video if needed
        file_path = download_video(youtube_url, format_type, user_folder)

        # Step 2: Convert if requested format is audio
        if format_type == 'audio':
            file_path = convert_video_to_audio(file_path, user_folder)
            return file_path

        # Step 3: Return video filename
        return os.path.basename(file_path)

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"yt-dlp download error: {e}")
        raise RuntimeError(f"Download failed: {e}")

    except Exception as e:
        logging.exception("Unexpected error:")
        raise RuntimeError(f"An unexpected error occurred: {e}")
