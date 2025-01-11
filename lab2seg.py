import os
import argparse
import re

def convert_lab_to_seg(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for lab_file_name in os.listdir(input_directory):
        if lab_file_name.endswith(".lab"):
            input_lab_file = os.path.join(input_directory, lab_file_name)
            output_seg_file = os.path.join(output_directory, lab_file_name.replace(".lab", ".seg"))

            phoneme_list = []

            try:
                with open(input_lab_file, 'r') as infile:
                    lines = infile.readlines()

                for line in lines:
                    line = line.strip()
                    match = re.match(r'(\d+)\s+(\d+)\s+(.+)', line)
                    if match:
                        start_time = float(match.group(1)) / 1e7
                        end_time = float(match.group(2)) / 1e7
                        phoneme = match.group(3)


                        # The correct way to handle "R" and "pau" is to check for them
                        # before removing digits
                        if phoneme == "R" or phoneme == "pau":
                            phoneme = "Sil"

                        phoneme_list.append((phoneme, start_time, end_time))

                if phoneme_list:
                    with open(output_seg_file, 'w') as outfile:
                        outfile.write("nPhonemes {}\n".format(len(phoneme_list)))
                        outfile.write("articulationsAreStationaries 0\n")
                        outfile.write("phoneme\t\tBeginTime\t\tEndTime\n")
                        outfile.write("=" * 49 + "\n")
                        for phoneme, start_time, end_time in phoneme_list:
                            outfile.write("{}\t\t{:.6f}\t\t{:.6f}\n".format(phoneme, start_time, end_time))

                    print(f"Conversion complete for {lab_file_name}")
                else:
                    print(f"Skipping empty file: {lab_file_name}")
            except FileNotFoundError:
                print(f"Error: Input file not found: {input_lab_file}")
            except Exception as e:
                print(f"Error processing {lab_file_name}: {e}")

    print("All conversions complete.")

def main():
    parser = argparse.ArgumentParser(description="Convert .lab files to .seg files.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input directory containing .lab files.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output directory where .seg files will be saved.")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input directory does not exist: {args.input}")
        return

    convert_lab_to_seg(args.input, args.output)

if __name__ == "__main__":
    main()