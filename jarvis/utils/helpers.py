"""
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
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"[^\w\s\'-]", '', text)
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
