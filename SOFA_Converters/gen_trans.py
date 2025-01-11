import os
import argparse

def process_directory(input_folder):
    """
    Processes a directory to:
    1. Delete non-.wav files.
    2. Remove underscores from .wav file names.
    3. Create corresponding .txt files (without suffix inside).
    4. Add a suffix to .wav and .txt files based on the folder name.
    """

    for root, _, files in os.walk(input_folder):  # No need for topdown=False now
        folder_name = os.path.basename(root)
        suffix = f"_{folder_name}"

        for file in files:
            file_path = os.path.join(root, file)
            base_name, ext = os.path.splitext(file)

            # 1. Delete non-.wav files
            if ext.lower() != ".wav":
                print(f"Deleting: {file_path}")
                os.remove(file_path)
                continue

            # 2. Remove underscores from .wav names and add suffix to .wav file
            new_base_name = base_name.replace("_", "")
            new_wav_name = f"{new_base_name}{suffix}{ext}"
            new_wav_path = os.path.join(root, new_wav_name)

            if file_path != new_wav_path:  # Avoid unnecessary renaming
                print(f"Renaming: {file_path} to {new_wav_path}")
                os.rename(file_path, new_wav_path)

            # 3. Create .txt file with suffix in the name (but not inside)
            txt_file_name = f"{new_base_name}{suffix}.txt"
            txt_file_path = os.path.join(root, txt_file_name)
            print(f"Creating: {txt_file_path}")

            with open(txt_file_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(new_base_name)  # Write only the base name

def main():
    """
    Parses command-line arguments and initiates the directory processing.
    """
    parser = argparse.ArgumentParser(description="Process a directory to modify .wav files and create .txt files.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input folder")

    args = parser.parse_args()

    if not os.path.isdir(args.input):
        print(f"Error: Invalid input directory: {args.input}")
        return

    process_directory(args.input)
    print("Directory processing complete!")

if __name__ == "__main__":
    main()