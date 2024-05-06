import csv
import os
import pandas as pd

# Path to the input CSV file
input_csv_path = 'LetAIEntertainYou/Posts/llama_und_ChatGPT_unbloat.csv'

# Directory to store the output CSV files
output_directory = 'LetAIEntertainYou/csvchunks/both'
os.makedirs(output_directory, exist_ok=True)


records_per_file = 50

def split_csv():
    """
       Reads records from a CSV file, splits them into multiple files based on a preset number of records per file.

       This function assumes that the CSV file uses a semicolon (;) as a delimiter. It processes each row from the
       input CSV file and writes out a new CSV file whenever the number of records reaches a predefined limit (`records_per_file`).
       Any remaining records after processing in batches are written to a final CSV file.
       """
    with open(input_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        header = next(reader)

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


        if records:
            write_to_file(records, header, file_count)

def write_to_file(records, header, file_count):
    """
       Writes a list of records to a CSV file, including a header at the top of the file.

       Args:
           records (list): List of records to write to the file.
           header (list): The header row for the CSV file.
           file_count (int): A counter used to number and distinguish each output file.

       This function writes the records to a new CSV file in the specified output directory. Each output file is named
       according to its sequence number (`file_count`). The function assumes that the output directory is already specified
       in `output_directory`.
       """
    output_file_path = os.path.join(output_directory, f'output_{file_count}.csv')
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(header)
        writer.writerows(records)

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
4. Provide a judgement for every pair in the file. The file contains 100 pairs - so i need 100 judgements
5. provide your result like a python list
"""
#promt für 3 varianten
"""imagine the following scenario:
on a neighborhood social media plattform, users can create all kinds of posts.
some user will activate email notification, meaning they get an email every time a post for their neighborhood is posted.
for this email, we will need a subject line that catches the users interest, meaning he clicks on the email.
the attached csv contains three versions for each post. The delimiter is ';'
your task is
1. to judge which one is more likely to produce a positive response, meaning the user will click on it.
2. please evaluate like a human would, so dont write code. focus on factors like engagement, specificity, urgency, and relevance. 
3. i only need your answer for each pair - so something like '3. C, 2. A, 3.B' without explanation
4. Provide a judgement for every pair in the file. The file contains 50 tripplets- so i need 50 judgements
5. Do not try to extrapolate a pattern from a few examples, do not chose randomely - judge each tripplet on its own
6. provide your result like a python list

"""

output_9 = "1. A, 2. B, 3. B, 4. A, 5. A, 6. A, 7. B, 8. A, 9. A, 10. A, 11. A, 12. B, 13. A, 14. A, 15. A, 16. A, 17. A, 18. B, 19. B, 20. A, 21. B, 22. A, 23. B, 24. A, 25. A, 26. B, 27. B, 28. B, 29. A, 30. A, 31. B, 32. B, 33. A, 34. A, 35. B, 36. A, 37. A, 38. B, 39. A, 40. B."
parts = output_9.split(", ")
letters = [part.split(". ")[1].upper() for part in parts]
count_A = letters.count('A')

output_1 = ['B', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'B']
count_A = output_1.count('A')


singles_1 =[
    'B', 'B', 'B', 'B', 'B',
    'A', 'A', 'B', 'A', 'B',
    'A', 'B', 'B', 'A', 'B',
    'A', 'B', 'A', 'B', 'A',
    'A', 'B', 'A', 'B', 'A',
    'B', 'B', 'A', 'B', 'B',
    'A', 'B', 'A', 'A', 'B',
    'A', 'B', 'B', 'A', 'B',
    'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'B', 'A', 'B'
]
count_A = singles_1.count('A')
#22 - llama
#https://chat.openai.com/share/4d06efeb-e209-475f-9555-193908257210

singles_2 =[
    'B', 'B', 'B', 'B', 'A',
    'A', 'A', 'B', 'A', 'B',
    'B', 'A', 'A', 'B', 'A',
    'B', 'B', 'A', 'B', 'A',
    'B', 'B', 'B', 'A', 'B',
    'A', 'B', 'B', 'B', 'B',
    'B', 'B', 'A', 'B', 'A',
    'A', 'B', 'B', 'A', 'B',
    'B', 'B', 'B', 'B', 'B',
    'A', 'A', 'B', 'A', 'B'
]
count_A = singles_2.count('A')
#18 f llama
#https://chat.openai.com/share/ad6cdace-db04-4ff2-8557-e010bcd50e29

singles_3 = [
    'B', 'B', 'B', 'B', 'B', 'B', 'A', 'B', 'B', 'A',
    'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'B', 'A',
    'A', 'B', 'B', 'B', 'A', 'B', 'B', 'B', 'B', 'A',
    'A', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'B', 'B',
    'A', 'B', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'A'
]

count_A = singles_3.count('A')
#14
#https://chat.openai.com/share/b9541b4f-ffcb-464b-8bad-cf59f5a6c37c

singles_4 =['A', 'A', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A',
 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'A',
 'A', 'B', 'A', 'B', 'B', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'B', 'A',
 'A', 'B', 'A', 'A', 'B', 'A', 'A', 'B', 'B', 'A']

count_A = singles_4.count('A')
#27
#https://chat.openai.com/share/ad7b0bff-c039-47d6-b1ea-e3b40dfb8351

singles_5=['B', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'B', 'A', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'B']

count_A = singles_5.count('A')
#22
#https://chat.openai.com/share/b085b97d-8730-448f-bb66-8fcadbd43643

singles_6 =[
    'B', 'A', 'A', 'B', 'A',
    'A', 'B', 'B', 'A', 'B',
    'A', 'B', 'B', 'A', 'B',
    'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'B', 'A', 'B',
    'A', 'A', 'B', 'B', 'A',
    'B', 'B', 'A', 'B', 'A',
    'A', 'B', 'A', 'B', 'B',
    'A', 'A', 'B', 'B', 'B',
    'A', 'A', 'B', 'A', 'B'
]
count_A = singles_6.count('A')
#24
#https://chat.openai.com/share/fdd51cff-2480-457b-bfe5-5c53dcccc44a


singles_7 =['A', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'A', 'A', 'B', 'B']


count_A = singles_7.count('A')
#49
#https://chat.openai.com/share/b69835ba-52dd-412e-a216-6c7f77021d4b
singles_8 = [
    "B", "B", "B", "B", "A", "A", "B", "A", "B", "A",
    "B", "A", "B", "A", "A", "B", "A", "B", "A", "B",
    "A", "B", "A", "B", "B", "A", "B", "A", "B", "B",
    "A", "B", "A", "A", "B", "A", "B", "B", "B", "A",
    "B", "A", "A", "B", "B", "B", "B", "A", "A", "A",
    "A", "A", "B", "A", "B", "B", "A", "B", "B", "B",
    "B", "B", "B", "A", "B", "A", "A", "B", "A", "B",
    "B", "B", "A", "A", "B", "B", "B", "A", "A", "B",
    "B", "A", "B", "B", "B", "B", "B", "B", "B", "A",
    "A", "A", "B", "A", "B", "B", "A", "B", "A", "B"
]
count_A = singles_8.count('A')
#42 (of COURSE)
#https://chat.openai.com/share/7ccb8160-81dd-4cd3-948a-0b842824f81d

singles_9 = [
    "B", "B", "B", "A", "B",
    "A", "B", "B", "A", "B",
    "A", "A", "B", "B", "A",
    "B", "B", "B", "A", "B",
    "A", "B", "B", "A", "B",
    "A", "A", "B", "B", "A",
    "B", "B", "B", "A", "B",
    "A", "B", "B", "A", "B",
    "A", "A", "B", "B", "A",
    "B", "B", "B", "A", "B",
    "A", "B", "B", "A", "B",
    "A", "A", "B", "B", "A",
    "B", "B", "B", "A", "B",
    "A", "B", "B", "A", "B",
    "A", "A", "B", "B", "A",
    "B", "B", "B", "A", "B",
    "A", "B", "B", "A", "B",
    "A", "A", "B", "B", "A",
    "B", "B", "B", "A", "B",
    "A", "B", "B", "A", "B"
]
count_A = singles_9.count('A')
#21
#https://chat.openai.com/share/7a54fd7a-282d-4575-8e1e-53548b944f95

singles_10 = ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B',
 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']

count_A = singles_10.count('A')
#50
#https://chat.openai.com/share/f5c676cf-5221-4386-9d28-41c6e96ff76a


singles_11 =[
    'B', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'A', 'B',
    'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'B']

count_A = singles_11.count('A')
#40
#https://chat.openai.com/share/b9e3eba0-f858-4997-990e-54f29d46d2ba

singles_12 =[
    "A", "B", "B", "B", "B",  # 1-5
    "A", "A", "B", "A", "B",  # 6-10
    "A", "B", "A", "B", "A",  # 11-15
    "B", "B", "A", "B", "B",  # 16-20
    "B", "A", "B", "B", "A",  # 21-25
    "B", "A", "A", "B", "A",  # 26-30
    "B", "B", "A", "A", "B",  # 31-35
    "A", "A", "B", "B", "B",  # 36-40
    "B", "A", "A", "B", "B",  # 41-45
    "B", "A", "A", "B", "B",  # 46-50
    "B", "A", "B", "A", "B",  # 51-55
    "B", "A", "B", "A", "A",  # 56-60
    "B", "B", "A", "A", "B",  # 61-65
    "A", "A", "B", "A", "B",  # 66-70
    "A", "A", "B", "A", "A",  # 71-75
    "A", "B", "A", "B", "B",  # 76-80
    "B", "A", "B", "B", "A",  # 81-85
    "B", "A", "A", "A", "B",  # 86-90
    "A", "A", "B", "A", "A",  # 91-95
    "B", "B", "B", "B", "B"   # 96-100
]

count_A = singles_12.count('A')
#46
#https://chat.openai.com/share/66b7d28a-8989-437d-bbd2-1e0806c57a7c

singles_13 =[
    "B", "B", "B", "B", "B",
    "A", "B", "A", "A", "B",
    "B", "A", "B", "A", "A",
    "A", "B", "A", "A", "B",
    "B", "A", "A", "A", "B",
    "A", "B", "B", "A", "B",
    "A", "A", "B", "A", "B",
    "A", "A", "B", "B", "B",
    "B", "A", "B", "B", "B",
    "B", "B", "A", "A", "B",
    "A", "A", "B", "A", "B",
    "B", "A", "A", "A", "B",
    "B", "A", "B", "A", "A",
    "B", "A", "B", "A", "B",
    "A", "B", "B", "A", "B",
    "A", "A", "B", "B", "B",
    "A", "B", "A", "B", "A",
    "B", "B", "B", "A", "A",
    "B", "A", "B", "A", "A",
    "A", "B", "B", "A", "B"
]
count_A = singles_13.count('A')
#47
#https://chat.openai.com/share/e8667662-83a2-43e1-a80c-6155936ea5c1

singles_14 = ['A', 'B', 'B', 'B', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'A', 'B']
count_A = singles_14.count('A')
#7
#https://chat.openai.com/share/6cfc1da2-98eb-4b21-acaa-082cfd64e7c4





all_singles=[]

for i in range(1, 15):  # From single_1 to single_14
    list_name = f'singles_{i}'
    # Retrieve the list using its name from the globals dictionary
    current_list = globals().get(list_name, [])
    all_singles.extend(current_list)
count_A = all_singles.count('A')
count_B = all_singles.count('B')

#für a: 44,88 %
#für b: 55.12 %

#both:

three_1 = ["C", "A", "B", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B",
 "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A",
 "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C",
 "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B",
 "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A", "B", "C", "A"]

count_A = three_1.count('A')
count_B = three_1.count('B')
#a34, b33, 33
#https://chat.openai.com/share/69b0d138-c152-4d18-8efd-978c2758b510

three_2 = ['C', 'B', 'B', 'C', 'C', 'B', 'C', 'A', 'B', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C']


count_A = three_2.count('A')
count_B = three_2.count('B')
#13, 18, 19

three_3 = judgments = [
    'B', 'B', 'C', 'C', 'C',
    'A', 'A', 'B', 'B', 'A',
    'C', 'B', 'C', 'B', 'B',
    'A', 'C', 'A', 'C', 'B',
    'C', 'A', 'B', 'C', 'A',
    'B', 'C', 'B', 'A', 'C',
    'A', 'B', 'C', 'B', 'A',
    'C', 'A', 'B', 'C', 'A',
    'B', 'C', 'B', 'A', 'C',
    'A', 'B', 'C', 'B', 'A'
]

count_A = three_3.count('A')
count_B = three_3.count('B')
#15,18,17
#https://chat.openai.com/share/876bb195-5cdf-424c-8ac8-1349f1cbead9
three_4 = ['C', 'B', 'B', 'C', 'B', 'A', 'B', 'A', 'A', 'A',
 'B', 'B', 'A', 'A', 'B', 'B', 'C', 'B', 'A', 'B',
 'A', 'B', 'A', 'A', 'C', 'B', 'A', 'C', 'A', 'B',
 'A', 'B', 'A', 'A', 'C', 'A', 'A', 'A', 'A', 'B',
 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'C', 'A', 'B']

count_A = three_4.count('A')
count_B = three_4.count('B')
#23,20,7
#https://chat.openai.com/share/7387407d-921d-45c0-b0cb-60d6881a35c8


three_5 = ['C', 'C', 'A', 'B', 'A', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A']


count_A = three_5.count('A')
count_B = three_5.count('B')
#19,17,14
#https://chat.openai.com/share/6c92856a-2dd4-4269-a7fa-bfff352bef33

three_6 = ['C', 'A', 'C', 'C', 'B', 'A', 'C', 'B', 'A', 'C',
 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B',
 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A',
 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C',
 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B']


count_A = three_6.count('A')
count_B = three_6.count('B')
#https://chat.openai.com/share/42453305-1e6d-4aa9-b30e-2a66471c7b7b
#16,16,18


three_7 = ['C', 'B', 'C', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'A', 'A', 'B', 'C', 'B', 'A', 'C', 'A', 'B', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'A']



count_A = three_7.count('A')
count_B = three_7.count('B')
#16,17,17
#https://chat.openai.com/share/17ff5d98-5b55-45a2-8d0c-7a20b50aa5a2


three_8 = [
    "A", "B", "B", "B", "B",
    "A", "C", "B", "C", "B",
    "A", "B", "A", "B", "B",
    "A", "A", "A", "B", "C",
    "B", "C", "B", "A", "A",
    "B", "A", "C", "B", "B",
    "A", "B", "A", "B", "B",
    "A", "A", "A", "B", "C",
    "B", "C", "B", "A", "A",
    "B", "A", "C", "B", "B"
]


count_A = three_8.count('A')
count_B = three_8.count('B')
#18,24,18
#https://chat.openai.com/share/701598de-0e2f-4665-ae59-59dbb22d2803

three_9 = ['C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A',
 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A',
 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A',
 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A',
 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A']



count_A = three_9.count('A')
count_B = three_9.count('B')
#15,20,15
#https://chat.openai.com/share/102564cc-479b-4821-8d72-54d6a5c01af1

three_10 = [
    'C', 'B', 'C', 'C', 'B', # 1-5
    'B', 'A', 'C', 'B', 'A', # 6-10
    'C', 'A', 'B', 'A', 'C', # 11-15
    'B', 'C', 'B', 'C', 'B', # 16-20
    'A', 'C', 'B', 'A', 'B', # 21-25
    'C', 'A', 'B', 'C', 'A', # 26-30
    'B', 'C', 'A', 'B', 'C', # 31-35
    'A', 'C', 'B', 'A', 'C', # 36-40
    'B', 'A', 'C', 'B', 'C', # 41-45
    'A', 'B', 'C', 'B', 'A'  # 46-50
]



count_A = three_10.count('A')
count_B = three_10.count('B')
#14,18,18
#https://chat.openai.com/share/ad620430-f2c8-48a9-ada3-40937274edb9


three_11 = [
    'B', 'A', 'C', 'C', 'C',
    'B', 'A', 'B', 'A', 'C',
    'B', 'C', 'A', 'B', 'A',
    'C', 'B', 'C', 'B', 'A',
    'C', 'B', 'A', 'C', 'B',
    'A', 'C', 'B', 'A', 'C',
    'B', 'A', 'C', 'B', 'A',
    'C', 'B', 'A', 'C', 'B',
    'A', 'C', 'B', 'A', 'C',
    'B', 'A', 'C', 'B', 'A'
]



count_A = three_11.count('A')
count_B = three_11.count('B')
#16,17,17
#https://chat.openai.com/share/8aecb3d0-d22b-4cd4-9fbf-b9b8812c1a9f

three_12 = [
    "A", "C", "B", "C", "A", "A", "C", "B", "C", "B",
    "A", "C", "A", "B", "C", "B", "A", "C", "B", "A",
    "C", "B", "A", "C", "B", "A", "C", "B", "A", "C",
    "B", "A", "C", "B", "A", "C", "B", "A", "C", "B",
    "A", "C", "B", "A", "C", "B", "A", "C", "B", "A"
]



count_A = three_12.count('A')
count_B = three_12.count('B')
#17,16,17
#https://chat.openai.com/share/a3327fc1-a1bb-447d-8585-42ad4cb211ea

three_13 = [
    "C", "A", "B", "C", "B", "C", "A", "C", "B", "A",
    "B", "C", "A", "B", "C", "A", "C", "B", "A", "B",
    "C", "A", "B", "C", "A", "B", "C", "A", "B", "C",
    "A", "B", "C", "A", "B", "C", "A", "B", "C", "A",
    "B", "C", "A", "B", "C", "A", "B", "C", "A", "B"
]




count_A = three_13.count('A')
count_B = three_13.count('B')
#16,17,17
#https://chat.openai.com/share/a97c3c09-48e1-49f4-9d6b-6a74bbe0b22e


three_14 = ['C', 'B', 'C', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A']





count_A = three_14.count('A')
count_B = three_14.count('B')
#16,17,17
#https://chat.openai.com/share/018d8d6d-6516-4e3d-90ac-e170d28550ac


three_15 = [
    "A", "C", "B", "C", "B", "A", "C", "B", "A", "B",
    "C", "A", "B", "C", "A", "B", "A", "C", "B", "A",
    "C", "B", "A", "B", "C", "A", "B", "C", "A", "B",
    "A", "C", "B", "A", "C", "B", "A", "C", "B", "A",
    "C", "B", "A", "B", "C", "A", "B", "C", "A", "B"
]


count_A = three_15.count('A')
count_B = three_15.count('B')
#17,18,15
#https://chat.openai.com/share/f033073e-79bd-4cc0-934b-a81a64381fea

three_16 = [
    'C', 'B', 'C', 'B', 'B', 'A', 'A', 'C', 'B', 'C', # Entries 1 to 10
    'A', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', # Entries 11 to 20
    'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', # Entries 21 to 30
    'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', # Entries 31 to 40
    'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C'  # Entries 41 to 50
]



count_A = three_16.count('A')
count_B = three_16.count('B')
#16,17,17
#https://chat.openai.com/share/2e355791-7953-49e0-9212-b23cf193bc4d

three_17 = [
    'C', 'A', 'C', 'B', 'B', 'A', 'B', 'C', 'A', 'B',
    'C', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A',
    'C', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B',
    'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C',
    'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A'
]



count_A = three_17.count('A')
count_B = three_17.count('B')
#17,17,16
#https://chat.openai.com/share/7bca2ecc-4c46-402d-87a3-c251bf1fd9c3


three_18 = results = ['B', 'C', 'C', 'B', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A']



count_A = three_18.count('A')
count_B = three_18.count('B')
#15,18,17
#https://chat.openai.com/share/70529ead-f84a-48e9-9c0d-6e2d2535c4f7

three_19 = [
    'B', 'B', 'C', 'B', 'B', 'B', 'C', 'A', 'C', 'A',
    'C', 'A', 'B', 'C', 'A', 'B', 'A', 'B', 'C', 'A',
    'B', 'B', 'C', 'B', 'A', 'C', 'B', 'C', 'A', 'C',
    'B', 'C', 'A', 'B', 'A', 'B', 'C', 'A', 'B', 'C',
    'A', 'C', 'B', 'B', 'A', 'C', 'B', 'B', 'C', 'A'
]


count_A = three_19.count('A')
count_B = three_19.count('B')
#14,20,16
#https://chat.openai.com/share/7bca2ecc-4c46-402d-87a3-c251bf1fd9c3


three_20  = ['B', 'B', 'B', 'A', 'B', 'C', 'A', 'C', 'A', 'A', 'B', 'B', 'C', 'B', 'A', 'B']




count_A = three_20.count('A')
count_B = three_20.count('B')

#https://chat.openai.com/share/d2477a06-2a26-494c-8a0b-e008b18af905

all_threes=[]

for i in range(1, 22):
    list_name = f'three_{i}'
    print(list_name)
    current_list = globals().get(list_name, [])
    all_threes.extend(current_list)
count_A = all_threes.count('A')
count_B = all_threes.count('B')
count_C = all_threes.count('C')



df =pd.read_csv('LetAIEntertainYou/Posts/llama_und_base_unbloat.csv',delimiter=';')
df['judgement'] = all_singles
df.to_csv('LetAIEntertainYou/Posts/llama_und_base_judged.csv', sep=';',index=False)
