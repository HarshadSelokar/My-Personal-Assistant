# Jarvis Voice Assistant
# Run setup.py first, then cd jarvis && python main.py

## Quick Start

```bash
# Step 1: Setup (creates directories and optionally installs dependencies)
python setup.py --all

# Step 2: Run
cd jarvis
python main.py
```

## Manual Installation

```bash
pip install SpeechRecognition pyttsx3 selenium webdriver-manager pyautogui pyaudio
```

## Project Structure

```
jarvis/
├── main.py              # Entry point
├── listener.py          # Voice input handling
├── speaker.py           # Text-to-speech output
├── command_parser.py    # Intent detection and routing
├── config.py            # All configuration settings
├── actions/
│   ├── __init__.py
│   ├── open_apps.py     # Application launcher
│   └── youtube.py       # YouTube automation
├── utils/
│   ├── __init__.py
│   ├── logger.py        # Logging utilities
│   └── helpers.py       # Common helpers
└── logs/
    └── jarvis.log       # Application logs
```

## Commands

- "Jarvis" - Wake word
- "Open Chrome" / "Open Notepad" / "Open Calculator"
- "Open YouTube and play [search term]"
- "Search YouTube for [query]"
- "What time is it?"
- "What's the date?"
- "Goodbye" / "Exit"

## Configuration

Edit `jarvis/config.py` to customize:
- Chrome/browser paths
- Wake word
- Speech settings
- Timeout values
