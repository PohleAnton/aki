import os
import csv

input_directory = './LetAIEntertainYou/Posts/Text'
output_directory = './LetAIEntertainYou/Posts/RuleGenerated'


os.makedirs(output_directory, exist_ok=True)

def read_text_file(file_path):
    """
        Reads the contents of a text file and returns it. If UTF-8 encoding fails, it attempts to read the file using Latin-1 encoding.

        Args:
            file_path (str): The path to the file to be read.

        Returns:
            str: The content of the file.
        """
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


def process_posts(input_csv_path, output_csv_path):
    """
    Reads a CSV file, processes text from the 'Posts' column by extracting the first 10 words,
    and writes the result into the 'Subject Line B' column of a new CSV file.

    Args:
        input_csv_path (str): The path to the input CSV file.
        output_csv_path (str): The path to the output CSV file where the processed data will be saved.
    """
    with open(input_csv_path, mode='r', newline='', encoding='windows-1252') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        headers = reader.fieldnames + [
            'Subject Line B'] if 'Subject Line B' not in reader.fieldnames else reader.fieldnames

        with open(output_csv_path, mode='w', newline='', encoding='windows-1252') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers, delimiter=';')
            writer.writeheader()

            for row in reader:
                content = row['Posts']
                words = content.split()
                first_10_words = words[:10]
                result_string = ' '.join(first_10_words)
                if len(words) > 10:
                    result_string += '...'

                row['Subject Line B'] = result_string
                writer.writerow(row)


# Usage
input_csv_path = 'LetAIEntertainYou/data/posts_neu.csv'
output_csv_path = 'LetAIEntertainYou/data/posts_rules_neu.csv'
process_posts(input_csv_path, output_csv_path)