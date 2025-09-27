import os
import shutil
import tkinter as tk
from os import mkdir
from tkinter import messagebox
from tkinter import filedialog

# 🔧 Change this path to your actual mods folder
GAME_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\Hollow Knight Silksong\BepInEx"
ENABLED = os.path.join(GAME_DIR, "plugins")
DISABLED = os.path.join(GAME_DIR, "plugins-disabled")

def toggle_mods(turn_on=True):
    global ENABLED, DISABLED, GAME_DIR
    try:
        if os.path.isdir(GAME_DIR):
            if os.path.isdir(DISABLED):
                if turn_on:
                    # Move everything from disabled → enabled
                    for f in os.listdir(DISABLED):
                        src = os.path.join(DISABLED, f)
                        dst = os.path.join(ENABLED, f)
                        shutil.move(src, dst)
                    messagebox.showinfo("Mods Manager", "✅ Mods turned ON")
                else:
                    # Move everything from enabled → disabled
                    for f in os.listdir(ENABLED):
                        src = os.path.join(ENABLED, f)
                        dst = os.path.join(DISABLED, f)
                        shutil.move(src, dst)
                    messagebox.showinfo("Mods Manager", "❌ Mods turned OFF")
            else:
                res=messagebox.askquestion("Make disabled directory?", "There was no disabled directory found. Do you want to create it and continue?")
                if res == "yes":
                    os.mkdir(DISABLED)
                    toggle_mods(turn_on)
                else:
                    messagebox.showinfo("Sure but like then it wont work LOL")
        else:
            messagebox.showinfo("Please select the BepInEx folder within your game files")
            selected_dir=filedialog.askdirectory(parent=root, initialdir=GAME_DIR, title="Select BepInEx Folder")
            if os.path.isdir(selected_dir):
                GAME_DIR=selected_dir
                ENABLED = os.path.join(GAME_DIR, "plugins")
                DISABLED = os.path.join(GAME_DIR, "plugins-disabled")
                toggle_mods(turn_on)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# --- UI ---
root = tk.Tk()
root.title("Silksong Mods Toggle")
root.geometry("300x150")

label = tk.Label(root, text="Toggle Mods", font=("Arial", 14))
label.pack(pady=10)

btn_on = tk.Button(root, text="Turn Mods ON", width=20, command=lambda: toggle_mods(True))
btn_on.pack(pady=5)

btn_off = tk.Button(root, text="Turn Mods OFF", width=20, command=lambda: toggle_mods(False))
btn_off.pack(pady=5)

root.mainloop()
