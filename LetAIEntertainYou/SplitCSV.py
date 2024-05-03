import csv
import os

# Path to the input CSV file
input_csv_path = 'LetAIEntertainYou//Posts/llama_unbloated.csv'

# Directory to store the output CSV files
output_directory = 'LetAIEntertainYou/csvchunks'
os.makedirs(output_directory, exist_ok=True)

# Number of records per file (excluding the header)
records_per_file = 40

def split_csv():
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)  # Read the first line as header

        # Initialize
        file_count = 1
        records = []

        for row in reader:
            records.append(row)
            # When we hit the records_per_file number, write to a new file
            if len(records) == records_per_file:
                write_to_file(records, header, file_count)
                file_count += 1
                records = []

        # Write any remaining records to a new file
        if records:
            write_to_file(records, header, file_count)

def write_to_file(records, header, file_count):
    output_file_path = os.path.join(output_directory, f'output_{file_count}.csv')
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(header)  # Write the header
        writer.writerows(records)  # Write the batch of records

if __name__ == '__main__':
    split_csv()


#ich habe hier mal mit den bestehenden daten ein paar judgements gemacht.
#factors quasi step back promted hier:
#https://chat.openai.com/share/06ef08e9-9672-4736-b579-f7d0448b8f45
# folgnder prompt:
"""imagine the following scenario:
on a neighborhood social media plattform, users can create all kinds of posts.
some user will activate email notification, meaning they get an email every time a post for their neighborhood is posted.
for this email, we will need a subject line that catches the users interest, meaning he clicks on the email.
the attached csv contains two versions for each post. The delimiter is ';'
your task is
1. to judge which one is more likely to produce a positive response, meaning the user will click on it.
2. please evaluate like a human would, so dont write code. focus on factors like engagement, specificity, urgency, and relevance. 
3. i only need your answer for each pair - so something like '1. A, 2. b' without explanation
4. Provide a judgement for every pair in the file. The file contains 40 pairs - so i need 40 judgements
5. provide your result like a python list
"""

output_9 = "1. A, 2. B, 3. B, 4. A, 5. A, 6. A, 7. B, 8. A, 9. A, 10. A, 11. A, 12. B, 13. A, 14. A, 15. A, 16. A, 17. A, 18. B, 19. B, 20. A, 21. B, 22. A, 23. B, 24. A, 25. A, 26. B, 27. B, 28. B, 29. A, 30. A, 31. B, 32. B, 33. A, 34. A, 35. B, 36. A, 37. A, 38. B, 39. A, 40. B."
parts = output_9.split(", ")
letters = [part.split(". ")[1].upper() for part in parts]
count_A = letters.count('A')

output_1 = ['B', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'B']
count_A = output_1.count('A')
