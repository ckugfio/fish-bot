# 🎣 Fishing Bot v2.1

> **Automated fishing bot for PC games using real-time screen color detection**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgray.svg)]()

[Spanish Version](README_ES.md)

---

## ✨ Features

- **Customizable Hotkeys** — Configure keys for casting, reeling, and toggling the bot
- **Screen Color Detection** — Automatically capture the fishing indicator color from screen
- **Region Selection** — Define the screen area where the fishing icon appears
- **Adjustable Color Tolerance** — Control how precise the color detection should be
- **Multilingual Interface** — Available in English and Spanish
- **Quick Toggle Key** — Enable/disable the bot instantly (default: F9)
- **Persistent Configuration** — Settings are saved between sessions

## 📋 Requirements

- **OS**: Windows (uses native Windows APIs for key input)
- **Python**: 3.8 or higher

## 🚀 Quick Start

### 1. Install

```bash
# Clone the repository
git clone https://github.com/yourusername/fishing-bot.git
cd fishing-bot

# Install dependencies
pip install -r requirements.txt
```

### 2. Run

```bash
python fishing_bot.py
```

### 3. Or Build Executable

```bash
pyinstaller BotDePesca.spec
```

Executable will be in the `dist/` folder.

## ⚙️ Configuration

### Step 1: Configure Hotkeys
Click on each key button to change it:
- **CAST** — Key to cast the fishing line
- **REEL** — Key to reel in the line
- **TOGGLE** — Key to enable/disable the bot

### Step 2: Select Screen Region
1. Click **"Select Region"**
2. Drag to draw a box around where the fishing icon appears in-game

### Step 3: Select Target Color
- **Palette** — Manually choose a color
- **Screen** — Capture color directly from the game

### Step 4: Adjust Tolerance
- **Increase** if detection is not working (more lenient)
- **Decrease** for more precise detection (stricter)

### Step 5: Start Bot
- Click **"START BOT"** or press your toggle key (default: F9)

## 🔧 How It Works

The bot operates in a continuous loop:

1. **Casts** the fishing line (presses configured key)
2. **Monitors** the selected screen region for the target color
3. **Detects** the color (fish bite) and automatically reels in
4. **Waits** and repeats the cycle

## 📝 Example Configuration

```json
{
  "cast_key": "1",
  "reel_key": "2",
  "toggle_key": "f9",
  "region": [100, 100, 200, 200],
  "color": [255, 200, 100],
  "tolerance": 20,
  "language": "en"
}
```

Copy `config.json.example` to `config.json` and customize.

## 📁 Project Files

| File | Description |
|------|-------------|
| `fishing_bot.py` | Main source code |
| `requirements.txt` | Python dependencies |
| `BotDePesca.spec` | PyInstaller configuration |
| `build_exe.bat` | Build script (English) |
| `crear_exe.bat` | Build script (Spanish) |
| `config.json.example` | Example configuration |

## 💡 Tips

- Uses Windows `SendInput` API for better game compatibility
- Game doesn't need to be constantly focused
- Bot can be minimized while running
- If antivirus blocks the .exe, add an exclusion for the folder

## ⚠️ Disclaimer

**Use at your own risk.** Some games may consider bot usage a violation of their Terms of Service. Always check the game rules before using.

---

**Version**: 2.1
