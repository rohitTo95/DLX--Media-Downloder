# DLX Media Downloader
![Capture](https://github.com/user-attachments/assets/5068ed5a-fb62-4e49-a9e4-fa085d543315)

A simple web application to download YouTube videos in various formats.

## Features

* Download YouTube videos as **video** (MP4).
* Download YouTube videos as **audio** (MP3).
* Clean and intuitive user interface.
* Basic input validation.
* Asynchronous processing for faster downloads.
* Caching of recent downloads.
* Rate limiting to prevent abuse.
* Light and dark theme support.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd rohitto95-dlx--media-downloder
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Node.js dependencies (for CSS):**
    ```bash
    npm install
    ```

4.  **Run the CSS build process (watches for changes):**
    ```bash
    npm run build:css
    ```
    (Open a separate terminal for this command)

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will be accessible at `http://127.0.0.1:5000/` in your web browser.

## How to Use

1.  Open the application in your web browser.
2.  Paste the URL of the YouTube video you want to download into the input field.
3.  Click either the "Download Video" or "Download Audio" button.
4.  A status message will appear indicating the processing progress.
5.  Once the download is ready, a download link with the filename will be provided. Click the link to save the file.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any bugs or feature requests.
