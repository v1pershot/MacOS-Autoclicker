import tkinter as tk
import json
import os
import time
import webbrowser

statsGUI, terminalGUI, codeGUI, logGUI = None,None, None, None
data = {}
choice = 0
vm = 0

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
            'mode': data.get('mode', choice),
            'interval': data.get('interval', vm)
        }
        
        

        # Example extra widget
        details = tk.Text(statsGUI, width=35, height=15)
        details.insert(tk.END, "More detailed stats can go here...\n")
        details.config(state=tk.DISABLED)
        details.pack(pady=10)
    else:
        statsGUI.lift()

def SettingsPage(root):
    global terminalGUI, vm

    def on_gui_close():
        solveInterval('close2')
        terminalGUI.destroy()
    if terminalGUI is None or not terminalGUI.winfo_exists():
        terminalGUI = tk.Toplevel(root)
        terminalGUI.title('Settings')
        terminalGUI.geometry('305x380+555+165')
        terminalGUI.protocol("WM_DELETE_WINDOW", on_gui_close)

        tk.Label(terminalGUI, text='Print intervals', font=("TkDefaultFont", 12, "bold")).pack(anchor='w')
        tk.Label(terminalGUI, text="The smaller the number, more laggier it gets,\n but you won't see progress as quick\n(Default is 1k)").pack(anchor='w')
        vm = tk.IntVar()
        vm_value = solveInterval('open')
        vm.set(vm_value)
        tk.Radiobutton(terminalGUI, text='10', variable=vm, value=1,).pack(anchor='w')
        tk.Radiobutton(terminalGUI, text="100", variable=vm, value=2).pack(anchor='w')
        tk.Radiobutton(terminalGUI, text="1k", variable=vm, value=3).pack(anchor='w')
        tk.Radiobutton(terminalGUI, text="10k", variable=vm, value=4).pack(anchor='w')
        tk.Radiobutton(terminalGUI, text="100k", variable=vm, value=5).pack(anchor='w')
        tk.Radiobutton(terminalGUI, text="1m", variable=vm, value=6).pack(anchor='w')

        tk.Button(terminalGUI, text='Save', command=lambda: solveInterval('close2')).pack(pady='10')

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
    global logGUI, data
    if logGUI is None or not logGUI.winfo_exists():
        logGUI = tk.Toplevel(root)
        logGUI.title('Saved Data')
        logGUI.geometry('305x380+555+165')
        data_text = "\n".join(f"{key}: {value}" for key, value in data.items())
        dataArea = tk.Label(logGUI, text=data_text, width='340', font=('Arial', 14))
        dataArea.pack()

def update(w_menu, root, total_clicks, last_cps):  # w_menu means which menu
    global statsGUI
    if statsGUI is not None and statsGUI.winfo_exists():
        dataSave(total_clicks, last_cps)
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
    func_return = solveInterval('close')
    
    data_clicks = int(total_clicks) + int(data.get('total_clicks'))
    #print(f'Data Clicks: {data_clicks}')
    data['total_clicks'] = data_clicks
    data['last_cps'] = lcps
    data['mode'] = choice
    data['interval'] = func_return
    
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

def dataPipe(c_c_choice):
    global choice
    choice = c_c_choice

def solveInterval(mode):
    global vm, data

    # Ensure vm is always an IntVar
    if not isinstance(vm, tk.IntVar):
        vm = tk.IntVar(value=3)  # default "1k"

    mapping = {
        1: 10,
        2: 100,
        3: 1000,
        4: 10000,
        5: 100000,
        6: 1000000
    }

    if mode == 'close':
        return mapping.get(vm.get(), 1000)  # fallback 1k if not set

    elif mode == 'close2':
        interval2 = mapping.get(vm.get(), 1000)
        data['interval'] = interval2
        return interval2

    elif mode == 'open':
        reverse_map = {v: k for k, v in mapping.items()}
        return reverse_map.get(data.get('interval', 1000), 3)
