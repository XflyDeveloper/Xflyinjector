import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import psutil
from pyinjector import inject
import os
import logging
import requests


def check():
    try:
        rr = requests.get("https://raw.githubusercontent.com/XflyDeveloper/Xflyinjector/refs/heads/main/VERSION.MD")
        v = rr.text.strip()
        if v != version:
            if messagebox.askyesno("Update Available", 
                                     "A new version is available, want to upgrade? (warning: DLLs may not save in new versions. you will have to put them in again.)"):
                os.startfile("https://github.com/XflyDeveloper/Xflyinjector")
                root.quit()
    except Exception as e:
        logging.error(f"{e}")

version = "1.0.0"
dlls = []
dllfile = "dlls.txt"
logs = "xfly.log"

logging.basicConfig(filename=logs, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_dlls():
    global dlls
    if os.path.exists(dllfile):
        with open(dllfile, "r") as file:
            dlls = [line.strip() for line in file.readlines()]
        update()

def save_dlls():
    with open(dllfile, "w") as file:
        for dll in dlls:
            file.write(dll + "\n")

def warning():
    messagebox.showwarning("Warning", "Xfly is not responsible for anything YOU inject, we are NOT responsible for any bans by injected dll's.")

def select_dll():
    dll_path = filedialog.askopenfilename(filetypes=[("DLL files", "*.dll")])
    if dll_path:
        dlls.append(dll_path)
        update()
        save_dlls()

def update():
    dll_listbox.delete(0, tk.END)
    for dll in dlls:
        dll_listbox.insert(tk.END, os.path.basename(dll))

def inject_all_dlls():
    status_text_label.configure(text="Injecting...")
    root.update()

    if not dlls:
        messagebox.showerror("Error", "No DLLs to inject.")
        logging.error("Injection attempted with no DLLs.")
        status_text_label.configure(text="Idle")
        return
    
    RL = "RocketLeague.exe"
    pid = None
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] == RL:
            pid = proc.info['pid']
            break
    
    if pid is None:
        messagebox.showerror("Error", f"{RL} is not running.")
        logging.error(f"{RL} is not running, injection aborted.")
        status_text_label.configure(text="Idle")
        return

    for dll in dlls:
        try:
            inject(pid, dll)
            logging.info(f"Injected: {os.path.basename(dll)}")
        except Exception as b:
            messagebox.showerror("Error", f"inject Failed {os.path.basename(dll)}: {str(b)}")
            logging.error(f"inject Failed {os.path.basename(dll)}: {str(b)}")

    messagebox.showinfo("Success", "injected Success.")
    reset()

def reset():
    update()
    status_text_label.configure(text="Idle")

def remove_dll():
    si = dll_listbox.curselection()
    if si:
        removed_dll = dlls.pop(si[0])
        update()
        save_dlls()
        logging.info(f"Removed: {removed_dll}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Xfly Injector")
root.geometry("500x350")
root.iconbitmap("logo.ico")
root.attributes("-topmost", True)

main_frame = ctk.CTkFrame(root)
main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

settings_frame = ctk.CTkFrame(root)
settings_frame.pack(side="right", fill="y", padx=10, pady=10)

title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
title_frame.pack(pady=10)

title_label_fly = ctk.CTkLabel(title_frame, text="Xfly", font=("Impact", 36, "bold"), text_color="white")
title_label_fly.pack(side="left")

title_label_x = ctk.CTkLabel(title_frame, text="Injector", font=("Impact", 36, "bold"), text_color="#7D3C98")
title_label_x.pack(side="left")

subtitle_label = ctk.CTkLabel(main_frame, text="A Rocket League injector.", font=("Arial", 12, "italic"))
subtitle_label.pack(pady=(0, 20))

config_label = ctk.CTkLabel(settings_frame, text="Config", font=("Arial", 12, "bold"))
config_label.pack(pady=(10, 0))

dll_listbox = tk.Listbox(settings_frame, selectmode=tk.SINGLE, bg="#333", fg="white", font=("Arial", 10))
dll_listbox.pack(pady=10, fill="y", expand=True)

button_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
button_frame.pack(pady=10)

select_dll_button = ctk.CTkButton(button_frame, text="Add DLL", command=select_dll, width=90, fg_color="#7D3C98", hover_color="#9B59B6")
select_dll_button.pack(side="left", padx=5)

remove_dll_button = ctk.CTkButton(button_frame, text="Remove DLL", command=remove_dll, width=90, fg_color="#7D3C98", hover_color="#9B59B6")
remove_dll_button.pack(side="left", padx=5)

inject_button = ctk.CTkButton(main_frame, text="Inject", command=inject_all_dlls, width=90, fg_color="#7D3C98", hover_color="#9B59B6")
inject_button.pack(pady=10)

status_text_label = ctk.CTkLabel(root, text="Idle", font=("Arial", 12))
status_text_label.pack(side="bottom", anchor="se", padx=10, pady=10)

load_dlls()
warning()
check()

root.mainloop()
