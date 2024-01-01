import os
from googletrans import Translator

def is_chinese(text):
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def translate_comments(input_file, error_log):
    try:
        with open(input_file, 'r', encoding='gb2312', errors='ignore') as file:
            lines = file.readlines()

        translator = Translator()

        for i, line in enumerate(lines):
            parts = line.split('//')  # Split the line based on '//'
            translated_parts = []

            for part in parts:
                if is_chinese(part):
                    try:
                        translated_part = translator.translate(part, src='zh-CN', dest='en')
                        translated_parts.append(f"{translated_part.text}\n")
                    except Exception as e:
                        error_log.write(f"Error translating {input_file}, line {i + 1}, part: {str(e)}\n")
                else:
                    translated_parts.append(f"{part}")

            lines[i] = '//'.join(translated_parts)

        # Write the translated code back to the input file
        with open(input_file, 'w', encoding='UTF-8') as file:
            file.writelines(lines)

    except Exception as e:
        error_log.write(f"Error processing {input_file}: {str(e)}\n")

def translate_files_in_directory(directory):
    error_log_path = os.path.join(directory, 'translation_errors.log')

    with open(error_log_path, 'w', encoding='UTF-8') as error_log:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".h") or filename.endswith(".c"):
                    input_file_path = os.path.join(root, filename)
                    translate_comments(input_file_path, error_log)
                    print(f"{filename} is now translated.")


# Example usage
directory_path = r'D:\translated_M500\sp-m500-firmware\src'
translate_files_in_directory(directory_path)
