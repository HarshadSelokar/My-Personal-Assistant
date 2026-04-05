"""
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
    
    print("\n[1/2] Testing microphone...")
    mic_ok = test_microphone()
    
    print("\n[2/2] Testing speaker...")
    speaker_ok = test_speaker()
    
    print("\n" + "=" * 50)
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
        print(f"\nError: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
