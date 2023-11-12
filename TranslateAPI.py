import re
import translators as ts

def translate_comments(input_file, output_file):
    with open(input_file, 'r', encoding='GBK') as file:
        c_code = file.read()

    comments = re.findall(r'/\*.*?\*/|//.*?(?=\n|$)', c_code, re.DOTALL)

    # Translate each comment
    translated_comments = []
    for comment in comments:
        translated_comment = ts.google(comment)
        translated_comments.append(translated_comment)

    # Replace original comments with translated comments
    translated_code = c_code
    for original, translated in zip(comments, translated_comments):
        translated_code = translated_code.replace(original, translated)

    # Write the translated code to the output file
    with open(output_file, 'w', encoding='UTF-8') as output_file:
        output_file.write(translated_code)

# Example usage
input_file_path = r'D:\reboot.h'
output_file_path = r'D:\Myreboot.h'
translate_comments(input_file_path, output_file_path)