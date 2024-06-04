import os
import json
import tkinter as tk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox
import sys
# Module level variables
playback_time = 0.0  # Range is 0-1
playback_speed = 1.0  # Default is 1, can be modified
recording = False  # Boolean to indicate if recording is happening

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

def listen_to_sound(file_name):
    # Implement your logic to play the sound file here
    print(f"Playing sound: {file_name}")

def record_sound(file_name, prefix):
    # Dummy function
    print(f"Recording sound for file: {prefix}_{file_name}")

def delete_recording(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"Deleted recording: {file_name}")
    else:
        print("The file does not exist")

def amend_text_to_json(file_path, data):
    new_text = simpledialog.askstring("Input", "Enter new text")
    if new_text:
        # Amend the data as per your requirement
        data['new_key'] = new_text
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
            
def play_from_crop(file_name, prefix):
    # Dummy function
    print(f"Playing from crop for file: {prefix}_{file_name}")

def stop_playback(file_name, prefix):
    # Dummy function
    print(f"Stopping playback for file: {prefix}_{file_name}")

def additional_output_prefix():
    prefix = simpledialog.askstring("Input", "Enter prefix")
    if prefix:
        prefix = prefix.replace('_', '')
    else:
        prefix = ''
    return prefix

def create_gui(data):
    root = tk.Tk()
    root.title("JSON Viewer")

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for key, value in data.items():
        row_frame = tk.Frame(scrollable_frame)
        row_frame.pack(fill='both', expand=True)

        text = tk.Text(row_frame)
        text.pack(side='left', fill='both', expand=True)

        text.insert(tk.END, f"Index: {key}\n")
        for item in value:
            text.insert(tk.END, f"Item: {item}\n")

        button_frame = tk.Frame(row_frame)
        button_frame.pack(side='left', fill='y')
        
        button_names = ["Listen to Sound", "Record Sound", "Delete Recording", "Amend Text to JSON", "Additional Output Prefix", "Play from crop", "Stop Playback"]
        button_functions = [listen_to_sound, record_sound, delete_recording, amend_text_to_json, additional_output_prefix, play_from_crop, stop_playback]
        for i in range(6):  # Adjust the range for the number of buttons you want
            prefix = additional_output_prefix()
            file_name = f"{file_path}_{prefix}"
            button = tk.Button(button_frame, text=button_names[i], command=lambda: button_functions[i](file_name, prefix))
            button.pack(side='top')

        # Add labels and sliders
        crop_label = tk.Label(row_frame, text="Crop")
        crop_label.pack(side='top')
        crop_slider1 = tk.Scale(row_frame, from_=0, to=100, orient='horizontal')
        crop_slider1.pack(side='top', fill='both', expand=True)
        crop_slider2 = tk.Scale(row_frame, from_=0, to=100, orient='horizontal')
        crop_slider2.pack(side='top', fill='both', expand=True)

        slider_label = tk.Label(row_frame, text="Slider")
        slider_label.pack(side='top')
        slider = tk.Scale(row_frame, from_=0, to=100, orient='horizontal')
        slider.pack(side='top', fill='both', expand=True)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    root.mainloop()

    
if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "path_to_your_file.json"
    data = load_json(file_path)
    create_gui(data, file_path)