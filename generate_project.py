"""
Jarvis Voice Assistant - Complete Project Generator
Run this script to generate all project files in the correct structure.

Usage: python generate_project.py
"""

import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
JARVIS_PATH = os.path.join(BASE_PATH, "jarvis")

# ============================================================
# FILE CONTENTS
# ============================================================

CONFIG_PY = '''"""
Configuration settings for Jarvis Voice Assistant.
All configurable paths and settings are centralized here.
"""

import os
from pathlib import Path

# ============================================================
# PATHS CONFIGURATION
# ============================================================

# Chrome browser path (update if installed elsewhere)
CHROME_PATH = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

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
    "firefox": r"C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    "notepad": r"C:\\Windows\\System32\\notepad.exe",
    "calculator": r"C:\\Windows\\System32\\calc.exe",
    "calc": r"C:\\Windows\\System32\\calc.exe",
    "explorer": r"C:\\Windows\\explorer.exe",
    "file explorer": r"C:\\Windows\\explorer.exe",
    "cmd": r"C:\\Windows\\System32\\cmd.exe",
    "command prompt": r"C:\\Windows\\System32\\cmd.exe",
    "vscode": os.path.expandvars(r"%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\Code.exe"),
    "visual studio code": os.path.expandvars(r"%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\Code.exe"),
    "spotify": os.path.expandvars(r"%APPDATA%\\Spotify\\Spotify.exe"),
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
'''

# ============================================================

UTILS_INIT_PY = '''"""
Utility modules for Jarvis Voice Assistant.
"""

from .logger import get_logger, setup_logging
from .helpers import (
    get_random_response,
    clean_text,
    get_current_time,
    get_current_date,
)

__all__ = [
    "get_logger",
    "setup_logging",
    "get_random_response",
    "clean_text",
    "get_current_time",
    "get_current_date",
]
'''

# ============================================================

UTILS_LOGGER_PY = '''"""
Logging utility for Jarvis Voice Assistant.
Provides centralized logging with file and console output.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional

# Import config - handle both direct run and module import
try:
    from config import LOG_FILE, LOG_LEVEL, LOG_FORMAT, LOG_MAX_BYTES, LOG_BACKUP_COUNT
except ImportError:
    from ..config import LOG_FILE, LOG_LEVEL, LOG_FORMAT, LOG_MAX_BYTES, LOG_BACKUP_COUNT


def setup_logging() -> None:
    """
    Configure the root logger with file and console handlers.
    Should be called once at application startup.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    formatter = logging.Formatter(LOG_FORMAT)
    
    # File handler with rotation
    try:
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create log file: {e}")
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name or "jarvis")
'''

# ============================================================

UTILS_HELPERS_PY = '''"""
Helper utilities for Jarvis Voice Assistant.
Common functions used across modules.
"""

import random
import re
from typing import List, Optional
from datetime import datetime

# Import config - handle both direct run and module import
try:
    from config import RESPONSES
except ImportError:
    from ..config import RESPONSES


def get_random_response(response_type: str) -> str:
    """
    Get a random response from the configured responses.
    
    Args:
        response_type: Type of response (greeting, acknowledgment, etc.)
        
    Returns:
        Random response string
    """
    responses = RESPONSES.get(response_type, RESPONSES["not_understood"])
    return random.choice(responses)


def clean_text(text: str) -> str:
    """
    Clean and normalize text for processing.
    
    Args:
        text: Raw text input
        
    Returns:
        Cleaned text (lowercase, trimmed, normalized whitespace)
    """
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'\\s+', ' ', text)
    text = re.sub(r"[^\\w\\s\\'-]", '', text)
    return text


def extract_after_keyword(text: str, keywords: List[str]) -> Optional[str]:
    """
    Extract text that comes after any of the given keywords.
    
    Args:
        text: Full text to search
        keywords: List of keywords to look for
        
    Returns:
        Text after the keyword, or None if no keyword found
    """
    text_lower = text.lower()
    for keyword in keywords:
        if keyword in text_lower:
            idx = text_lower.find(keyword) + len(keyword)
            result = text[idx:].strip()
            if result:
                return result
    return None


def get_current_time() -> str:
    """Get current time as formatted string."""
    return datetime.now().strftime("%I:%M %p")


def get_current_date() -> str:
    """Get current date as formatted string."""
    return datetime.now().strftime("%A, %B %d, %Y")


def find_best_match(query: str, options: List[str]) -> Optional[str]:
    """
    Find the best matching option for a query.
    
    Args:
        query: Search query
        options: List of options to match against
        
    Returns:
        Best matching option or None
    """
    query_words = set(clean_text(query).split())
    
    best_match = None
    best_score = 0
    
    for option in options:
        option_words = set(clean_text(option).split())
        score = len(query_words & option_words)
        if score > best_score:
            best_score = score
            best_match = option
            
    return best_match if best_score > 0 else None


def is_affirmative(text: str) -> bool:
    """Check if text is an affirmative response."""
    affirmatives = {"yes", "yeah", "yep", "sure", "ok", "okay", "definitely", "absolutely", "correct", "right"}
    return clean_text(text) in affirmatives


def is_negative(text: str) -> bool:
    """Check if text is a negative response."""
    negatives = {"no", "nope", "nah", "negative", "cancel", "never"}
    return clean_text(text) in negatives
'''

# ============================================================

ACTIONS_INIT_PY = '''"""
Action modules for Jarvis Voice Assistant.
Each module handles a specific category of commands.
"""

from .open_apps import open_application, close_application
from .youtube import YouTubeController

__all__ = [
    "open_application",
    "close_application",
    "YouTubeController",
]
'''

# ============================================================

ACTIONS_OPEN_APPS_PY = '''"""
Application launcher module for Jarvis Voice Assistant.
Handles opening and closing desktop applications.
"""

import subprocess
import os
from typing import Optional, Tuple
import logging

# Import config
try:
    from config import APPLICATIONS, CHROME_PATH
except ImportError:
    from ..config import APPLICATIONS, CHROME_PATH

logger = logging.getLogger(__name__)


def open_application(app_name: str) -> Tuple[bool, str]:
    """
    Open an application by name.
    
    Args:
        app_name: Name of the application to open
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    app_name_lower = app_name.lower().strip()
    
    # Check if app is in configured applications
    app_path = APPLICATIONS.get(app_name_lower)
    
    if not app_path:
        # Try to find partial match
        for name, path in APPLICATIONS.items():
            if app_name_lower in name or name in app_name_lower:
                app_path = path
                break
    
    if not app_path:
        logger.warning(f"Application not found: {app_name}")
        return False, f"I don't know how to open {app_name}"
    
    # Expand environment variables
    app_path = os.path.expandvars(app_path)
    
    # Check if application exists
    if not os.path.exists(app_path.split()[0]):  # Handle paths with arguments
        logger.error(f"Application path does not exist: {app_path}")
        return False, f"{app_name} is not installed at the expected location"
    
    try:
        # Use subprocess to open the application
        if " " in app_path and "--" in app_path:
            # Handle paths with arguments (like Discord)
            subprocess.Popen(app_path, shell=True)
        else:
            subprocess.Popen([app_path], shell=False)
        
        logger.info(f"Successfully opened: {app_name}")
        return True, f"Opening {app_name}"
        
    except FileNotFoundError:
        logger.error(f"File not found: {app_path}")
        return False, f"Could not find {app_name}"
    except PermissionError:
        logger.error(f"Permission denied: {app_path}")
        return False, f"Permission denied to open {app_name}"
    except Exception as e:
        logger.error(f"Error opening {app_name}: {e}")
        return False, f"Error opening {app_name}"


def close_application(app_name: str) -> Tuple[bool, str]:
    """
    Close an application by name (Windows only).
    
    Args:
        app_name: Name of the application to close
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    # Map common names to process names
    process_names = {
        "chrome": "chrome.exe",
        "google chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "notepad": "notepad.exe",
        "calculator": "Calculator.exe",
        "explorer": "explorer.exe",
        "vscode": "Code.exe",
        "visual studio code": "Code.exe",
        "spotify": "Spotify.exe",
    }
    
    app_name_lower = app_name.lower().strip()
    process_name = process_names.get(app_name_lower, f"{app_name_lower}.exe")
    
    try:
        # Use taskkill on Windows
        result = subprocess.run(
            ["taskkill", "/F", "/IM", process_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info(f"Successfully closed: {app_name}")
            return True, f"Closed {app_name}"
        else:
            logger.warning(f"Could not close {app_name}: {result.stderr}")
            return False, f"{app_name} is not running"
            
    except Exception as e:
        logger.error(f"Error closing {app_name}: {e}")
        return False, f"Error closing {app_name}"


def open_url_in_browser(url: str, browser: str = "chrome") -> Tuple[bool, str]:
    """
    Open a URL in the specified browser.
    
    Args:
        url: URL to open
        browser: Browser to use (default: chrome)
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    browser_paths = {
        "chrome": CHROME_PATH,
        "firefox": APPLICATIONS.get("firefox", ""),
    }
    
    browser_path = browser_paths.get(browser.lower(), CHROME_PATH)
    browser_path = os.path.expandvars(browser_path)
    
    if not os.path.exists(browser_path):
        logger.error(f"Browser not found: {browser_path}")
        return False, f"{browser} is not installed"
    
    try:
        subprocess.Popen([browser_path, url])
        logger.info(f"Opened URL: {url}")
        return True, f"Opening {url}"
    except Exception as e:
        logger.error(f"Error opening URL: {e}")
        return False, f"Could not open {url}"
'''

# ============================================================

ACTIONS_YOUTUBE_PY = '''"""
YouTube automation module for Jarvis Voice Assistant.
Handles YouTube search and video playback using Selenium.
"""

import time
import logging
from typing import Optional, Tuple
from urllib.parse import quote_plus

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import (
        TimeoutException,
        NoSuchElementException,
        WebDriverException,
    )
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Import config
try:
    from config import (
        CHROME_PATH,
        CHROMEDRIVER_PATH,
        BROWSER_IMPLICIT_WAIT,
        PAGE_LOAD_TIMEOUT,
        HEADLESS_MODE,
        YOUTUBE_URL,
        YOUTUBE_SEARCH_DELAY,
    )
except ImportError:
    from ..config import (
        CHROME_PATH,
        CHROMEDRIVER_PATH,
        BROWSER_IMPLICIT_WAIT,
        PAGE_LOAD_TIMEOUT,
        HEADLESS_MODE,
        YOUTUBE_URL,
        YOUTUBE_SEARCH_DELAY,
    )

logger = logging.getLogger(__name__)


class YouTubeController:
    """
    Controller for YouTube browser automation.
    Handles searching and playing videos.
    """
    
    def __init__(self):
        """Initialize the YouTube controller."""
        self.driver: Optional[webdriver.Chrome] = None
        self._initialized = False
        
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium is not installed. YouTube features unavailable.")
    
    def _setup_driver(self) -> bool:
        """
        Set up the Chrome WebDriver.
        
        Returns:
            True if successful, False otherwise
        """
        if not SELENIUM_AVAILABLE:
            return False
            
        if self._initialized and self.driver:
            return True
        
        try:
            # Configure Chrome options
            chrome_options = Options()
            
            # Set Chrome binary location
            chrome_options.binary_location = CHROME_PATH
            
            # Common options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-popup-blocking")
            
            # Disable automation flags to avoid detection
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            # Headless mode if configured
            if HEADLESS_MODE:
                chrome_options.add_argument("--headless=new")
            
            # Set up driver service
            if CHROMEDRIVER_PATH:
                service = Service(CHROMEDRIVER_PATH)
            else:
                # Use webdriver-manager for automatic driver management
                service = Service(ChromeDriverManager().install())
            
            # Create driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(BROWSER_IMPLICIT_WAIT)
            self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            
            self._initialized = True
            logger.info("Chrome WebDriver initialized successfully")
            return True
            
        except WebDriverException as e:
            logger.error(f"WebDriver error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {e}")
            return False
    
    def search_and_play(self, query: str) -> Tuple[bool, str]:
        """
        Search YouTube and play the first video result.
        
        Args:
            query: Search query for YouTube
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self._setup_driver():
            return False, "Could not start browser. Is Chrome installed?"
        
        try:
            # Navigate to YouTube
            logger.info(f"Navigating to YouTube to search: {query}")
            search_url = f"{YOUTUBE_URL}/results?search_query={quote_plus(query)}"
            self.driver.get(search_url)
            
            # Wait for search results to load
            time.sleep(YOUTUBE_SEARCH_DELAY)
            
            # Wait for and click the first video
            wait = WebDriverWait(self.driver, 10)
            
            # Try multiple selectors for video results
            selectors = [
                "ytd-video-renderer #video-title",
                "a#video-title",
                "ytd-video-renderer a.ytd-thumbnail",
                "#contents ytd-video-renderer"
            ]
            
            video_clicked = False
            for selector in selectors:
                try:
                    video = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    video.click()
                    video_clicked = True
                    logger.info(f"Clicked video using selector: {selector}")
                    break
                except (TimeoutException, NoSuchElementException):
                    continue
            
            if not video_clicked:
                logger.warning("Could not find video to click")
                return False, "Could not find videos for that search"
            
            # Wait for video to start loading
            time.sleep(2)
            
            logger.info(f"Successfully started playing: {query}")
            return True, f"Playing {query} on YouTube"
            
        except TimeoutException:
            logger.error("Timeout waiting for YouTube to load")
            return False, "YouTube took too long to respond"
        except WebDriverException as e:
            logger.error(f"Browser error: {e}")
            return False, "Browser encountered an error"
        except Exception as e:
            logger.error(f"Error searching YouTube: {e}")
            return False, f"Error playing video: {str(e)}"
    
    def open_youtube(self) -> Tuple[bool, str]:
        """
        Open YouTube homepage.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self._setup_driver():
            return False, "Could not start browser"
        
        try:
            self.driver.get(YOUTUBE_URL)
            logger.info("Opened YouTube homepage")
            return True, "Opening YouTube"
        except Exception as e:
            logger.error(f"Error opening YouTube: {e}")
            return False, "Could not open YouTube"
    
    def pause_video(self) -> Tuple[bool, str]:
        """Pause the currently playing video."""
        if not self.driver:
            return False, "Browser is not open"
        
        try:
            # Press 'k' to toggle play/pause on YouTube
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys("k")
            return True, "Video paused"
        except Exception as e:
            logger.error(f"Error pausing video: {e}")
            return False, "Could not pause video"
    
    def close(self) -> None:
        """Close the browser and clean up resources."""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            finally:
                self.driver = None
                self._initialized = False
    
    def __del__(self):
        """Destructor to ensure browser is closed."""
        self.close()
'''

# ============================================================

LISTENER_PY = '''"""
Voice input listener module for Jarvis Voice Assistant.
Handles microphone input and speech-to-text conversion.
"""

import logging
from typing import Optional, Callable
from threading import Thread, Event
from queue import Queue, Empty

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

from config import (
    WAKE_WORD,
    LISTEN_TIMEOUT,
    PHRASE_TIME_LIMIT,
    ENERGY_THRESHOLD,
    DYNAMIC_ENERGY,
)

logger = logging.getLogger(__name__)


class VoiceListener:
    """
    Handles continuous voice listening and speech-to-text conversion.
    Supports wake word detection and background listening.
    """
    
    def __init__(self):
        """Initialize the voice listener."""
        if not SPEECH_RECOGNITION_AVAILABLE:
            raise ImportError("SpeechRecognition library is not installed")
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configure recognizer
        self.recognizer.energy_threshold = ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = DYNAMIC_ENERGY
        
        # Background listening state
        self._stop_event = Event()
        self._command_queue: Queue = Queue()
        self._background_thread: Optional[Thread] = None
        
        # Calibrate for ambient noise on initialization
        self._calibrate_microphone()
    
    def _calibrate_microphone(self) -> None:
        """Calibrate the microphone for ambient noise levels."""
        logger.info("Calibrating microphone for ambient noise...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info(f"Microphone calibrated. Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            logger.error(f"Error calibrating microphone: {e}")
    
    def listen_once(self, prompt: bool = True) -> Optional[str]:
        """
        Listen for a single voice command.
        
        Args:
            prompt: Whether to log a listening prompt
            
        Returns:
            Recognized text or None if recognition failed
        """
        if prompt:
            logger.info("Listening...")
        
        try:
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=LISTEN_TIMEOUT,
                    phrase_time_limit=PHRASE_TIME_LIMIT
                )
            
            # Convert speech to text using Google's API
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text.strip()
            
        except sr.WaitTimeoutError:
            logger.debug("Listening timed out, no speech detected")
            return None
        except sr.UnknownValueError:
            logger.debug("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error during listening: {e}")
            return None
    
    def listen_for_wake_word(self) -> bool:
        """
        Listen for the wake word.
        
        Returns:
            True if wake word detected, False otherwise
        """
        text = self.listen_once(prompt=False)
        if text and WAKE_WORD.lower() in text.lower():
            logger.info(f"Wake word '{WAKE_WORD}' detected!")
            return True
        return False
    
    def listen_with_wake_word(self) -> Optional[str]:
        """
        Listen for wake word, then listen for command.
        
        Returns:
            Command text (excluding wake word) or None
        """
        text = self.listen_once(prompt=False)
        if not text:
            return None
        
        text_lower = text.lower()
        
        # Check if wake word is present
        if WAKE_WORD.lower() in text_lower:
            # Extract command after wake word
            wake_idx = text_lower.find(WAKE_WORD.lower())
            command = text[wake_idx + len(WAKE_WORD):].strip()
            
            # If command is empty, listen again for the actual command
            if not command:
                logger.info("Wake word detected, listening for command...")
                return self.listen_once()
            
            return command
        
        return None
    
    def start_background_listening(self, callback: Callable[[str], None]) -> None:
        """
        Start listening in the background.
        
        Args:
            callback: Function to call with recognized text
        """
        if self._background_thread and self._background_thread.is_alive():
            logger.warning("Background listening already active")
            return
        
        self._stop_event.clear()
        
        def background_listen():
            logger.info("Background listening started")
            while not self._stop_event.is_set():
                text = self.listen_with_wake_word()
                if text:
                    callback(text)
        
        self._background_thread = Thread(target=background_listen, daemon=True)
        self._background_thread.start()
    
    def stop_background_listening(self) -> None:
        """Stop background listening."""
        self._stop_event.set()
        if self._background_thread:
            self._background_thread.join(timeout=2)
            self._background_thread = None
        logger.info("Background listening stopped")
    
    def get_command_from_queue(self, timeout: float = 0.1) -> Optional[str]:
        """
        Get a command from the background listening queue.
        
        Args:
            timeout: Time to wait for command
            
        Returns:
            Command text or None
        """
        try:
            return self._command_queue.get(timeout=timeout)
        except Empty:
            return None


def test_microphone() -> bool:
    """
    Test if the microphone is working.
    
    Returns:
        True if microphone is functional
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        print("SpeechRecognition library is not installed")
        return False
    
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Microphone detected. Testing...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Microphone is working!")
            return True
    except OSError as e:
        print(f"Microphone error: {e}")
        return False
    except Exception as e:
        print(f"Error testing microphone: {e}")
        return False
'''

# ============================================================

SPEAKER_PY = '''"""
Text-to-speech module for Jarvis Voice Assistant.
Handles voice output and spoken responses.
"""

import logging
from typing import Optional
from threading import Thread, Lock
from queue import Queue, Empty

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

from config import TTS_RATE, TTS_VOLUME, TTS_VOICE_INDEX

logger = logging.getLogger(__name__)


class VoiceSpeaker:
    """
    Handles text-to-speech conversion and voice output.
    Supports non-blocking speech in a separate thread.
    """
    
    def __init__(self):
        """Initialize the voice speaker."""
        if not PYTTSX3_AVAILABLE:
            raise ImportError("pyttsx3 library is not installed")
        
        self.engine: Optional[pyttsx3.Engine] = None
        self._speech_queue: Queue = Queue()
        self._speech_thread: Optional[Thread] = None
        self._running = False
        self._lock = Lock()
        
        self._initialize_engine()
    
    def _initialize_engine(self) -> None:
        """Initialize the TTS engine with configured settings."""
        try:
            self.engine = pyttsx3.init()
            
            # Set speech rate
            self.engine.setProperty('rate', TTS_RATE)
            
            # Set volume
            self.engine.setProperty('volume', TTS_VOLUME)
            
            # Set voice (if available)
            voices = self.engine.getProperty('voices')
            if voices and TTS_VOICE_INDEX < len(voices):
                self.engine.setProperty('voice', voices[TTS_VOICE_INDEX].id)
            
            logger.info("TTS engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {e}")
            self.engine = None
    
    def speak(self, text: str, blocking: bool = True) -> bool:
        """
        Speak the given text.
        
        Args:
            text: Text to speak
            blocking: If True, wait for speech to complete
            
        Returns:
            True if speech was successful
        """
        if not self.engine:
            logger.error("TTS engine not initialized")
            print(f"[SPEAK]: {text}")  # Fallback to print
            return False
        
        if not text:
            return False
        
        logger.debug(f"Speaking: {text}")
        
        if blocking:
            return self._speak_blocking(text)
        else:
            return self._speak_async(text)
    
    def _speak_blocking(self, text: str) -> bool:
        """Speak text and wait for completion."""
        try:
            with self._lock:
                self.engine.say(text)
                self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"Error during speech: {e}")
            return False
    
    def _speak_async(self, text: str) -> bool:
        """Speak text asynchronously."""
        self._speech_queue.put(text)
        
        if not self._running:
            self._start_speech_thread()
        
        return True
    
    def _start_speech_thread(self) -> None:
        """Start the background speech thread."""
        if self._speech_thread and self._speech_thread.is_alive():
            return
        
        self._running = True
        self._speech_thread = Thread(target=self._speech_worker, daemon=True)
        self._speech_thread.start()
    
    def _speech_worker(self) -> None:
        """Worker thread for processing speech queue."""
        while self._running:
            try:
                text = self._speech_queue.get(timeout=1)
                self._speak_blocking(text)
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Speech worker error: {e}")
    
    def stop(self) -> None:
        """Stop any ongoing speech."""
        if self.engine:
            try:
                self.engine.stop()
            except Exception as e:
                logger.error(f"Error stopping speech: {e}")
    
    def shutdown(self) -> None:
        """Shutdown the speaker and clean up resources."""
        self._running = False
        self.stop()
        
        if self._speech_thread:
            self._speech_thread.join(timeout=2)
        
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
    
    def list_voices(self) -> list:
        """
        List available voices.
        
        Returns:
            List of voice information
        """
        if not self.engine:
            return []
        
        voices = self.engine.getProperty('voices')
        return [
            {
                "id": v.id,
                "name": v.name,
                "languages": v.languages,
                "gender": v.gender,
            }
            for v in voices
        ]
    
    def set_voice(self, index: int) -> bool:
        """
        Set the voice by index.
        
        Args:
            index: Voice index from list_voices()
            
        Returns:
            True if successful
        """
        if not self.engine:
            return False
        
        voices = self.engine.getProperty('voices')
        if 0 <= index < len(voices):
            self.engine.setProperty('voice', voices[index].id)
            return True
        return False
    
    def set_rate(self, rate: int) -> None:
        """Set speech rate (words per minute)."""
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)."""
        if self.engine:
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))


def test_speaker() -> bool:
    """
    Test if the speaker is working.
    
    Returns:
        True if speaker is functional
    """
    if not PYTTSX3_AVAILABLE:
        print("pyttsx3 library is not installed")
        return False
    
    try:
        engine = pyttsx3.init()
        engine.say("Text to speech is working")
        engine.runAndWait()
        print("Speaker is working!")
        return True
    except Exception as e:
        print(f"Speaker error: {e}")
        return False
'''

# ============================================================

COMMAND_PARSER_PY = '''"""
Command parser module for Jarvis Voice Assistant.
Handles intent detection and command routing.

This module is designed for easy replacement with LLM-based parsing.
The parse() method returns a structured Command object that can be
used by the executor regardless of how it was generated.
"""

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any, List

from config import COMMAND_KEYWORDS
from utils.helpers import clean_text, extract_after_keyword, get_current_time, get_current_date

logger = logging.getLogger(__name__)


class Intent(Enum):
    """Enumeration of supported intents."""
    OPEN_APP = "open_app"
    CLOSE_APP = "close_app"
    YOUTUBE_PLAY = "youtube_play"
    YOUTUBE_SEARCH = "youtube_search"
    SEARCH_WEB = "search_web"
    GET_TIME = "get_time"
    GET_DATE = "get_date"
    GREETING = "greeting"
    GOODBYE = "goodbye"
    UNKNOWN = "unknown"


@dataclass
class Command:
    """
    Structured command representation.
    
    Attributes:
        intent: The detected intent
        entities: Dictionary of extracted entities (e.g., app_name, query)
        raw_text: Original input text
        confidence: Confidence score (0.0 to 1.0)
    """
    intent: Intent
    entities: Dict[str, Any]
    raw_text: str
    confidence: float = 1.0


class CommandParser:
    """
    Rule-based command parser.
    
    This class can be replaced with an LLM-based parser by implementing
    the same interface (parse method returning Command objects).
    """
    
    def __init__(self):
        """Initialize the command parser."""
        self.keywords = COMMAND_KEYWORDS
        
        # Compile regex patterns for common commands
        self._patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for command matching."""
        return {
            # "open youtube and play X" or "open youtube and search X"
            "youtube_play": re.compile(
                r"(?:open\\s+)?youtube\\s+(?:and\\s+)?(?:play|watch|search)\\s+(.+)",
                re.IGNORECASE
            ),
            # "play X on youtube"
            "play_on_youtube": re.compile(
                r"(?:play|watch)\\s+(.+?)\\s+(?:on|in)\\s+youtube",
                re.IGNORECASE
            ),
            # "search youtube for X"
            "search_youtube": re.compile(
                r"(?:search|find)\\s+(?:on\\s+)?youtube\\s+(?:for\\s+)?(.+)",
                re.IGNORECASE
            ),
            # "open X"
            "open_app": re.compile(
                r"(?:open|launch|start|run)\\s+(.+)",
                re.IGNORECASE
            ),
            # "close X"
            "close_app": re.compile(
                r"(?:close|exit|quit|terminate)\\s+(.+)",
                re.IGNORECASE
            ),
            # Time query
            "get_time": re.compile(
                r"(?:what(?:\\'s|\\s+is)?\\s+the\\s+)?time",
                re.IGNORECASE
            ),
            # Date query
            "get_date": re.compile(
                r"(?:what(?:\\'s|\\s+is)?\\s+(?:the\\s+)?)?(?:date|today|day)",
                re.IGNORECASE
            ),
            # Greetings
            "greeting": re.compile(
                r"^(?:hello|hi|hey|good\\s+(?:morning|afternoon|evening))(?:\\s+jarvis)?$",
                re.IGNORECASE
            ),
            # Goodbye
            "goodbye": re.compile(
                r"(?:goodbye|bye|exit|quit|stop\\s+listening)",
                re.IGNORECASE
            ),
        }
    
    def parse(self, text: str) -> Command:
        """
        Parse input text and extract intent and entities.
        
        Args:
            text: Raw input text from speech recognition
            
        Returns:
            Command object with intent and entities
        """
        if not text:
            return Command(
                intent=Intent.UNKNOWN,
                entities={},
                raw_text="",
                confidence=0.0
            )
        
        # Clean and normalize text
        cleaned = clean_text(text)
        logger.debug(f"Parsing command: {cleaned}")
        
        # Try to match patterns in priority order
        
        # Check for greetings first
        if self._patterns["greeting"].match(cleaned):
            return Command(
                intent=Intent.GREETING,
                entities={},
                raw_text=text,
                confidence=0.95
            )
        
        # Check for goodbye
        if self._patterns["goodbye"].search(cleaned):
            return Command(
                intent=Intent.GOODBYE,
                entities={},
                raw_text=text,
                confidence=0.95
            )
        
        # Check for YouTube commands (higher priority than general open)
        youtube_match = self._patterns["youtube_play"].search(cleaned)
        if youtube_match:
            query = youtube_match.group(1).strip()
            return Command(
                intent=Intent.YOUTUBE_PLAY,
                entities={"query": query},
                raw_text=text,
                confidence=0.9
            )
        
        play_youtube_match = self._patterns["play_on_youtube"].search(cleaned)
        if play_youtube_match:
            query = play_youtube_match.group(1).strip()
            return Command(
                intent=Intent.YOUTUBE_PLAY,
                entities={"query": query},
                raw_text=text,
                confidence=0.9
            )
        
        search_youtube_match = self._patterns["search_youtube"].search(cleaned)
        if search_youtube_match:
            query = search_youtube_match.group(1).strip()
            return Command(
                intent=Intent.YOUTUBE_SEARCH,
                entities={"query": query},
                raw_text=text,
                confidence=0.85
            )
        
        # Check for time query
        if self._patterns["get_time"].search(cleaned):
            return Command(
                intent=Intent.GET_TIME,
                entities={},
                raw_text=text,
                confidence=0.9
            )
        
        # Check for date query
        if self._patterns["get_date"].search(cleaned):
            return Command(
                intent=Intent.GET_DATE,
                entities={},
                raw_text=text,
                confidence=0.9
            )
        
        # Check for open app command
        open_match = self._patterns["open_app"].search(cleaned)
        if open_match:
            app_name = open_match.group(1).strip()
            # Remove common filler words
            app_name = re.sub(r"^(?:the|a|an)\\s+", "", app_name)
            return Command(
                intent=Intent.OPEN_APP,
                entities={"app_name": app_name},
                raw_text=text,
                confidence=0.8
            )
        
        # Check for close app command
        close_match = self._patterns["close_app"].search(cleaned)
        if close_match:
            app_name = close_match.group(1).strip()
            app_name = re.sub(r"^(?:the|a|an)\\s+", "", app_name)
            return Command(
                intent=Intent.CLOSE_APP,
                entities={"app_name": app_name},
                raw_text=text,
                confidence=0.8
            )
        
        # Unknown command
        logger.debug(f"Could not parse command: {text}")
        return Command(
            intent=Intent.UNKNOWN,
            entities={"raw": text},
            raw_text=text,
            confidence=0.0
        )
    
    def get_supported_commands(self) -> List[str]:
        """
        Get list of supported command examples.
        
        Returns:
            List of example commands
        """
        return [
            "Open [application name]",
            "Close [application name]",
            "Open YouTube and play [search query]",
            "Play [video] on YouTube",
            "Search YouTube for [query]",
            "What time is it?",
            "What's the date?",
            "Hello / Hi",
            "Goodbye / Exit",
        ]


# ============================================================
# LLM Parser Interface (for future implementation)
# ============================================================

class LLMCommandParser:
    """
    Placeholder for LLM-based command parser.
    
    To use an LLM for parsing, implement this class with your
    preferred LLM (OpenAI, local model, etc.) and swap it in
    place of CommandParser in main.py.
    
    Example implementation:
    
    def parse(self, text: str) -> Command:
        # Call your LLM API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Extract intent and entities..."},
                {"role": "user", "content": text}
            ]
        )
        # Parse LLM response into Command object
        ...
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize LLM parser with API credentials."""
        self.api_key = api_key
        self.model = model or "gpt-3.5-turbo"
        # Initialize your LLM client here
    
    def parse(self, text: str) -> Command:
        """Parse using LLM - implement with your chosen LLM."""
        raise NotImplementedError("Implement with your LLM of choice")
'''

# ============================================================

MAIN_PY = '''"""
Jarvis Voice Assistant - Main Entry Point

A production-level desktop voice assistant that:
- Listens continuously for voice commands
- Understands natural language intent
- Executes system actions
- Provides voice feedback

Usage:
    python main.py              # Normal mode (wake word required)
    python main.py --no-wake    # Direct command mode (no wake word)
    python main.py --test       # Test microphone and speaker
"""

import sys
import signal
import logging
from typing import Optional

# Add parent directory to path for imports
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import WAKE_WORD
from utils.logger import setup_logging, get_logger
from utils.helpers import get_random_response, get_current_time, get_current_date
from listener import VoiceListener, test_microphone
from speaker import VoiceSpeaker, test_speaker
from command_parser import CommandParser, Intent, Command
from actions import open_application, close_application, YouTubeController


class JarvisAssistant:
    """
    Main Jarvis Voice Assistant class.
    Coordinates all components and handles the main loop.
    """
    
    def __init__(self, use_wake_word: bool = True):
        """
        Initialize the Jarvis assistant.
        
        Args:
            use_wake_word: Whether to require wake word before commands
        """
        self.logger = get_logger("jarvis.main")
        self.use_wake_word = use_wake_word
        
        # Initialize components
        self.listener: Optional[VoiceListener] = None
        self.speaker: Optional[VoiceSpeaker] = None
        self.parser: Optional[CommandParser] = None
        self.youtube: Optional[YouTubeController] = None
        
        # State
        self._running = False
        
        self._initialize_components()
    
    def _initialize_components(self) -> None:
        """Initialize all assistant components."""
        self.logger.info("Initializing Jarvis components...")
        
        try:
            self.listener = VoiceListener()
            self.logger.info("✓ Voice listener initialized")
        except Exception as e:
            self.logger.error(f"✗ Voice listener failed: {e}")
            raise
        
        try:
            self.speaker = VoiceSpeaker()
            self.logger.info("✓ Voice speaker initialized")
        except Exception as e:
            self.logger.error(f"✗ Voice speaker failed: {e}")
            raise
        
        self.parser = CommandParser()
        self.logger.info("✓ Command parser initialized")
        
        self.youtube = YouTubeController()
        self.logger.info("✓ YouTube controller initialized")
        
        self.logger.info("All components initialized successfully!")
    
    def speak(self, text: str) -> None:
        """Speak text using TTS."""
        if self.speaker:
            self.speaker.speak(text)
    
    def execute_command(self, command: Command) -> None:
        """
        Execute a parsed command.
        
        Args:
            command: Parsed Command object
        """
        intent = command.intent
        entities = command.entities
        
        self.logger.info(f"Executing: {intent.value} with {entities}")
        
        # Handle each intent type
        if intent == Intent.GREETING:
            self.speak(get_random_response("greeting"))
        
        elif intent == Intent.GOODBYE:
            self.speak(get_random_response("goodbye"))
            self._running = False
        
        elif intent == Intent.OPEN_APP:
            app_name = entities.get("app_name", "")
            self.speak(get_random_response("acknowledgment"))
            success, message = open_application(app_name)
            if not success:
                self.speak(message)
        
        elif intent == Intent.CLOSE_APP:
            app_name = entities.get("app_name", "")
            success, message = close_application(app_name)
            self.speak(message)
        
        elif intent == Intent.YOUTUBE_PLAY:
            query = entities.get("query", "")
            if query:
                self.speak(f"Playing {query} on YouTube")
                success, message = self.youtube.search_and_play(query)
                if not success:
                    self.speak(message)
            else:
                self.speak("What would you like me to play?")
        
        elif intent == Intent.YOUTUBE_SEARCH:
            query = entities.get("query", "")
            if query:
                self.speak(f"Searching YouTube for {query}")
                success, message = self.youtube.search_and_play(query)
                if not success:
                    self.speak(message)
        
        elif intent == Intent.GET_TIME:
            current_time = get_current_time()
            self.speak(f"The time is {current_time}")
        
        elif intent == Intent.GET_DATE:
            current_date = get_current_date()
            self.speak(f"Today is {current_date}")
        
        elif intent == Intent.UNKNOWN:
            self.speak(get_random_response("not_understood"))
        
        else:
            self.logger.warning(f"Unhandled intent: {intent}")
            self.speak("I'm not sure how to do that yet.")
    
    def process_input(self, text: str) -> None:
        """
        Process voice input text.
        
        Args:
            text: Recognized text from speech
        """
        if not text:
            return
        
        self.logger.info(f"Processing: {text}")
        
        # Parse the command
        command = self.parser.parse(text)
        
        # Execute the command
        self.execute_command(command)
    
    def run(self) -> None:
        """Run the main assistant loop."""
        self._running = True
        
        # Announce startup
        if self.use_wake_word:
            self.speak(f"Jarvis is ready. Say '{WAKE_WORD}' to activate.")
            self.logger.info(f"Listening for wake word: {WAKE_WORD}")
        else:
            self.speak("Jarvis is ready. How can I help you?")
            self.logger.info("Listening for commands (no wake word required)")
        
        # Main loop
        while self._running:
            try:
                if self.use_wake_word:
                    # Listen for wake word + command
                    text = self.listener.listen_with_wake_word()
                else:
                    # Listen directly for commands
                    text = self.listener.listen_once()
                
                if text:
                    self.process_input(text)
                    
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.speak("I encountered an error. Let me try again.")
        
        self.shutdown()
    
    def shutdown(self) -> None:
        """Shutdown the assistant and clean up resources."""
        self.logger.info("Shutting down Jarvis...")
        
        self._running = False
        
        if self.youtube:
            self.youtube.close()
        
        if self.speaker:
            self.speaker.shutdown()
        
        if self.listener:
            self.listener.stop_background_listening()
        
        self.logger.info("Jarvis shutdown complete.")


def run_tests() -> bool:
    """Run component tests."""
    print("=" * 50)
    print("  JARVIS COMPONENT TESTS")
    print("=" * 50)
    
    print("\\n[1/2] Testing microphone...")
    mic_ok = test_microphone()
    
    print("\\n[2/2] Testing speaker...")
    speaker_ok = test_speaker()
    
    print("\\n" + "=" * 50)
    if mic_ok and speaker_ok:
        print("✓ All tests passed!")
        return True
    else:
        print("✗ Some tests failed. Check your hardware.")
        return False


def main():
    """Main entry point."""
    # Setup logging
    setup_logging()
    logger = get_logger("jarvis")
    
    # Parse command line arguments
    use_wake_word = True
    
    if "--test" in sys.argv:
        success = run_tests()
        sys.exit(0 if success else 1)
    
    if "--no-wake" in sys.argv:
        use_wake_word = False
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        sys.exit(0)
    
    # Handle graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Received shutdown signal")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the assistant
    try:
        print("=" * 50)
        print("  JARVIS VOICE ASSISTANT")
        print("=" * 50)
        
        assistant = JarvisAssistant(use_wake_word=use_wake_word)
        assistant.run()
        
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print(f"\\nError: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
'''

# ============================================================
# GENERATE FILES
# ============================================================

def create_directories():
    """Create the project directory structure."""
    directories = [
        JARVIS_PATH,
        os.path.join(JARVIS_PATH, "actions"),
        os.path.join(JARVIS_PATH, "utils"),
        os.path.join(JARVIS_PATH, "logs"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def write_file(path: str, content: str):
    """Write content to a file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✓ Created file: {path}")

def main():
    print("=" * 60)
    print("  JARVIS VOICE ASSISTANT - PROJECT GENERATOR")
    print("=" * 60)
    
    print("\n📁 Creating directories...")
    create_directories()
    
    print("\n📝 Creating files...")
    
    # Config
    write_file(os.path.join(JARVIS_PATH, "config.py"), CONFIG_PY)
    
    # Utils
    write_file(os.path.join(JARVIS_PATH, "utils", "__init__.py"), UTILS_INIT_PY)
    write_file(os.path.join(JARVIS_PATH, "utils", "logger.py"), UTILS_LOGGER_PY)
    write_file(os.path.join(JARVIS_PATH, "utils", "helpers.py"), UTILS_HELPERS_PY)
    
    # Actions
    write_file(os.path.join(JARVIS_PATH, "actions", "__init__.py"), ACTIONS_INIT_PY)
    write_file(os.path.join(JARVIS_PATH, "actions", "open_apps.py"), ACTIONS_OPEN_APPS_PY)
    write_file(os.path.join(JARVIS_PATH, "actions", "youtube.py"), ACTIONS_YOUTUBE_PY)
    
    # Core modules
    write_file(os.path.join(JARVIS_PATH, "listener.py"), LISTENER_PY)
    write_file(os.path.join(JARVIS_PATH, "speaker.py"), SPEAKER_PY)
    write_file(os.path.join(JARVIS_PATH, "command_parser.py"), COMMAND_PARSER_PY)
    write_file(os.path.join(JARVIS_PATH, "main.py"), MAIN_PY)
    
    # Create __init__.py for jarvis package
    write_file(os.path.join(JARVIS_PATH, "__init__.py"), '"""Jarvis Voice Assistant Package."""\n')
    
    print("\n" + "=" * 60)
    print("✅ PROJECT GENERATION COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Install dependencies:")
    print("     pip install -r requirements.txt")
    print("\n  2. Run the assistant:")
    print("     cd jarvis")
    print("     python main.py")
    print("\n  3. Test components:")
    print("     python main.py --test")
    print("\n  4. Run without wake word:")
    print("     python main.py --no-wake")
    print("=" * 60)

if __name__ == "__main__":
    main()
