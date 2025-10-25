"""
Startup script for Election Tracker Web Server.
Run this to start the web interface on localhost:4000
"""
import subprocess
import sys
import time
import webbrowser
from threading import Timer

def open_browser():
    """Open browser after a short delay."""
    time.sleep(1.5)
    webbrowser.open('http://localhost:4000')

def main():
    print("=" * 60)
    print("Election Tracker Web Server")
    print("=" * 60)
    print()
    print("Starting web server on http://localhost:4000")
    print("Press Ctrl+C to stop the server")
    print()
    
    # Open browser after delay
    Timer(2.0, open_browser).start()
    
    try:
        # Start Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        print("Thank you for using Election Tracker!")

if __name__ == "__main__":
    main()
