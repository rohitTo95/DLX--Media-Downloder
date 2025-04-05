import os
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory, url_for, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from cachelib import SimpleCache
from utils.config import config
from utils.helper import sanitize_filename, is_valid_youtube_url, get_user_session_folder, clear_user_downloads
from utils.downloader import download_and_convert

app = Flask(__name__)
app.config.from_object(config)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.secret_key = config.SECRET_KEY  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[config.RATELIMIT_DEFAULT],
    storage_uri=config.RATELIMIT_STORAGE_URL
)

executor = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)
cache = SimpleCache(default_timeout=config.CACHE_DEFAULT_TIMEOUT)

# Map of original filenames to sanitized filenames
filename_map = {}

@app.route('/process', methods=['POST'])
@limiter.limit(config.RATELIMIT_DEFAULT)
def process_video():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    url = data.get('url')
    format_type = data.get('format', 'video').lower()

    if not url or not is_valid_youtube_url(url):
        return jsonify({"error": "Invalid or missing YouTube URL"}), 400

    user_folder = get_user_session_folder()
    # session_id = session['session_id']
    
    cache_key = f"{url}_{format_type}"
    cached_result = cache.get(cache_key)

    # ✅ CHECK CACHE FIRST before deleting anything
    if cached_result:
        sanitized_path = os.path.join(user_folder, cached_result['sanitized_filename'])
        if os.path.exists(sanitized_path):
            return jsonify({
                "message": "File ready (cached)",
                "download_url": url_for('download_file', filename=cached_result['original_filename'], _external=True),
                "filename": cached_result['original_filename']
            })

    try:
        future = executor.submit(download_and_convert, url, format_type, user_folder)
        original_filename = future.result(timeout=600)

        if not original_filename:
            raise RuntimeError("Processing completed but returned an empty filename.")
            
        sanitized_filename = sanitize_filename(original_filename)
        original_path = os.path.join(user_folder, original_filename)
        sanitized_path = os.path.join(user_folder, sanitized_filename)

        if original_path != sanitized_path and os.path.exists(original_path):
            os.rename(original_path, sanitized_path)

        filename_map[original_filename] = sanitized_filename
        cache.set(cache_key, {
            "original_filename": original_filename,
            "sanitized_filename": sanitized_filename
        })

        return jsonify({
            "message": "Processing complete!",
            "download_url": url_for('download_file', filename=original_filename, _external=True),
            "filename": original_filename
        })
    
    except FutureTimeoutError:
        return jsonify({"error": "Processing timed out."}), 504
    except Exception as e:
        logging.exception("Unexpected error: %s", e)
        return jsonify({"error": "An unexpected server error occurred."}), 500


@app.route('/downloads/<path:filename>')
def download_file(filename):
    """Serve the file from the user's session folder."""
    user_folder = get_user_session_folder()
    
    # Look up the sanitized filename
    sanitized_filename = filename_map.get(filename, sanitize_filename(filename))
    logging.info(f"Download requested - Original: {filename}, Sanitized: {sanitized_filename}")
    
    file_path = os.path.join(user_folder, sanitized_filename)
    
    # If file doesn't exist, try with the original name as fallback
    if not os.path.exists(file_path):
        original_path = os.path.join(user_folder, filename)
        if os.path.exists(original_path):
            logging.info(f"Using original filename for download: {filename}")
            return send_from_directory(user_folder, filename, as_attachment=True)
        
        # Debug: Log directory contents
        logging.warning(f"File not found: {file_path}")
        if os.path.exists(user_folder):
            logging.info(f"Directory contents: {os.listdir(user_folder)}")
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(user_folder, sanitized_filename, as_attachment=True)

@app.route('/')
def index():
    # Ensure session is initialized
    get_user_session_folder()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)