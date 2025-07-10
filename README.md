# MacOS Auto-Clicker v1.0

A simple auto-clicker GUI application for MacOS built with Python and Tkinter.  
It allows you to automatically click either the **spacebar** key or the **left mouse button** at a customizable clicks-per-second (CPS) rate.

---

## Features

- Select between clicking the **Spacebar** or the **Left Mouse Button**.
- Set the number of clicks per second (CPS).
- Start and stop the auto-clicking with buttons.
- Logs click activity and status messages in a scrolling text output.
- Runs clicking in a background thread to keep the GUI responsive.
- Uses native macOS Quartz APIs for precise mouse clicks.

---

## Requirements

- Python 3.12+  
- `pynput` library  
- macOS platform (uses Quartz CoreGraphics API)

---

## Installation

1. Install Python 3.12 or newer from [python.org](https://www.python.org/downloads/mac-osx/).

2. Install dependencies using pip:
   ```bash
   pip install pynput
3. Type this in a terminal python3 main.py
