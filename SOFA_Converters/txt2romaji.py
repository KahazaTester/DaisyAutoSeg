import os
import argparse
import pykakasi

def convert_japanese_to_romaji(text):
    """
    Converts Japanese text to Romaji using a custom mapping,
    forcing 'ん' to be 'N', and adding spaces between most characters,
    while keeping specific consonant clusters and character combinations together.
    """

    custom_mapping = {
        'あ': 'a',
        'い': 'i',
        'う': 'u',
        'うぇ': 'we',
        'うぃ': 'wi',
        'え': 'e',
        'お': 'o',
        'か': 'ka',
        'が': 'ga',
        'き': 'ki',
        'ぎ': 'gi',
        'く': 'ku',
        'ぐ': 'gu',
        'け': 'ke',
        'げ': 'ge',
        'こ': 'ko',
        'ご': 'go',
        'さ': 'sa',
        'ざ': 'za',
        'し': 'shi',
        'じ': 'ji',
        'す': 'su',
        'ず': 'zu',
        'せ': 'se',
        'ぜ': 'ze',
        'そ': 'so',
        'ぞ': 'zo',
        'た': 'ta',
        'だ': 'da',
        'ち': 'chi',
        'つ': 'tsu',
        'て': 'te',
        'で': 'de',
        'と': 'to',
        'ど': 'do',
        'な': 'na',
        'に': 'ni',
        'ぬ': 'nu',
        'ね': 'ne',
        'の': 'no',
        'は': 'ha',
        'ば': 'ba',
        'ぱ': 'pa',
        'ひ': 'hi',
        'び': 'bi',
        'ぴ': 'pi',
        'ふ': 'hu',
        'ぶ': 'bu',
        'ぷ': 'pu',
        'へ': 'he',
        'べ': 'be',
        'ぺ': 'pe',
        'ほ': 'ho',
        'ぼ': 'bo',
        'ぽ': 'po',
        'ま': 'ma',
        'み': 'mi',
        'む': 'mu',
        'め': 'me',
        'も': 'mo',
        'や': 'ya',
        'ゆ': 'yu',
        'よ': 'yo',
        'ら': 'ra',
        'り': 'ri',
        'る': 'ru',
        'れ': 're',
        'ろ': 'ro',
        'わ': 'wa',
        'を': 'wo',
        'ん': 'N',
        'ヴぁ': 'va',
        'ヴぃ': 'vi',
        'ヴ': 'vu',
        'ヴぇ': 've',
        'ヴぉ': 'vo',
        '・': 'cl',
        "'": 'vf',
        'っ': 'xtu',

        # Combinations with small ya, yu, yo:
        'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
        'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
        'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
        'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
        'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
        'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
        'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
        'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
        'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
        'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
        'じゃ': 'ja',  'じゅ': 'ju',  'じょ': 'jo',
        'ぢゃ': 'ja',  'ぢゅ': 'ju',  'ぢょ': 'jo',
        'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',

        # Additional entries for small vowel combinations:
        'つぁ': 'tsa', 'つぃ': 'tsi', 'つぇ': 'tse', 'つぉ': 'tso',
        'ふぁ': 'fa', 'ふぃ': 'fi', 'ふぇ': 'fe', 'ふぉ': 'fo',
        'じゃ': 'ja', 'じゅ': 'ju', 'じぇ': 'je', 'じょ': 'jo',
        'ぢゃ': 'ja', 'ぢゅ': 'ju', 'じぇ': 'je', 'ぢょ': 'jo',

        # Small vowel combinations for "by"
        'びぇ': 'bye',

        # Hiragana for "du", "di", "ti", "tu"
        'どぅ': 'du', 'でぃ': 'di', 'てぃ': 'ti', 'とぅ': 'tu',

        # Hiragana for "xye" sounds
        'きぇ': 'kye',
        'みぇ': 'mye',
        'にぇ': 'nye',
        'ぴぇ': 'pye',
        'りぇ': 'rye',
        'ぎぇ': 'gye',
        'ひぇ': 'hye',
        'びぇ': 'bye',

        # Hiragana for "ye"
        'いぇ': 'ye',

        # Added replacements
        'ずぃ': 'zi',  # Hiragana for "zi"
        'しぇ': 'she', # Hiragana for "she"
        'ちぇ': 'che', # Hiragana for "che"
        'すぃ': 'si', # Hiragana for "si"
        'ほぅ': 'hu', # Hiragana for "hu"
        'わぅ': 'wu', # Hiragana for "wu"
        'うぉ': 'wo', # Hiragana for "wo"
    }
   
    # Consonant clusters to keep together (no internal spaces)
    consonant_clusters = ["ky", "py", "by", "ny", "my", "fy", "hy", "gy", "dy", "ty", "vy", "zy", "ry"]

    # Character combinations to be treated like clusters (no spaces within)
    special_combinations = ["ch", "sh", "ts", "dh", "th", "vf", "hh", "jh", "ng", "cl"]

    romaji_text = ""
    i = 0
    while i < len(text):
        matched = False
        # Prioritize longer combinations in custom_mapping
        for j in range(3, 0, -1):  # Check for 3, 2, and 1 character combinations
            if i + j <= len(text):
                kana = text[i:i+j]
                if kana in custom_mapping:
                    romaji_text += custom_mapping[kana]
                    i += j
                    matched = True
                    break
        if matched:
            continue

        # If not in custom_mapping, use pykakasi (for Kanji, etc.)
        kks = pykakasi.kakasi()
        result = kks.convert(text[i:i + 1])
        if result:
            item = result[0]  # Assuming single character conversion
            if item['orig'] == 'ん':
                romaji_text += 'N'
            else:
                romaji_text += item['hepburn']
        else:
            # Handle cases where pykakasi can't convert (punctuation, etc.)
            romaji_text += text[i]
        i += 1

    # Add spaces between characters, but not within clusters or special combinations
    spaced_romaji_text = ""
    i = 0
    while i < len(romaji_text):
        cluster_found = False

        # Check for consonant clusters first
        for cluster in consonant_clusters:
            if romaji_text.startswith(cluster, i):
                spaced_romaji_text += cluster + " "
                i += len(cluster)
                cluster_found = True
                break

        # Then check for special character combinations
        if not cluster_found:
            for combination in special_combinations:
                if romaji_text.startswith(combination, i):
                    spaced_romaji_text += combination + " "
                    i += len(combination)
                    cluster_found = True
                    break

        if not cluster_found:
            spaced_romaji_text += romaji_text[i] + " "
            i += 1

    return spaced_romaji_text.strip()
    
def process_file(filepath):
    """
    Reads a text file, converts Japanese text to Romaji with modifications,
    and overwrites the file.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        converted_content = convert_japanese_to_romaji(content)

        # Add "SP" at the beginning and end
        final_content = "SP " + converted_content + " SP"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"Processed: {filepath}")

    except UnicodeDecodeError:
        print(f"Skipped (likely not a text file or has incompatible encoding): {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_folder(folder_path):
    """
    Recursively processes all .txt files in a folder and its subfolders.
    """
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                process_file(filepath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Japanese text in .txt files to Romaji.")
    parser.add_argument("-i", "--input", required=True, help="Path to the folder containing .txt files")
    args = parser.parse_args()

    input_folder = args.input

    if not os.path.isdir(input_folder):
        print(f"Error: Input folder '{input_folder}' not found.")
    else:
        process_folder(input_folder)
        print("Romaji conversion complete!")