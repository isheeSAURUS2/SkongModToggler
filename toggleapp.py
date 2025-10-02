import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# 🔧 Change this path to your actual mods folder
GAME_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\Hollow Knight Silksong\BepInEx"
ENABLED = os.path.join(GAME_DIR, "plugins")
DISABLED = os.path.join(GAME_DIR, "plugins-disabled")

mods = []       # list of mod paths
modbuttons = {} # maps mod path → Checkbutton widget

# --- Scan for mods ---
for (root_dir, dirs, file) in os.walk(ENABLED):
    for f in file:
        if f.endswith(".dll"):
            mods.append(os.path.join(root_dir, f))
for (root_dir, dirs, file) in os.walk(DISABLED):
    for f in file:
        if f.endswith(".dll"):
            mods.append(os.path.join(root_dir, f))

print("Found mods:", mods)


# --- Core functions ---
def mod_on(modpath=""):
    """Enable a single mod."""
    try:
        if os.path.isfile(modpath):
            modname = os.path.basename(modpath)
            src = os.path.join(DISABLED, modname)
            dst = os.path.join(ENABLED, modname)
            shutil.move(src, dst)
            return dst
        else:
            # maybe already in ENABLED
            modname = os.path.basename(modpath)
            dst = os.path.join(ENABLED, modname)
            if os.path.isfile(dst):
                return dst
            print("mod_on: file not found", modpath)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


def mod_off(modpath=""):
    """Disable a single mod."""
    try:
        if os.path.isfile(modpath):
            modname = os.path.basename(modpath)
            src = os.path.join(ENABLED, modname)
            dst = os.path.join(DISABLED, modname)
            shutil.move(src, dst)
            return dst
        else:
            # maybe already in DISABLED
            modname = os.path.basename(modpath)
            dst = os.path.join(DISABLED, modname)
            if os.path.isfile(dst):
                return dst
            print("mod_off: file not found", modpath)
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


def toggle_action(path_var, switchvar):
    """Called when a checkbox is clicked."""
    modpath = path_var.get()
    new_path = None
    if switchvar:
        new_path = mod_on(modpath)
    else:
        new_path = mod_off(modpath)
    if new_path:
        path_var.set(new_path)


# --- UI Setup ---
root = tk.Tk()
root.title("Silksong Mods Manager")
root.geometry("650x650")
root.configure(bg="#2b2b2b")

# Apply dark theme
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#2b2b2b")
style.configure("TLabelframe", background="#2b2b2b", foreground="#ffffff")
style.configure("TLabelframe.Label", background="#2b2b2b", foreground="#ffffff", font=("Segoe UI", 12, "bold"))
style.configure("TLabel", background="#2b2b2b", foreground="#ffffff", font=("Segoe UI", 12))
style.configure("TButton", background="#4e5254", foreground="#ffffff", font=("Segoe UI", 10), padding=6)
style.map("TButton",
          background=[("active", "#5a5d60"), ("pressed", "#6b6e70")],
          foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])
style.configure("TCheckbutton", background="#2b2b2b", foreground="#ffffff", font=("Segoe UI", 10))

# Title
title_frame = ttk.Frame(root, padding=10)
title_frame.pack(fill="x")
ttk.Label(title_frame, text="Silksong Mods Manager", font=("Segoe UI", 16, "bold")).pack()

# Global toggle buttons
controls_frame = ttk.Frame(root, padding=10)
controls_frame.pack(fill="x")

# Scrollable mod list
mods_frame = ttk.LabelFrame(root, text="Mods", padding=10)
mods_frame.pack(fill="both", expand=True, padx=10, pady=10)

canvas = tk.Canvas(mods_frame, bg="#2b2b2b", highlightthickness=0)
scrollbar = ttk.Scrollbar(mods_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas, style="TFrame")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")



def make_mod_button(modpath="", isenabled=True):
    switch_var = tk.BooleanVar(root, value=isenabled)
    path_var = tk.StringVar(root, value=modpath)

    toggle = ttk.Checkbutton(
        scrollable_frame,
        text=os.path.basename(modpath),
        variable=switch_var,
        command=lambda v=switch_var, p=path_var: toggle_action(p, v.get())
    )
    toggle.pack(anchor="w", pady=2)

    # store variables on widget for toggle_mods
    toggle.path_var = path_var
    toggle.switch_var = switch_var

    modbuttons[modpath] = toggle
    return toggle


# Create mod buttons
for mod in mods:
    statuspath = os.path.dirname(mod)
    status = os.path.basename(statuspath)

    if status == "plugins":
        make_mod_button(mod, True)
    elif status == "plugins-disabled":
        make_mod_button(mod, False)

root.mainloop()
