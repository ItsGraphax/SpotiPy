import tkinter as tk
from tkinter import ttk
import json

# Load JSON file
with open("settings.json", "r") as file:
    settings = json.load(file)

def save_settings():
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)

# Function to update JSON data with new values
def update_json(key_path, value):
    obj = settings
    for key in key_path[:-1]:
        obj = obj[key]
    current_type = type(obj[key_path[-1]])
    if current_type is str:
        obj[key_path[-1]] = str(value)
    elif current_type is int:
        obj[key_path[-1]] = int(value)
    elif current_type is float:
        obj[key_path[-1]] = float(value)
    elif current_type is bool:
        obj[key_path[-1]] = value.lower() == 'true'
    else:
        obj[key_path[-1]] = value
    save_settings()

# Recursive function to create entry widgets for JSON data
def create_widgets(container, data, key_path=[]):
    for key, value in data.items():
        frame = ttk.Frame(container)
        frame.pack(fill="x", padx=5, pady=2)
        
        label = ttk.Label(frame, text=key)
        label.pack(side="left", padx=5)

        if isinstance(value, dict):
            nested_frame = ttk.Frame(container)
            nested_frame.pack(fill="x", padx=20)
            create_widgets(nested_frame, value, key_path + [key])
        else:
            entry = ttk.Entry(frame)
            entry.insert(0, str(value))
            entry.pack(side="right", fill="x", expand=True)

            entry.bind("<FocusOut>", lambda e, kp=key_path + [key], ent=entry: update_json(kp, ent.get()))

# Main application window
root = tk.Tk()
root.title("JSON Settings Editor")
root.tk.call('tk', 'scaling', 1)

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# Create widgets for settings JSON
create_widgets(main_frame, settings)

# Add a Save button to trigger saving manually
save_button = ttk.Button(root, text="Save Settings", command=save_settings)
save_button.pack(pady=1)

root.mainloop()
