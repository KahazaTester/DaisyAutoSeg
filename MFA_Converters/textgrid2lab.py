import mytextgrid
import os
import argparse

def lowercase_and_remove_numbers(text):
    """Lowercase text and remove digits."""
    text = text.lower()
    return ''.join(c for c in text if not c.isdigit())

def load_converter(converter_path, apply_low_number=False):
    """
    Load the converter file into a dictionary with tuple keys.
    
    Args:
        converter_path (str): Path to the converter file.
        apply_low_number (bool): Whether to apply lowercase_and_remove_numbers to phonemes.
    
    Returns:
        dict: Dictionary mapping phoneme sequence tuples to replacements.
    """
    converter = {}
    try:
        with open(converter_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        sequence_str, replacement = parts
                        sequence = sequence_str.strip().split()
                        if apply_low_number:
                            sequence = [lowercase_and_remove_numbers(ph) for ph in sequence]
                        converter[tuple(sequence)] = replacement.strip()
    except FileNotFoundError:
        print(f"Error: Converter file '{converter_path}' not found.")
        raise
    except Exception as e:
        print(f"Error reading converter file: {e}")
        raise
    return converter

def textgrid_to_lab(textgrid_file, converter, use_converter=True, apply_low_number=False):
    """
    Convert a TextGrid file to LAB format, merging consecutive phoneme sequences as specified.
    
    Args:
        textgrid_file (str): Path to the TextGrid file.
        converter (dict): Dictionary of phoneme sequences to replacements.
        use_converter (bool): Whether to apply the converter.
        apply_low_number (bool): Whether to apply lowercase_and_remove_numbers to labels.
    
    Returns:
        list: List of LAB file lines.
    """
    try:
        tg = mytextgrid.read_from_file(textgrid_file)
    except Exception as e:
        print(f"Error reading TextGrid file '{textgrid_file}': {e}")
        return []

    # Collect intervals from the 'phones' tier
    intervals = []
    for tier in tg:
        if tier.name == 'phones' and tier.is_interval():
            for interval in tier:
                label = interval.text if interval.text else 'pau'
                if apply_low_number:
                    label = lowercase_and_remove_numbers(label)
                intervals.append((interval.xmin, interval.xmax, label))
    
    if not intervals:
        return []

    # Process intervals for sequence matching
    lab_lines = []
    i = 0
    max_seq_len = max(len(seq) for seq in converter.keys()) if converter else 1
    
    while i < len(intervals):
        if use_converter and converter:
            # Look for the longest matching sequence
            for k in range(min(max_seq_len, len(intervals) - i), 0, -1):
                seq = tuple(intervals[i + j][2] for j in range(k))
                if seq in converter:
                    start_time = intervals[i][0]
                    end_time = intervals[i + k - 1][1]
                    replacement = converter[seq]
                    lab_lines.append(f"{int(start_time * 10000000)} {int(end_time * 10000000)} {replacement}")
                    i += k
                    break
            else:
                # No sequence matched; use the original label
                start_time, end_time, label = intervals[i]
                lab_lines.append(f"{int(start_time * 10000000)} {int(end_time * 10000000)} {label}")
                i += 1
        else:
            # No converter applied; use original labels
            start_time, end_time, label = intervals[i]
            lab_lines.append(f"{int(start_time * 10000000)} {int(end_time * 10000000)} {label}")
            i += 1
    
    return lab_lines

def process_files(converter_path, output_dir=None, use_converter=True, apply_low_number=True):
    """
    Process all TextGrid files in the current directory and subdirectories.
    
    Args:
        converter_path (str): Path to the converter file.
        output_dir (str, optional): Directory for output LAB files.
        use_converter (bool): Whether to use the converter.
        apply_low_number (bool): Whether to apply lowercase_and_remove_numbers.
    """
    converter = load_converter(converter_path, apply_low_number)
    
    for subdir, _, files in os.walk("./"):
        for file in files:
            if file.endswith(".TextGrid"):
                textgrid_file = os.path.join(subdir, file)
                lab_lines = textgrid_to_lab(
                    textgrid_file,
                    converter,
                    use_converter=use_converter,
                    apply_low_number=apply_low_number
                )
                if not lab_lines:
                    continue
                
                lab_file = textgrid_file.replace(".TextGrid", ".lab")
                output_lab_file = lab_file
                
                # Handle output directory
                if output_dir:
                    rel_subdir = os.path.relpath(subdir, ".")
                    output_subdir = os.path.join(output_dir, rel_subdir)
                    os.makedirs(output_subdir, exist_ok=True)
                    output_lab_file = os.path.join(output_subdir, os.path.basename(lab_file))
                
                try:
                    with open(output_lab_file, 'w', encoding='utf-8') as f:
                        for line in lab_lines:
                            f.write(f"{line}\n")
                    print(f"Converted {textgrid_file} to {output_lab_file}")
                except Exception as e:
                    print(f"Error writing LAB file '{output_lab_file}': {e}")

def main():
    """Main function to parse arguments and initiate processing."""
    parser = argparse.ArgumentParser(description="Convert TextGrid files to LAB files.")
    parser.add_argument('-c', '--converter', type=str, required=True, help="Path to the converter file (.txt)")
    parser.add_argument('-o', '--output', type=str, help="Path to the output directory for LAB files")
    args = parser.parse_args()
    
    process_files(
        converter_path=args.converter,
        output_dir=args.output,
        use_converter=True,
        apply_low_number=True
    )

if __name__ == "__main__":
    main()
