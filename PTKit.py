import tkinter as tk
from tkinter import Toplevel, ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import sqlite3
import subprocess
import os
import threading

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)

def vuln_Start():
    fqd = combo.get()
    if not fqd:
        messagebox.showwarning("Warning", "Please select an FQD.")
        return

    term_host = tk.Frame(vuln_frame)
    term_host.grid(row=0, rowspan=len(vuln_tools) + 1, column=1, sticky='nsew')
    termf = tk.Frame(term_host, height=1024, width=760)
    termf.pack(fill=tk.BOTH, expand=tk.YES)
    wid = termf.winfo_id()
    
    # Run command in the newly opened xterm
    if vuln_variables['Smuggler'].get() == 1:
        script_path_smuggler = os.path.join(script_directory, 'tools', 'smuggler', 'smuggler.py')
        command = f'python3 {script_path_smuggler} -u {fqd} && bash'
        os.system(f'xterm -into {wid} -geometry 600x480 -sb -e "{command}" &')
    else:
        os.system(f'xterm -into {wid} -geometry 600x480 -sb -e "bash" &')

def add_fqd():
    new_fqd = simpledialog.askstring("Input", "Enter new FQD:")
    if new_fqd:
        conn = sqlite3.connect("fqd_data.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO fqds (name) VALUES (?)", (new_fqd,))
        conn.commit()
        conn.close()
        combo['values'] = get_fqds_from_db()
        combo.current(0)
    else:
        messagebox.showwarning("Warning", "Please enter an FQD.")

def delete_fqd():
    selected_fqd = combo.get()
    if selected_fqd:
        conn = sqlite3.connect("fqd_data.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM fqds WHERE name=?", (selected_fqd,))
        conn.commit()
        conn.close()
        combo['values'] = get_fqds_from_db()
        combo.set('')
    else:
        messagebox.showwarning("Warning", "Please select an FQD to delete.")

def get_fqds_from_db():
    conn = sqlite3.connect("fqd_data.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM fqds")
    fqds = [row[0] for row in cur.fetchall()]
    conn.close()
    return fqds

# Initialize root window
root = tk.Tk()
root.title("P.T. Kit")

# Create background label here
image = Image.open("hacker_background.jpg")
bg_image = ImageTk.PhotoImage(image)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# Create FQD combo box and buttons here
frame_fqd = tk.Frame(root)
frame_fqd.pack(padx=20, pady=20)
combo = ttk.Combobox(frame_fqd, values=get_fqds_from_db())
combo.grid(row=0, column=0)
btn_add = tk.Button(frame_fqd, text="Add", command=add_fqd)
btn_add.grid(row=0, column=1)
btn_del = tk.Button(frame_fqd, text="Delete", command=delete_fqd)
btn_del.grid(row=0, column=2)

notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

recon_frame = tk.Frame(notebook)
vuln_frame = tk.Frame(notebook)
termf = tk.Frame(vuln_frame, height=400, width=500)

notebook.add(recon_frame, text='Recon')
notebook.add(vuln_frame, text='Vulnerabilities')

recon_tools = ['Sublist3r', 'Amass', 'SubFinder', 'Knockpy', 'Censys', 'Crt.sh']
recon_variables = {}
for index, tool in enumerate(recon_tools):
    recon_variables[tool] = tk.IntVar(value=1)
    chk = tk.Checkbutton(recon_frame, text=tool, variable=recon_variables[tool])
    chk.grid(row=index, column=0)

vuln_tools = ['Nuclei', 'Smuggler']
vuln_variables = {}
for index, tool in enumerate(vuln_tools):
    vuln_variables[tool] = tk.IntVar(value=1)
    chk = tk.Checkbutton(vuln_frame, text=tool, variable=vuln_variables[tool])
    chk.grid(row=index, column=0)

vuln_start_button = tk.Button(vuln_frame, text="Start", command=vuln_Start)
vuln_start_button.grid(row=len(vuln_tools), column=0, pady=20)

root.mainloop()
