import mytextgrid
import os
import argparse
import shutil

# Setup CLI argument parser
parser = argparse.ArgumentParser(description="Convert TextGrid files to lab files.")
parser.add_argument('-c', '--converter', type=str, required=True, help="Path to the converter file (.txt)")
parser.add_argument('-o', '--output', type=str, help="Path to the output directory for lab files")
args = parser.parse_args()

use_converter = True  # Enable converter usage
low_number = True  # Remove numbers and transform text to lowercase

# Open, read and store info for conversion
with open(args.converter, 'r', encoding='utf-8') as converter_file:
    converter_text = converter_file.read()
    converter = dict(map(str.strip, line.split(',')) for line in converter_text.split('\n') if line.strip())

# Function to lowercase and remove numbers
def lowercase_and_remove_numbers(text):
    text = text.lower()
    text = ''.join(c for c in text if not c.isdigit())
    return text

# Function to convert TextGrid to lab file
def textgrid_to_lab(textgrid_file):
    tg = mytextgrid.read_from_file(textgrid_file)
    lab_lines = []
    for tier in tg:
        if tier.name == 'phones' and tier.is_interval():
            for interval in tier:
                time_start = int(float(interval.xmin)*10000000)
                time_end = int(float(interval.xmax)*10000000)
                label = interval.text
                if label == '':
                    label = 'pau'
                if low_number:
                    label = lowercase_and_remove_numbers(label)
                if use_converter:
                    label = converter.get(label, label)
                lab_lines.append(f"{time_start} {time_end} {label}")
    return lab_lines

# Process TextGrid files
for subdir, dirs, files in os.walk("./"):
    for file in files:
        if file.endswith(".TextGrid"):
            textgrid_file = os.path.join(subdir, file)
            lab_lines = textgrid_to_lab(textgrid_file)
            lab_file = textgrid_file.replace(".TextGrid", ".lab")

            # Handle output directory if specified
            if args.output:
                output_dir = os.path.join(args.output, os.path.relpath(subdir, "."))
                os.makedirs(output_dir, exist_ok=True)
                output_lab_file = os.path.join(output_dir, os.path.basename(lab_file))
            else:
                output_lab_file = lab_file
            
            with open(output_lab_file, 'w') as f:
                for lab_line in lab_lines:
                    f.write("%s\n" % lab_line)
            print(f"Converted {textgrid_file} to {output_lab_file}")