"""
Configuration settings for Jarvis Voice Assistant.
All configurable paths and settings are centralized here.
"""

import os
from pathlib import Path

# ============================================================
# PATHS CONFIGURATION
# ============================================================

# Chrome browser path (update if installed elsewhere)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Chrome WebDriver path (set to None for auto-management)
CHROMEDRIVER_PATH = None

# ============================================================
# VOICE SETTINGS
# ============================================================

# Wake word to activate the assistant
WAKE_WORD = "jarvis"

# Speech recognition settings
LISTEN_TIMEOUT = 5  # Seconds to wait for speech
PHRASE_TIME_LIMIT = 10  # Max seconds for a single phrase
ENERGY_THRESHOLD = 4000  # Microphone sensitivity
DYNAMIC_ENERGY = True  # Auto-adjust for ambient noise

# Text-to-speech settings
TTS_RATE = 175  # Words per minute
TTS_VOLUME = 1.0  # Volume (0.0 to 1.0)
TTS_VOICE_INDEX = 0  # Voice index

# ============================================================
# BROWSER AUTOMATION SETTINGS
# ============================================================

BROWSER_IMPLICIT_WAIT = 10  # Seconds to wait for elements
PAGE_LOAD_TIMEOUT = 30  # Seconds to wait for page load
HEADLESS_MODE = False  # Run browser in background

# YouTube settings
YOUTUBE_URL = "https://www.youtube.com"
YOUTUBE_SEARCH_DELAY = 2  # Seconds to wait after search

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / "jarvis.log"
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3

# ============================================================
# APPLICATION PATHS
# ============================================================

APPLICATIONS = {
    "chrome": CHROME_PATH,
    "google chrome": CHROME_PATH,
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "calc": r"C:\Windows\System32\calc.exe",
    "explorer": r"C:\Windows\explorer.exe",
    "file explorer": r"C:\Windows\explorer.exe",
    "cmd": r"C:\Windows\System32\cmd.exe",
    "command prompt": r"C:\Windows\System32\cmd.exe",
    "vscode": os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
    "visual studio code": os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
    "spotify": os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
}

# ============================================================
# ASSISTANT RESPONSES
# ============================================================

RESPONSES = {
    "greeting": [
        "Hello! How can I help you?",
        "Hi there! What would you like me to do?",
        "Greetings! I am ready to assist.",
    ],
    "acknowledgment": [
        "On it!",
        "Sure thing!",
        "Right away!",
        "Consider it done!",
    ],
    "not_understood": [
        "I didn't catch that. Could you repeat?",
        "Sorry, I didn't understand. Please try again.",
        "Could you say that again?",
    ],
    "error": [
        "Something went wrong. Please try again.",
        "I encountered an error. Let me try again.",
    ],
    "goodbye": [
        "Goodbye!",
        "See you later!",
        "Take care!",
    ],
}

# ============================================================
# COMMAND KEYWORDS
# ============================================================

COMMAND_KEYWORDS = {
    "open": ["open", "launch", "start", "run"],
    "close": ["close", "exit", "quit", "terminate"],
    "search": ["search", "find", "look for", "google"],
    "play": ["play", "watch", "stream"],
    "stop": ["stop", "pause", "halt"],
    "volume": ["volume", "sound"],
    "time": ["time", "clock"],
    "date": ["date", "day", "today"],
    "weather": ["weather", "temperature"],
    "goodbye": ["goodbye", "bye", "exit assistant", "quit assistant", "stop listening"],
}

# ============================================================
# ENSURE DIRECTORIES EXIST
# ============================================================

def ensure_directories():
    """Create necessary directories if they don't exist."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

ensure_directories()
