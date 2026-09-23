@echo off
cd /d "%~dp0"
echo Open http://localhost:8765/ in your browser.
echo Keep this window open while reading. Press Ctrl+C to stop.
python -m http.server 8765 --bind 127.0.0.1 --directory site
pause
