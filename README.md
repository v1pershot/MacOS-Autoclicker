# MacOS Auto-Clicker v1.1.1

A simple auto-clicker GUI application for MacOS built with Python and Tkinter.  
It allows you to automatically click either the **spacebar** key or the **left mouse button** at a customizable clicks-per-second (CPS) rate.

---

## Features

- Select between clicking the **Spacebar** or the **Left Mouse Button**.
- Set the number of clicks per second (CPS).
- Delay between button clicked and clicking starting v1.1.1
- Start and stop the auto-clicking with buttons.
- Working Force Quit (CTRL+Q) v1.1.1
- Logs click activity and status messages in a scrolling text output.
- Runs clicking in a background thread to keep the GUI responsive.
- Uses native macOS Quartz APIs for precise mouse clicks.
- Stats are saved even when you close the program. v1.1.1
- You can view the code and data logs inside the autoclicker.

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

## Future Updates

For update v1.1 I plan to add a menubar to the top and a way to track user stats localy through a text file. Windows support will not be added as the Auto-Clicker uses MacOS dependant libraies. Major features I plan to add is more keys for clicking and stoping, In-app cps tester, and a way to systematically tell the mouse where to be for more advanced controll over position and timing. Minor updates include: GUI fixes and quality updates, better timing of cps, and less lag by reducing the amount of printed statements.

## Troubleshooting/Bugfixes

Make a pull request and explain whats wrong.

