# DLX Media Downloader

![Capture](https://github.com/user-attachments/assets/5068ed5a-fb62-4e49-a9e4-fa085d543315)

## Overview

DLX Media Downloader is a modern, web-based YouTube video and audio downloader built with Flask and a beautiful responsive interface. It allows users to effortlessly download YouTube videos in MP4 format or convert them to high-quality MP3 audio files. With its clean, intuitive design and powerful backend, DLX makes media downloading simple and accessible for everyone.

## Problem It Solves

In today's digital world, users often need to download YouTube content for offline viewing, educational purposes, or audio extraction. However, most existing solutions are either:
- **Cluttered with ads and pop-ups**
- **Require software installation**
- **Have poor user interfaces**
- **Lack proper error handling**
- **Don't support both video and audio formats**

DLX Media Downloader solves these problems by providing a clean, ad-free, web-based solution that works directly in your browser with session-based file management, intelligent caching, and rate limiting for optimal performance.

## Tech Stack

### Backend
- **Python 3.x**: Core programming language
- **Flask**: Lightweight web framework for the API
- **yt-dlp**: Robust YouTube video extraction library
- **moviepy**: Video processing and MP3 conversion
- **Flask-Limiter**: Rate limiting for API protection
- **cachelib**: In-memory caching system

### Frontend
- **HTML5**: Modern semantic markup
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Vanilla JavaScript**: Clean, dependency-free frontend interactions
- **CSS Grid & Flexbox**: Modern layout techniques

### Development Tools
- **Node.js & npm**: For CSS build process
- **Git**: Version control
- **dotenv**: Environment variable management

## How to Run

### Prerequisites
- Python 3.7 or higher
- Node.js and npm
- Git

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/DLX-Media-Downloader.git
   cd DLX-Media-Downloader
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

4. **Build CSS assets**:
   ```bash
   npm run build:css
   ```

5. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

6. **Run the application**:
   ```bash
   python app.py
   ```

7. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

### Development Mode

For development with auto-reload:
```bash
export FLASK_ENV=development
python app.py
```

For CSS development with watch mode:
```bash
npm run watch:css
```

## Features

- ✨ **Clean, Modern UI** with dark/light theme toggle
- 🚀 **Fast Downloads** with intelligent caching
- 🎵 **Dual Format Support** - MP4 video and MP3 audio
- 🛡️ **Rate Limiting** to prevent abuse
- 📱 **Responsive Design** works on all devices
- 🔒 **Session-based Security** with sanitized filenames
- ⚡ **Asynchronous Processing** for better performance
- 💾 **Smart Caching** to avoid redundant downloads

## API Endpoints

- `GET /` - Main application interface
- `POST /process` - Process download requests
- `GET /downloads/<filename>` - Serve downloaded files

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Built with ❤️ for the community**
