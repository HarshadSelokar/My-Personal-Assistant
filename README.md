# Jarvis Voice Assistant

A production-level desktop voice assistant that runs locally on Windows.

## Features

- **Wake Word Detection**: Say "Jarvis" to activate
- **Voice Recognition**: Continuous microphone listening
- **Natural Language**: Intent-based command parsing
- **Voice Feedback**: Text-to-speech responses
- **Browser Automation**: YouTube search and playback
- **App Launcher**: Open any Windows application

## Quick Start

```bash
# Step 1: Generate project structure
python generate_project.py

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Run the assistant
cd jarvis
python main.py
```

## Manual Installation

If PyAudio fails to install on Windows, download the wheel from:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

Then: `pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl`

## Project Structure

```
jarvis/
├── main.py              # Entry point
├── config.py            # All configuration settings
├── listener.py          # Voice input (speech-to-text)
├── speaker.py           # Voice output (text-to-speech)
├── command_parser.py    # Intent detection & routing
├── actions/
│   ├── open_apps.py     # Application launcher
│   └── youtube.py       # YouTube automation
├── utils/
│   ├── logger.py        # Logging utilities
│   └── helpers.py       # Common helpers
└── logs/
    └── jarvis.log       # Application logs
```

## Commands

### Application Control
- "Open Chrome"
- "Open Notepad"
- "Open Calculator"
- "Close Chrome"

### YouTube
- "Open YouTube and play Gate Smashers AVL tree"
- "Play Lofi music on YouTube"
- "Search YouTube for Python tutorials"

### System Info
- "What time is it?"
- "What's the date?"

### Assistant Control
- "Hello" / "Hi" - Greeting
- "Goodbye" / "Exit" - Stop assistant

## Usage Modes

```bash
# Normal mode (wake word "Jarvis" required)
python main.py

# Direct mode (no wake word needed)
python main.py --no-wake

# Test microphone and speaker
python main.py --test
```

## Configuration

Edit `jarvis/config.py` to customize:

```python
# Wake word
WAKE_WORD = "jarvis"

# Chrome path (update if needed)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Speech settings
TTS_RATE = 175      # Speech speed
TTS_VOLUME = 1.0    # Volume (0.0-1.0)
LISTEN_TIMEOUT = 5  # Seconds to wait for speech

# Add custom applications
APPLICATIONS = {
    "myapp": r"C:\Path\To\MyApp.exe",
    ...
}
```

## Architecture (For Developers)

### Modular Design

Each component is independent and replaceable:

1. **Listener** (`listener.py`): Handles microphone input, speech-to-text
2. **Speaker** (`speaker.py`): Handles text-to-speech output
3. **Parser** (`command_parser.py`): Converts text to structured commands
4. **Actions** (`actions/`): Execute specific tasks

### Adding New Commands

1. Add intent to `command_parser.py`:
```python
class Intent(Enum):
    MY_NEW_INTENT = "my_new_intent"
```

2. Add pattern matching in `CommandParser._compile_patterns()`

3. Add handler in `main.py` `execute_command()`

### Replacing with LLM Parser

The `CommandParser` returns structured `Command` objects. To use an LLM:

```python
# In main.py, replace:
self.parser = CommandParser()

# With:
from command_parser import LLMCommandParser
self.parser = LLMCommandParser(api_key="your-key")
```

### Adding GUI

The `JarvisAssistant` class can be instantiated from any GUI framework:

```python
from jarvis.main import JarvisAssistant

assistant = JarvisAssistant(use_wake_word=False)
# Connect to your GUI events
```

## Troubleshooting

### Microphone not working
1. Run `python main.py --test`
2. Check Windows microphone permissions
3. Ensure PyAudio is installed correctly

### Speech not recognized
- Adjust `ENERGY_THRESHOLD` in config.py
- Speak clearly and closer to microphone

### Chrome not opening
- Verify `CHROME_PATH` in config.py matches your installation

### YouTube videos not playing
- Ensure Chrome is installed
- WebDriver is auto-managed, but check internet connection

## License

MIT License
