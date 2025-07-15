import tkinter as tk
import json
import os
import time
import webbrowser

statsGUI, terminalGUI, codeGUI, logGUI = None,None, None, None
data = {}

def StatsPage(root, total_clicks):
    global statsGUI, data
    if statsGUI is None or not statsGUI.winfo_exists():
        statsGUI = tk.Toplevel(root)
        statsGUI.title('Stats')
        statsGUI.geometry('305x380+10+10')

        total_clicks_label = tk.Label(statsGUI, text=f'Current Session Total Clicks: {total_clicks}', font=('Arial', 14))
        total_clicks_label.pack(pady=10)

        all_time_clicks = tk.Label(statsGUI, text=f'All Time Total Clicks: {data.get('total_clicks')}', font=('Arial', 14))
        all_time_clicks.pack(pady=10)

        last_known_cps = tk.Label(statsGUI, text=f'Last known cps was {data.get('last_cps')}', font=('Arial', 14))
        last_known_cps.pack(pady=10)
        # Update global data dict
        data = {
            'total_clicks': 0,
            'last_cps': data.get('last_cps', 20),
            'mode': data.get('mode', 'left_mouse')
        }
        
        

        # Example extra widget
        details = tk.Text(statsGUI, width=35, height=15)
        details.insert(tk.END, "More detailed stats can go here...\n")
        details.config(state=tk.DISABLED)
        details.pack(pady=10)
    else:
        statsGUI.lift()

def TerminalPage(root):
    global terminalGUI
    if terminalGUI is None or not terminalGUI.winfo_exists():
        terminalGUI = tk.Toplevel(root)
        terminalGUI.title('Expanded Terminal')
        terminalGUI.geometry('305x380+555+165')
    else:
        terminalGUI.lift()

def CodeViewer(root):
    global codeGUI
    if codeGUI is None or not codeGUI.winfo_exists():
        codeGUI = tk.Toplevel(root)
        codeGUI.title('Code Viewer')
        codeGUI.geometry('305x380+555+165')
        link = tk.Label(codeGUI, text='MacOS Auto-Clicker Code', fg='blue', cursor='hand2')
        link.pack(pady=20)
        link.bind("<Button-1>", lambda e: webbrowser.open_new('https://github.com/v1pershot/MacOS-Autoclicker'))
    else:
        codeGUI.lift()

def LogViewer(root):
    global logGUI
    if logGUI is None or not logGUI.winfo_exists():
        logGUI = tk.Toplevel(root)
        logGUI.title('Saved Data')
        logGUI.geometry('305x380+555+165')
        dataArea = tk.Label(logGUI, text=data, width='340', font=('Arial', 14))
        dataArea.pack()

def update(w_menu, root, total_clicks, last_cps):  # w_menu means which menu
    global statsGUI
    if statsGUI is not None and statsGUI.winfo_exists():
        statsGUI.destroy()
        StatsPage(root, total_clicks)
    dataSave(total_clicks, last_cps)
    #StatsPage(root, total_clicks)

def onClose(total_clicks, last_cps):
    dataSave(total_clicks, last_cps)

def safeClose(root, total_clicks, last_cps):
    dataSave(total_clicks, last_cps)
    root.destroy()

def dataSave(total_clicks, last_cps):
    global data
    lcps = last_cps
    
    data_clicks = int(total_clicks) + int(data.get('total_clicks'))
    #print(f'Data Clicks: {data_clicks}')
    data['total_clicks'] = data_clicks
    data['last_cps'] = lcps
    time.sleep(1)
    #print(data)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def dataOpen():
    global data
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    #print(f"Loaded data: {data.get('total_clicks')}")
