import re
import translators as ts

def translate_comments(input_file, output_file, error_log):
    with open(input_file, 'r', encoding='GBK') as file:
        c_code = file.read()

    comments = re.findall(r'/\*.*?\*/|//.*?(?=\n|$)', c_code, re.DOTALL)

    # Translate each comment
    translated_comments = []
    for comment in comments:
        try:
            translated_comment = ts.google(comment)
            if translated_comment:
                translated_comments.append(translated_comment)
            else:
                error_log.write(f"Translation failed for comment: {comment}\n")
        except Exception as e:
            error_log.write(f"Error translating comment: {e}\n")
            translated_comments.append(comment)  # Use the original comment if translation fails

    # Replace original comments with translated comments
    translated_code = c_code
    for original, translated in zip(comments, translated_comments):
        translated_code = translated_code.replace(original, translated)

    # Write the translated code to the output file
    with open(output_file, 'w', encoding='UTF-8') as output_file:
        output_file.write(translated_code)

# Example usage
input_file_path = r'D:\PedDrv.h'
output_file_path = r'D:\MYPedDrv.h'
error_log_path = r'D:\translation_errors.log'

with open(error_log_path, 'w', encoding='UTF-8') as error_log:
    translate_comments(input_file_path, output_file_path, error_log)
