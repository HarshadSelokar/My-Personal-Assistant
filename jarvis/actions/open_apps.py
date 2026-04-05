"""
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
