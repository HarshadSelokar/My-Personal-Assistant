"""
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
                r"(?:open\s+)?youtube\s+(?:and\s+)?(?:play|watch|search)\s+(.+)",
                re.IGNORECASE
            ),
            # "play X on youtube"
            "play_on_youtube": re.compile(
                r"(?:play|watch)\s+(.+?)\s+(?:on|in)\s+youtube",
                re.IGNORECASE
            ),
            # "search youtube for X"
            "search_youtube": re.compile(
                r"(?:search|find)\s+(?:on\s+)?youtube\s+(?:for\s+)?(.+)",
                re.IGNORECASE
            ),
            # "open X"
            "open_app": re.compile(
                r"(?:open|launch|start|run)\s+(.+)",
                re.IGNORECASE
            ),
            # "close X"
            "close_app": re.compile(
                r"(?:close|exit|quit|terminate)\s+(.+)",
                re.IGNORECASE
            ),
            # Time query
            "get_time": re.compile(
                r"(?:what(?:\'s|\s+is)?\s+the\s+)?time",
                re.IGNORECASE
            ),
            # Date query
            "get_date": re.compile(
                r"(?:what(?:\'s|\s+is)?\s+(?:the\s+)?)?(?:date|today|day)",
                re.IGNORECASE
            ),
            # Greetings
            "greeting": re.compile(
                r"^(?:hello|hi|hey|good\s+(?:morning|afternoon|evening))(?:\s+jarvis)?$",
                re.IGNORECASE
            ),
            # Goodbye
            "goodbye": re.compile(
                r"(?:goodbye|bye|exit|quit|stop\s+listening)",
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
            app_name = re.sub(r"^(?:the|a|an)\s+", "", app_name)
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
            app_name = re.sub(r"^(?:the|a|an)\s+", "", app_name)
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
