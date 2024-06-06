import os
import json
import argparse
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtWidgets import QLabel, QSizePolicy

from bs4 import BeautifulSoup
import cssutils
import sys 
import re
import re
def html_to_json(html):
    print("Converting HTML to JSON...")
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    index = 1

    # Check if the HTML contains <p> tags
    if soup.find('p'):
        for p in soup.find_all('p'):
            # Parse inline style
            style = p.get('style', '')
            color = None
            match = re.search(r'color:\s*([^;]+)', style)
            if match:
                color = match.group(1).strip()
            # Remove escape characters
            text = p.text.encode('ascii', 'ignore').decode('unicode_escape')
            # Create a new entry for each p text
            data[index] = [text, color]
            index += 1
    else:
        # Fallback to original script if no <p> tags are found
        css = cssutils.parseString(soup.style.string)
        for span in soup.find_all('span'):
            # Parse the CSS class of the span
            css_class = span.get('class')[0]
            color = css.cssRules[css_class].style.color
            # Remove escape characters
            text = span.text.encode('ascii', 'ignore').decode('unicode_escape')
            # Create a new entry for each span text
            data[index] = [text, color]
            index += 1

    print("Conversion completed.")
    return json.dumps(data, indent=4)



#def process_file(filepath, output_dir=None):
#    with open(filepath, 'r', encoding='utf-8') as file:
#        html = file.read()
#    json_data = html_to_json(html)
#    if output_dir is None:
#        output_dir, filename = os.path.split(filepath)
#    base, _ = os.path.splitext(os.path.basename(filepath))
#    index = 1
#    while os.path.exists(os.path.join(output_dir, f"{base}_{index}.json")):
#        index += 1
#    with open(os.path.join(output_dir, f"{base}_{index}.json"), 'w') as file:
#        file.write(json_data)
#    print(f"File processed. Output saved to: {os.path.join(output_dir, f'{base}_{index}.json')}")

 
def process_file(filepath, output_dir=None):
    with open(filepath, 'r', encoding='utf-8') as file:
        html = file.read()
    json_data = html_to_json(html)
    if output_dir is None:
        output_dir, filename = os.path.split(filepath)
    base, _ = os.path.splitext(os.path.basename(filepath))
    output_file_path = os.path.join(output_dir, f"{base}.json")
    with open(output_file_path, 'w') as file:
        file.write(json_data)
    print(f"File processed. Output saved to: {output_file_path}")
    
class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        print("Initializing UI...")
        self.label = QLabel('Drag & Drop in or Select:', self)

        self.button = QPushButton('Select HTML file', self)
        self.button.clicked.connect(self.select_file)
        self.button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        print("UI initialized.")

    def select_file(self):
        print("Selecting file...")
        default_dir = os.path.dirname(os.path.abspath(__file__))
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open file', default_dir, "HTML files (*.html)")
        if not filepath:
            return
        print(f"File selected: {filepath}")
        process_file(filepath, os.path.dirname(filepath))


        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', help='Path to the HTML file')
    parser.add_argument('-o', help='Output directory')
    args = parser.parse_args()

    if args.file:
        print(f"Command line argument -file provided: {args.file}")
        if args.o:
            print(f"Command line argument -o provided: {args.o}")
            output_dir = args.o
        else:
            output_dir = os.path.dirname(args.file)
        process_file(args.file, output_dir)

        print("File processed successfully.")
        sys.exit(0)  # Exit with success
    else:  # No -file argument was passed
        print("Starting PyQt5 application...")
        app = QApplication(sys.argv)
        ex = FileSelector()
        ex.show()
        sys.exit(app.exec_())  # Use sys.exit here to ensure a clean exit


if __name__ == '__main__':
    print("Starting main function...")
    main()



