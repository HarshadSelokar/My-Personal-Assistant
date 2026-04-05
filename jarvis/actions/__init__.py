"""
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
