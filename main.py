import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import time
from pynput.keyboard import Controller as KeyboardController, Key
from Quartz.CoreGraphics import (
    CGEventCreate, CGEventGetLocation,
    CGEventCreateMouseEvent, CGEventPost,
    kCGHIDEventTap,
    kCGEventLeftMouseDown, kCGEventLeftMouseUp,
    kCGMouseButtonLeft
)

run = False
clicks_nums = 0
keyboard = KeyboardController()

def printTerm(message):
    output.config(state=tk.NORMAL)
    output.insert(tk.END, message + "\n")
    output.see(tk.END)
    output.config(state=tk.DISABLED)

def on_select():
    start_button.config(state=tk.NORMAL)

def left_mouse_click():
    event = CGEventCreate(None)
    pos = CGEventGetLocation(event)

    event_down = CGEventCreateMouseEvent(None, kCGEventLeftMouseDown, pos, kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, event_down)

    event_up = CGEventCreateMouseEvent(None, kCGEventLeftMouseUp, pos, kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, event_up)

def click_loop():
    global run, clicks_nums
    choice = v.get()
    try:
        cps = int(cps_entry.get())
        if cps <= 0:
            raise ValueError
    except:
        printTerm("Invalid CPS value, using default 20")
        cps = 20

    delay = 1.0 / cps
    clicks_nums = 0
    printTerm("Starting clicking...")

    while run:
        if choice == 1:
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        else:
            left_mouse_click()

        clicks_nums += 1

        if clicks_nums % 10 == 0:
            key_name = "Spacebar" if choice == 1 else "Left Mouse"
            printTerm(f'Clicked {key_name} {clicks_nums} times.')

        time.sleep(delay)

    printTerm("Stopped clicking.")

def start_clicking():
    global run
    if v.get() == 0:
        printTerm("Please select a key to click first.")
        return

    run = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    thread = Thread(target=click_loop, daemon=True)
    thread.start()

def stop_clicking():
    global run
    run = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

root = tk.Tk()
root.title("MacOS Auto-Clicker")
root.geometry('305x380+555+165')

frame = tk.Frame(root, relief=tk.RIDGE)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Clicks per second (CPS):").pack(pady=5)
cps_entry = tk.Entry(frame)
cps_entry.pack()
cps_entry.insert(0, "20")

v = tk.IntVar()
v.set(0)
tk.Label(frame, text='Key must be selected!').pack(anchor='e')
tk.Radiobutton(frame, text='Spacebar', variable=v, value=1, command=on_select).pack(anchor='e')
tk.Radiobutton(frame, text="Left Mouse", variable=v, value=2, command=on_select).pack(anchor='e')

start_button = tk.Button(frame, text="Start Clicking", command=start_clicking, state=tk.DISABLED)
start_button.pack(pady=5)

stop_button = tk.Button(frame, text="Stop Clicking", command=stop_clicking, state=tk.DISABLED)
stop_button.pack(pady=5)

output = scrolledtext.ScrolledText(frame, width=40, height=15, state=tk.DISABLED)
output.pack(pady=10)

root.mainloop()
