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

    # Run LTextTagger.py
    output_html_file = input_file.replace('.txt', '.html')
    ltexttagger_path = os.path.join(bin_dir, 'LTextTagger.exe')
    print(f"Running: {ltexttagger_path}")
    subprocess.run([ltexttagger_path, '-file', input_file], check=True)

    # Run LScriptGenerator.py
    output_json_file = os.path.join(output_dir, os.path.basename(output_html_file).replace('.html', '.json')) if output_dir else output_html_file.replace('.html', '.json')
    lscriptgenerator_path = os.path.join(bin_dir, 'LScriptGenerator.exe')
    print(f"Running: {lscriptgenerator_path}")
    subprocess.run([lscriptgenerator_path, '-file', output_html_file, '-o', output_dir if output_dir else os.path.dirname(output_html_file)], check=True)

    # Run LPremiereWavPrepare.py
    lpremierewavprepare_path = os.path.join(bin_dir, 'LPremiereWavPrepare.exe')
    print(f"Running: {lpremierewavprepare_path}")
    subprocess.run([lpremierewavprepare_path, '-file', output_json_file, '-time_per_word', str(time_per_word)], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a text file.')
    parser.add_argument('-file', help='the path to the input text file')
    parser.add_argument('-o', help='the path to the output directory')
    parser.add_argument('-time_per_word', type=float, default=0.6, help='the time per word in seconds')
    args = parser.parse_args()
    main(args.file, args.time_per_word, args.o)
