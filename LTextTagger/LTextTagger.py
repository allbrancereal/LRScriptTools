import re
import os
import tkinter as tk
from tkinter import filedialog
import argparse

def split_into_sentences(text):
    sentence_endings = r"[.!?]"
    return re.split(sentence_endings, text)

def generate_html(sentences, colors):
    html = '''<html><head><meta content="text/html; charset=UTF-8" http-equiv="content-type"><style type="text/css">body { font-family: Arial; }</style></head><body class="c5 doc-content">'''
    color_index = 0
    last_color = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:  # Ignore empty sentences
            color = colors[color_index]
            html += f'<p class="c6" style="color: {color}">{sentence}.</p>'
            last_color = color
            color_index = (color_index + 1) % len(colors)
            # Ensure the same color is not used twice in a row
            if colors[color_index] == last_color:
                color_index = (color_index + 1) % len(colors)

    html += "</body></html>"
    return html


def main():
    parser = argparse.ArgumentParser(description='Colorize sentences in a text file.')
    parser.add_argument('-file', metavar='file', type=str, help='the path to the text file')
    args = parser.parse_args()

    colors = ["#f9cb9c", "#b6d7a8", "#d9ead3"]

    # If a file path was provided as a command-line argument, use it. Otherwise, open a file dialog.
    if args.file:
        input_file_path = args.file
    else:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        input_file_path = filedialog.askopenfilename()

    with open(input_file_path, "r", encoding='utf-8') as file:
        text = file.read()

    sentences = split_into_sentences(text)
    html = generate_html(sentences, colors)

    # Extract the filename from the input file path
    filename = os.path.basename(input_file_path)
    # Replace the extension with .html
    filename = os.path.splitext(filename)[0] + '.html'

    # Save the output HTML file in the same directory as the input file
    output_file_path = os.path.join(os.path.dirname(input_file_path), filename)
    with open(output_file_path, "w", encoding='utf-8') as file:
        file.write(html)

if __name__ == "__main__":
    main()
