import os
import argparse
import shutil

def process_directory(input_folder):
    """
    Processes a directory to:
    1. Delete non-.wav files.
    2. Remove underscores from .wav file names.
    3. Create corresponding .txt files (without suffix inside).
    4. Add a suffix to all files based on the folder name.
    """

    for root, dirs, files in os.walk(input_folder, topdown=False):
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

            # 2. Remove underscores from .wav names and add suffix
            new_base_name = base_name.replace("_", "")
            new_wav_name = f"{new_base_name}{suffix}{ext}"
            new_wav_path = os.path.join(root, new_wav_name)

            if file_path != new_wav_path:
                print(f"Renaming: {file_path} to {new_wav_path}")
                os.rename(file_path, new_wav_path)

            # 3. Create .txt file (without suffix inside)
            txt_file_name = f"{new_base_name}{suffix}.txt"  # Suffix here for filename only
            txt_file_path = os.path.join(root, txt_file_name)
            print(f"Creating: {txt_file_path}")

            with open(txt_file_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(new_base_name)  # Write ONLY the base name without suffix

        # 4. Add suffix to directories
        if root != input_folder:
            new_dir_name = os.path.basename(root) + suffix
            new_dir_path = os.path.join(os.path.dirname(root), new_dir_name)

            # Prevent folder name collisions
            count = 1
            while os.path.exists(new_dir_path):
                new_dir_name = f"{os.path.basename(root)}{suffix}_{count}"
                new_dir_path = os.path.join(os.path.dirname(root), new_dir_name)
                count += 1
            
            if root != new_dir_path:
                print(f"Renaming directory: {root} to {new_dir_path}")
                os.rename(root, new_dir_path)

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