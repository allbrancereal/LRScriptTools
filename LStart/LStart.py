import argparse
import subprocess
import tkinter as tk
from tkinter import filedialog
import os
import sys

def main(input_file=None, time_per_word=None, output_dir=None):
    # If no input file is provided, ask the user to select a file
    if input_file is None:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        input_file = filedialog.askopenfilename()

    # Define the path to the bin directory
    bin_dir = os.path.join(os.path.dirname(sys.executable), 'bin')
    # Define the paths to the external scripts
    scripts = ['LTextTagger.exe', 'LScriptGenerator.exe', 'LPremiereWavPrepare.exe']
    script_paths = {script: os.path.join(bin_dir, script) for script in scripts}
    
    # Check if the external scripts exist
    for script, path in script_paths.items():
        if not os.path.exists(path):
            print(f"Error: {script} does not exist at {path}")
            return
        
    # Run LTextTagger.py
    output_html_file = input_file.replace('.txt', '.html')
    print(f"Running: {script_paths['LTextTagger.exe']}")
    subprocess.run([script_paths['LTextTagger.exe'], '-file', input_file], check=True)

    output_json_file = os.path.join(output_dir, os.path.basename(output_html_file).replace('.html', '.json')) if output_dir else output_html_file.replace('.html', '.json')
    print(f"Running: {script_paths['LScriptGenerator.exe']}")
    subprocess.run([script_paths['LScriptGenerator.exe'], '-file', output_html_file, '-o', output_dir if output_dir else os.path.dirname(output_html_file)], check=True)

    # Run LPremiereWavPrepare.py
    print(f"Running: {script_paths['LPremiereWavPrepare.exe']}")
    subprocess.run([script_paths['LPremiereWavPrepare.exe'], '-file', output_json_file, '-time_per_word', str(time_per_word)], check=True)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a text file.')
    parser.add_argument('-file', help='the path to the input text file')
    parser.add_argument('-o', help='the path to the output directory')
    parser.add_argument('-time_per_word', type=float, default=0.6, help='the time per word in seconds')
    args = parser.parse_args()
    main(args.file, args.time_per_word, args.o)
