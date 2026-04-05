"""
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
