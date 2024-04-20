import os


input_directory = './LetAIEntertainYou/Posts/Text'
output_directory = './LetAIEntertainYou/Posts/RuleGenerated'


os.makedirs(output_directory, exist_ok=True)

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try a different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()


for filename in os.listdir(input_directory):
    if filename.endswith('.txt'):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, 'processed_' + filename)

        content = read_text_file(input_file_path)
        words = content.split()
        first_10_words = words[:10]
        result_string = ' '.join(first_10_words)
        if len(words) > 10:
            result_string += '...'

        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(result_string + '\n')


