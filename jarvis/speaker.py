"""
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
