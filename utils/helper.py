import re 
import os 
import uuid
import logging
from flask import session
from .config import config
def sanitize_filename(filename):
    # Split filename and extension
    if '.' in filename:
        name_part, extension = filename.rsplit('.', 1)
        has_extension = True
    else:
        name_part = filename
        extension = ''
        has_extension = False

    # Remove special characters from the beginning
    name_part = re.sub(r'^[^a-zA-Z0-9]+', '', name_part)

    # Replace invalid characters with underscores
    name_part = re.sub(r'[^\w\-]', '_', name_part)

    # Convert "filename(1)" or "filename (1)" to "filename1"
    name_part = re.sub(r'\s*\((\d+)\)\s*', r'\1', name_part)

    # Remove leading/trailing underscores
    name_part = name_part.strip('_')

    # Replace multiple consecutive underscores with a single one
    name_part = re.sub(r'_+', '_', name_part)

    # Limit filename length (but preserve extension)
    if len(name_part) > 180:  # Leave room for extension
        name_part = name_part[:180]

    # Recombine with extension
    if has_extension:
        sanitized = f"{name_part}.{extension}"
    else:
        sanitized = name_part

    return sanitized

def is_valid_youtube_url(url):
    return any(sub in url for sub in ["youtube.com/watch?v=", "youtu.be/", "youtube.com/shorts/", "music.youtube.com/watch?v="])

def get_user_session_folder():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())  # Unique session ID
        logging.info(f"Created new session ID: {session['session_id']}")
    else:
        logging.info(f"Using existing session ID: {session['session_id']}")
        
    user_folder = os.path.join(config.DOWNLOAD_FOLDER, session['session_id'])
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def clear_user_downloads(user_folder):
    """Delete all files in the user's session folder before processing a new request."""
    for file in os.listdir(user_folder):
        file_path = os.path.join(user_folder, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"Deleted previous file: {file_path}")
        except Exception as e:
            logging.warning(f"Could not delete {file_path}: {e}")
            
            
def check_file_exists(title, user_folder):
    """Check if MP4 video and/or MP3 audio with the sanitized title exists."""
    sanitized_title = sanitize_filename(title)
    video_path = os.path.join(user_folder, f"{sanitized_title}.mp4")
    audio_path = os.path.join(user_folder, f"{sanitized_title}.mp3")

    video_exists = os.path.exists(video_path)
    audio_exists = os.path.exists(audio_path)

    return {
        "title": sanitized_title,
        "video_exists": video_exists,
        "audio_exists": audio_exists,
        "video_path": video_path if video_exists else None,
        "audio_path": audio_path if audio_exists else None
    }
