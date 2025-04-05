import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file if it exists

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key') # Change this!
    DOWNLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'downloads'))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Limit request size (e.g., 5MB) - adjust if needed
    # Rate limiting (e.g., 10 requests per minute per IP) - Adjust as needed!
    RATELIMIT_DEFAULT = "10/minute"
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'memory://') # Use redis for production: "redis://localhost:6379/1"

    # Concurrency settings
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 4).split()[0]) # Number of parallel processing workers

    # Caching settings (simple in-memory cache)
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300 # 5 minutes
    
    YT_DLP_PATH = os.environ.get('YT_DLP_PATH', 'yt-dlp') # Optional: if yt-dlp isn't in PATH

    # Ensure download folder exists
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

config = Config()