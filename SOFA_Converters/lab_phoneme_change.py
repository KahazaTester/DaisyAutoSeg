import argparse
import os
import glob

class SymbolConverter:
    """
    A class to handle the conversion of symbols in .lab files.
    """

    def __init__(self, converter_file):
        """
        Initializes the SymbolConverter with a conversion mapping.

        Args:
            converter_file (str): Path to the .txt file containing symbol mappings.
        """
        self.converter_map = self._load_converter_map(converter_file)

    def _load_converter_map(self, converter_file):
        """
        Loads the symbol mapping from the converter file.

        Args:
            converter_file (str): Path to the .txt file.

        Returns:
            dict: A dictionary mapping original symbols to replacement symbols.
        """
        converter_map = {}
        try:
            with open(converter_file, 'r') as f:
                for line in f:
                    original, replacement = line.strip().split(',')
                    converter_map[original] = replacement
        except FileNotFoundError:
            raise FileNotFoundError(f"Converter file not found: {converter_file}")
        except Exception as e:
            raise Exception(f"Error loading converter file: {e}")
        return converter_map

    def convert_lab_file(self, lab_file):
        """
        Converts the symbols in a single .lab file.

        Args:
            lab_file (str): Path to the .lab file.
        """
        try:
            with open(lab_file, 'r') as f_in:
                lines = f_in.readlines()

            converted_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 3:
                  
                    symbol = parts[2]
                    if symbol in self.converter_map:
                        parts[2] = self.converter_map[symbol]
                    converted_lines.append(" ".join(parts))
                else:
                  converted_lines.append(line)

            with open(lab_file, 'w') as f_out:
                f_out.write("\n".join(converted_lines))

        except Exception as e:
            print(f"Error processing {lab_file}: {e}")

    def convert_directory(self, input_dir):
        """
        Converts symbols in all .lab files within a directory and its subdirectories.

        Args:
            input_dir (str): Path to the input directory.
        """
        lab_files = glob.glob(os.path.join(input_dir, '**/*.lab'), recursive=True)
        for lab_file in lab_files:
            print(f"Converting: {lab_file}")
            self.convert_lab_file(lab_file)
        print(f"Conversion complete for directory: {input_dir}")

def main():
    """
    Parses command-line arguments and initiates the conversion process.
    """
    parser = argparse.ArgumentParser(description="Change symbols in .lab files.")
    parser.add_argument("-c", "--converter", required=True, help="Path to the converter .txt file")
    parser.add_argument("-i", "--input", required=True, help="Path to the input directory containing .lab files")
    args = parser.parse_args()

    try:
        converter = SymbolConverter(args.converter)
        converter.convert_directory(args.input)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()