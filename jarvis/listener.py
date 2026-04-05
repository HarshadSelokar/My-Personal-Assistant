"""
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
