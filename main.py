import tkinter as tk
import sys
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
import os
import menus as men

print("Running File:", os.path.abspath(__file__))
run = False
clicks_nums = 0
counter = 0
keyboard = KeyboardController()
last_cps = 0


# All Functions
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
    global run, clicks_nums, counter
    choice = v.get()
    try:
        cps = int(cps_entry.get())
        if cps <= 0:
            print('value error')
            raise ValueError
    except:
        printTerm("Invalid CPS value")
        sys.exit(1)

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
        counter += 1

        if clicks_nums % 10000 == 0:
            key_name = "Spacebar" if choice == 1 else "Left Mouse"
            printTerm(f'Clicked {key_name} {clicks_nums} times.')

        time.sleep(delay)

    printTerm("Stopped clicking.")
    printTerm(f'Clicked {counter} times')

def start_clicking():
    global run
    global last_cps
    if v.get() == 0:
        printTerm("Please select a key to click first.")
        return

    run = True
    delay = int(start_delay_button.get())
    time.sleep(delay)
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    last_cps = int(cps_entry.get())

    thread = Thread(target=click_loop, daemon=True)
    thread.start()
    

def stop_clicking():
    global run
    run = False
    men.update(run, root, counter, last_cps)
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def multiple_commands():
    thread2 = Thread(target=stop_clicking, daemon=True)
    thread2.start()
    root.destroy()


men.dataOpen()
root = tk.Tk()
root.title("MacOS Auto-Clicker")
root.geometry('305x380+555+165')

#Topbar menus

#menubar creation
menubar = tk.Menu(root)

#Main menu setup
main_menu = tk.Menu(menubar, tearoff=0)
main_menu.add_command(label='Stats', command=lambda: men.StatsPage(root, counter))
main_menu.add_command(label='Expanded Terminal', command=lambda: men.TerminalPage(root))
main_menu.add_command(label='Quick Kill', command=multiple_commands, accelerator='Ctrl+Q')
menubar.add_cascade(label='Main', menu=main_menu)

view_menu = tk.Menu(menubar, tearoff=0)
view_menu.add_command(label='View Code', command=lambda: men.CodeViewer(root))
view_menu.add_command(label="View Saved Data", command=lambda: men.LogViewer(root))

menubar.add_cascade(label='View', menu=view_menu)
root.config(menu=menubar)
root.bind_all('<Control-q>', lambda e: men.safeClose(root, counter, last_cps))


frame = tk.Frame(root, relief=tk.RIDGE)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Clicks per second (CPS):").pack(pady=5)
cps_entry = tk.Entry(frame)
cps_entry.pack()
cps_entry.insert(0, f"{men.data.get('last_cps', 20)}")

v = tk.IntVar()
v.set(0)
tk.Label(frame, text='Key must be selected!').pack(anchor='e')
tk.Radiobutton(frame, text='Spacebar', variable=v, value=1, command=on_select).pack(anchor='e')
tk.Radiobutton(frame, text="Left Mouse", variable=v, value=2, command=on_select).pack(anchor='e')

tk.Label(frame, text='Start delay (Seconds)').pack(anchor='e')

start_delay_button = tk.Entry(frame, width=2)
start_delay_button.pack(padx='52', anchor='e')
start_delay_button.insert(0, '1')


start_button = tk.Button(frame, text="Start Clicking", command=start_clicking, state=tk.DISABLED)
start_button.pack(pady=5)

stop_button = tk.Button(frame, text="Stop Clicking(Ctrl+Q)", command=stop_clicking, state=tk.DISABLED)
stop_button.pack(pady=5)

output = scrolledtext.ScrolledText(frame, width=40, height=15, state=tk.DISABLED)
output.pack(pady=10)

#attaches the menubar to the root window


root.protocol('WM_DELETE_ WINDOW',lambda: men.onClose(counter, last_cps))
root.mainloop()
