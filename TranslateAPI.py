import os
import re
import translators as ts

def is_english(text):
    return all(ord(char) < 128 for char in text)

def translate_comments(input_file, error_log):
    try:
        with open(input_file, 'r', encoding='GBK', errors='ignore') as file:
            lines = file.readlines()

        # Translate each non-English comment in-place
        for i, line in enumerate(lines):
            comments = re.findall(r'/\*.*?\*/|//.*?(?=\n|$)', line, re.DOTALL)
            for comment in comments:
                if not is_english(comment):
                    try:
                        translated_comment = ts.google(comment)
                        lines[i] = lines[i].replace(comment, translated_comment)
                    except Exception as e:
                        error_log.write(f"Error translating {input_file}, line {i + 1}: {str(e)}\n")

        # Write the translated code back to the input file
        with open(input_file, 'w', encoding='UTF-8') as file:
            file.writelines(lines)

    except Exception as e:
        error_log.write(f"Error processing {input_file}: {str(e)}\n")

def translate_files_in_directory(directory):
    error_log_path = os.path.join(directory, 'translation_errors.log')

    with open(error_log_path, 'w', encoding='UTF-8') as error_log:
        for filename in os.listdir(directory):
            if filename.endswith(".h") or filename.endswith(".c"):
                input_file_path = os.path.join(directory, filename)
                translate_comments(input_file_path, error_log)
                print(f"{filename} is now translated.")

# Example usage
directory_path = r'C:\Users\s.bazargan\Desktop\mh1902t\firmware_pos\src\app\ped'
translate_files_in_directory(directory_path)
