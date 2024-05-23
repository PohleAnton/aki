'''
enthält einges zum erzeugen der notwendigen datensätze und vor allem das ergebnis des abc verlgeichs von gpt4
'''


import csv
import os
import csv

import pandas as pd
os.getcwd()
input_file='LetAIEntertainYou/data/posts_best_of_n_complete_with_target.csv'
output_file='LetAIEntertainYou/data/posts_best_of_n_complete_targets.csv'
target_columns = []
df = pd.read_csv(input_file, delimiter=';')

# Extract the correct subject lines based on the "Target" column for each row
target_columns = []
for index, row in df.iterrows():
    target = row['Target']
    subject_line = row[f'Subject Line {target}']
    target_columns.append(subject_line)

# Create a new dataframe with the target columns
target_df = pd.DataFrame(target_columns, columns=['Target Column'])
target_df = target_df.applymap(lambda x: x.lstrip() if isinstance(x, str) else x)

# Save the new dataframe to a CSV file

target_df.to_csv(output_file, index=False)

full='LetAIEntertainYou/data/posts_rules_base_n.csv'
df = pd.read_csv(full,delimiter=';')
rows_per_chunk = 100
out_dir='LetAIEntertainYou/data/chunks/n/'
# Get the header
header = df.columns

# Split the dataframe into chunks and save each chunk to a new CSV file
for i in range(0, len(df), rows_per_chunk):
    chunk = df.iloc[i:i + rows_per_chunk]
    chunk_file_path = os.path.join(out_dir, f'chunk_{i // rows_per_chunk + 1}.csv')


    # Save the chunk to a CSV file
    chunk.to_csv(chunk_file_path, sep=';',index=False, header=header)

print("CSV file has been split and saved successfully.")


promp='''imagine the following scenario:
on a neighborhood social media plattform, users can create all kinds of posts.
some user will activate email notification, meaning they get an email every time a post for their neighborhood is posted.
for this email, we will need a subject line that catches the users interest, meaning he clicks on the email.
this file contains 100 rows with 3 different versions for an email subject line generated from a post on a social media plattform

use this code to render the file so you can read all the data

import pandas as pd

# Load the data from the provided file
file_path = f'/mnt/data/{filename}'
data = pd.read_csv(file_path, delimiter=';', encoding='iso-8859-1')

# Display the entire dataframe
data



your task is:
1. you asses which subject line is more likely to generate a click
2. evaluate like a human would, so don't write code or apply any patterns.
3. focus on factors like: Relevance and Specificity, Clarity and Directness, Urgency, Benefit or Offer, Emotional Engagement, Curiosity and Intrigue, Personalization
4. Provide a judgement for every tripplet in the file. the file contains 100 tripplets - so i need exactly 100 judgements
5. i only need your answer for each tripplet - so something like 'C', 'A','B' without explanation
6. provide your result like a python list'''



'''
hier beginnt der abc vergleich von gpt4

'''

singles_1=['B', 'A', 'A', 'B', 'C', 'C', 'B', 'B', 'B', 'C', 'C', 'A', 'A', 'C', 'C', 'C', 'A', 'B', 'B', 'C', 'B', 'B', 'A', 'B', 'B', 'C', 'A', 'B', 'A', 'B', 'A', 'C', 'A', 'B', 'C', 'B', 'B', 'A', 'A', 'B', 'C', 'A', 'A', 'B', 'B', 'A', 'C', 'A', 'B', 'B', 'A', 'C', 'A', 'C', 'B', 'B', 'B', 'A', 'C', 'A', 'A', 'C', 'C', 'B', 'A', 'A', 'C', 'A', 'B', 'B', 'C', 'C', 'A', 'B', 'A', 'A', 'C', 'C', 'A', 'C', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'B', 'A', 'C', 'A', 'B', 'B', 'A', 'B', 'B', 'B', 'C', 'A', 'C']

#https://chatgpt.com/share/239296b5-23c2-41f2-afe8-e2a0d6ccfe2e


print(len(singles_1))
count_A_1 = singles_1.count('A')
count_B_1 = singles_1.count('B')
count_C_1 = singles_1.count('C')

singles_2= [
    'B', 'C', 'B', 'B', 'B', 'A', 'B', 'B', 'B', 'A',
    'B', 'B', 'C', 'C', 'A', 'C', 'A', 'A', 'B', 'C',
    'C', 'A', 'C', 'C', 'B', 'B', 'A', 'A', 'A', 'C',
    'B', 'A', 'C', 'B', 'B', 'A', 'A', 'B', 'C', 'B',
    'C', 'B', 'B', 'C', 'B', 'B', 'C', 'A', 'B', 'A',
    'B', 'C', 'A', 'B', 'B', 'C', 'B', 'C', 'C', 'A',
    'C', 'C', 'B', 'A', 'C', 'C', 'A', 'B', 'B', 'C',
    'B', 'C', 'A', 'B', 'C', 'A', 'C', 'B', 'A', 'A',
    'C', 'A', 'A', 'B', 'A', 'A', 'B', 'A', 'C', 'A',
    'C', 'B', 'C', 'B', 'B', 'B', 'B', 'A', 'A', 'B'
]
#https://chatgpt.com/share/bb73c29f-df76-4f8f-8122-6573a074fadb
print(len(singles_2))
count_A_2 = singles_2.count('A')
count_B_2 = singles_2.count('B')
count_C_2 = singles_2.count('C')

singles_3= ['C', 'A', 'C', 'C', 'C', 'C', 'B', 'B', 'C', 'A', 'B', 'B', 'A', 'C', 'B', 'A', 'A', 'C', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'A', 'C', 'B', 'B', 'B', 'C', 'A', 'A', 'B', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'C', 'C', 'A', 'C', 'C', 'B', 'B', 'C', 'A', 'A', 'C', 'A', 'C', 'A', 'C', 'C', 'A', 'A', 'A', 'A', 'C', 'C', 'B', 'B', 'C', 'A', 'B', 'C', 'C', 'C', 'B', 'A', 'A', 'A', 'A', 'C', 'B', 'B', 'A', 'C', 'C', 'B', 'B', 'A', 'B', 'A', 'A', 'A', 'B', 'A', 'C', 'B', 'A', 'A', 'B', 'A', 'C', 'C', 'C']


#https://chatgpt.com/share/9cfa46ac-a26d-4e43-bb31-3ab6c5ad08ce
print(len(singles_3))
count_A_3 = singles_3.count('A')
count_B_3 = singles_3.count('B')
count_C_3 = singles_3.count('C')


singles_4= [
    'C', 'B', 'B', 'A', 'C', # Subject lines 1-5
    'A', 'C', 'B', 'B', 'C', # Subject lines 6-10
    'B', 'C', 'A', 'A', 'A', # Subject lines 11-15
    'C', 'B', 'C', 'A', 'B', # Subject lines 16-20
    'A', 'A', 'B', 'C', 'B', # Subject lines 21-25
    'C', 'A', 'A', 'B', 'A', # Subject lines 26-30
    'C', 'B', 'C', 'C', 'A', # Subject lines 31-35
    'B', 'B', 'B', 'C', 'A', # Subject lines 36-40
    'A', 'C', 'B', 'A', 'A', # Subject lines 41-45
    'B', 'C', 'A', 'B', 'C', # Subject lines 46-50
    'A', 'C', 'B', 'B', 'A', # Subject lines 51-55
    'B', 'B', 'C', 'A', 'A', # Subject lines 56-60
    'C', 'C', 'A', 'B', 'B', # Subject lines 61-65
    'A', 'B', 'A', 'C', 'C', # Subject lines 66-70
    'B', 'C', 'B', 'C', 'B', # Subject lines 71-75
    'A', 'A', 'B', 'B', 'C', # Subject lines 76-80
    'B', 'A', 'A', 'B', 'B', # Subject lines 81-85
    'C', 'A', 'A', 'C', 'B', # Subject lines 86-90
    'C', 'A', 'C', 'C', 'B', # Subject lines 91-95
    'C', 'B', 'C', 'A', 'A'  # Subject lines 96-100
]

#https://chatgpt.com/share/e35a538f-494f-4add-a663-e362e68dce8d
print(len(singles_4))
count_A_4 = singles_4.count('A')
count_B_4 = singles_4.count('B')
count_C_4 = singles_4.count('C')


singles_5=['A', 'A', 'B', 'A', 'A', 'A', 'A', 'B', 'A', 'A',
 'C', 'B', 'A', 'A', 'A', 'A', 'A', 'B', 'C', 'B',
 'C', 'B', 'A', 'B', 'A', 'C', 'C', 'C', 'B', 'C',
 'A', 'C', 'B', 'C', 'C', 'A', 'A', 'B', 'C', 'B',
 'B', 'B', 'A', 'B', 'B', 'C', 'B', 'B', 'C', 'A',
 'C', 'A', 'B', 'A', 'C', 'A', 'C', 'A', 'B', 'B',
 'C', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'B', 'B',
 'C', 'C', 'C', 'A', 'B', 'B', 'C', 'C', 'B', 'C',
 'C', 'A', 'B', 'A', 'B', 'A', 'C', 'A', 'A', 'A',
 'B', 'B', 'C', 'B', 'B', 'B', 'C', 'C', 'C', 'A']


#https://chatgpt.com/share/34e8d90d-60c5-4b55-8168-9d31bd5f6c9e
print(len(singles_5))
count_A_5 = singles_5.count('A')
count_B_5 = singles_5.count('B')
count_C_5 = singles_5.count('C')


singles_6=[
    "B", "B", "C", "B", "C", "C", "B", "B", "A", "B",
    "C", "B", "A", "A", "A", "A", "C", "C", "C", "B",
    "B", "B", "B", "B", "A", "C", "C", "B", "B", "B",
    "B", "B", "C", "B", "C", "B", "A", "A", "A", "B",
    "B", "B", "C", "C", "B", "A", "C", "B", "B", "B",
    "B", "B", "C", "B", "C", "B", "C", "A", "C", "C",
    "B", "C", "B", "A", "B", "B", "A", "B", "A", "B",
    "C", "C", "A", "C", "B", "A", "B", "B", "C", "C",
    "B", "A", "C", "C", "A", "A", "C", "A", "B", "C",
    "B", "B", "A", "B", "C", "C", "B", "C", "A", "B"
]
#https://chatgpt.com/share/40fbc34c-e48f-414f-b897-f570c17a4a1a
print(len(singles_6))
count_A_6 = singles_6.count('A')
count_B_6 = singles_6.count('B')
count_C_6 = singles_6.count('C')


singles_7=['C', 'C', 'B', 'B', 'B', 'C', 'A', 'C', 'A', 'B', 'B', 'C', 'C', 'C', 'B', 'B', 'C', 'C', 'B', 'A',
             'A', 'C', 'A', 'A', 'A', 'A', 'A', 'C', 'B', 'C', 'C', 'A', 'A', 'C', 'B', 'A', 'C', 'B', 'B', 'A',
             'B', 'B', 'B', 'C', 'B', 'C', 'C', 'A', 'A', 'C', 'C', 'C', 'A', 'B', 'A', 'A', 'B', 'A', 'B', 'C',
             'B', 'A', 'C', 'C', 'B', 'C', 'C', 'A', 'B', 'C', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'A',
             'B', 'A', 'C', 'C', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'C', 'A', 'A', 'B', 'B', 'C', 'A', 'B', 'A',
]
#https://chatgpt.com/share/3d998253-9931-421b-89e2-088d0a948fb7
print(len(singles_7))
count_A_7 = singles_7.count('A')
count_B_7 = singles_7.count('B')
count_C_7 = singles_7.count('C')



singles_8=['B', 'B', 'C', 'B', 'A', 'A', 'B', 'A', 'A', 'A',
           'B', 'C', 'A', 'A', 'C', 'C', 'A', 'C', 'A', 'B',
           'C', 'A', 'C', 'B', 'A', 'B', 'A', 'B', 'A', 'A',
           'B', 'A', 'C', 'A', 'B', 'A', 'B', 'A', 'A', 'B',
           'C', 'C', 'C', 'B', 'A', 'C', 'B', 'B', 'A', 'B',
           'B', 'C', 'B', 'B', 'A', 'A', 'C', 'B', 'B', 'B',
           'C', 'A', 'C', 'A', 'B', 'B', 'A', 'A', 'C', 'C',
           'B', 'C', 'B', 'C', 'A', 'A', 'B', 'A', 'B', 'C',
           'C', 'B', 'B', 'B', 'A', 'A', 'B', 'C', 'B', 'A',
           'C', 'A', 'C', 'C', 'C', 'B', 'C', 'A', 'B', 'B']
#https://chatgpt.com/share/b95a206c-6593-4009-9779-71f997dab41b
print(len(singles_8))
count_A_8 = singles_8.count('A')
count_B_8 = singles_8.count('B')
count_C_8 = singles_8.count('C')


singles_9=['A', 'C', 'B', 'A', 'A', 'A', 'C', 'B', 'C', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'B', 'A', 'C', 'A', 'B', 'A', 'C', 'A', 'B', 'A', 'C', 'B', 'C', 'B', 'A', 'A', 'B', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A']

#https://chatgpt.com/share/6c79f09c-027b-4c80-a090-da0d77ad6eaa
print(len(singles_9))
count_A_9 = singles_9.count('A')
count_B_9 = singles_9.count('B')
count_C_9 = singles_9.count('C')


singles_10=[
    'B', 'C', 'C', 'A', 'C', 'C', 'C', 'B', 'A', 'C',
    'B', 'A', 'C', 'B', 'C', 'B', 'C', 'A', 'C', 'C',
    'C', 'C', 'B', 'C', 'B', 'B', 'C', 'C', 'B', 'A',
    'A', 'C', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'B',
    'B', 'C', 'B', 'A', 'B', 'B', 'A', 'A', 'C', 'C',
    'C', 'C', 'B', 'C', 'B', 'B', 'C', 'C', 'B', 'A',
    'A', 'C', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'B',
    'B', 'C', 'B', 'A', 'B', 'B', 'A', 'A', 'C', 'C',
    'C', 'C', 'B', 'C', 'B', 'B', 'C', 'C', 'B', 'A',
    'A', 'C', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'B'
]
#https://chatgpt.com/share/6c79f09c-027b-4c80-a090-da0d77ad6eaa
print(len(singles_10))
count_A_10 = singles_10.count('A')
count_B_10 = singles_10.count('B')
count_C_10 = singles_10.count('C')


singles_11= [
    'A', 'A', 'A', 'C', 'A',
    'A', 'C', 'C', 'C', 'A',
    'A', 'A', 'C', 'A', 'C',
    'A', 'C', 'A', 'B', 'A',
    'C', 'A', 'C', 'A', 'B',
    'A', 'B', 'C', 'A', 'A',
    'A', 'C', 'B', 'A', 'C',
    'A', 'B', 'A', 'B', 'C',
    'A', 'C', 'B', 'A', 'A',
    'A', 'C', 'A', 'C', 'A',
    'B', 'A', 'A', 'C', 'A',
    'A', 'A', 'A', 'B', 'B',
    'B', 'A', 'C', 'A', 'A',
    'C', 'B', 'B', 'B', 'A',
    'A', 'A', 'B', 'C', 'A',
    'B', 'C', 'B', 'C', 'B',
    'A', 'A', 'C', 'C', 'A',
    'B', 'C', 'A', 'B', 'C',
    'A', 'C', 'B', 'A', 'A',
    'A', 'A', 'A', 'C', 'A'
]
#https://chatgpt.com/share/457e7835-6e03-4953-81a9-94e17bead735
print(len(singles_11))
count_A_11 = singles_11.count('A')
count_B_11 = singles_11.count('B')
count_C_11 = singles_11.count('C')



singles_12=['B', 'A', 'C', 'A', 'C', 'C', 'C', 'A', 'C', 'B', 'B', 'B', 'A', 'B', 'A', 'C', 'B', 'C', 'A', 'C', 'B', 'B', 'A', 'A', 'B', 'B', 'C', 'B', 'B', 'A', 'C', 'A', 'B', 'C', 'B', 'C', 'B', 'B', 'A', 'A', 'C', 'C', 'A', 'B', 'B', 'A', 'B', 'C', 'A', 'A', 'A', 'B', 'C', 'A', 'C', 'B', 'B', 'B', 'C', 'A', 'C', 'C', 'A', 'A', 'B', 'C', 'C', 'B', 'A', 'B', 'A', 'A', 'C', 'B', 'A', 'A', 'B', 'A', 'B', 'C', 'B', 'C', 'C', 'C', 'C', 'A', 'B', 'B', 'A', 'C', 'C', 'B', 'B', 'C', 'A', 'C', 'B', 'B', 'C',  'C']

#https://chatgpt.com/share/6c4387c8-c4e6-4a83-a0f6-57f17d658a6f
print(len(singles_12))
count_A_12 = singles_12.count('A')
count_B_12 = singles_12.count('B')
count_C_12 = singles_12.count('C')



singles_13=[
    'B', 'A', 'C', 'A', 'A',
    'A', 'A', 'C', 'C', 'C',
    'C', 'B', 'A', 'C', 'A',
    'C', 'A', 'B', 'B', 'A',
    'A', 'A', 'B', 'A', 'B',
    'B', 'C', 'C', 'A', 'B',
    'B', 'A', 'A', 'C', 'C',
    'A', 'A', 'B', 'C', 'C',
    'B', 'C', 'C', 'C', 'A',
    'A', 'A', 'B', 'B', 'C',
    'A', 'B', 'C', 'A', 'C',
    'C', 'A', 'C', 'C', 'A',
    'C', 'C', 'A', 'A', 'A',
    'B', 'C', 'C', 'B', 'C',
    'A', 'A', 'B', 'B', 'C',
    'A', 'B', 'B', 'C', 'C',
    'A', 'A', 'C', 'A', 'C',
    'A', 'B', 'C', 'A', 'C',
    'B', 'A', 'B', 'C', 'A',
    'B', 'A', 'B', 'A', 'A'
]
#https://chatgpt.com/share/c8803275-6390-465d-b9a0-fa974496e208
print(len(singles_13))
count_A_13 = singles_13.count('A')
count_B_13 = singles_13.count('B')
count_C_13 = singles_13.count('C')


singles_14=['C', 'B', 'C', 'A', 'B', 'B', 'C', 'A', 'C', 'B', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'A',
 'B', 'B', 'B', 'C', 'A', 'B', 'A', 'C', 'A', 'B', 'C', 'C', 'A', 'B', 'C', 'A', 'C', 'B', 'A', 'C',
 'A', 'C', 'B', 'B', 'B', 'A', 'A', 'C', 'B', 'B', 'A', 'B', 'A', 'B', 'C', 'B', 'B', 'B', 'B', 'A',
 'C', 'C', 'B', 'A', 'A', 'C', 'A', 'A', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A', 'B', 'B', 'C', 'B',
 'A', 'A', 'C', 'C', 'C', 'B', 'A', 'C', 'A', 'C', 'B', 'A', 'B', 'C', 'C', 'B', 'C', 'B', 'B', 'C']

#https://chatgpt.com/share/dcfac33a-5117-4dee-ac0d-1a53d2bc0958
print(len(singles_14))
count_A_14 = singles_14.count('A')
count_B_14 = singles_14.count('B')
count_C_14 = singles_14.count('C')




singles_15=[
    'C', 'B', 'B', 'A', 'B', # 1-5
    'A', 'C', 'B', 'A', 'A', # 6-10
    'C', 'B', 'A', 'C', 'C', # 11-15
    'B', 'A', 'A', 'B', 'B', # 16-20
    'C', 'A', 'B', 'C', 'A', # 21-25
    'B', 'C', 'B', 'A', 'B', # 26-30
    'A', 'C', 'A', 'B', 'C', # 31-35
    'A', 'B', 'C', 'A', 'A', # 36-40
    'B', 'C', 'A', 'B', 'C', # 41-45
    'B', 'A', 'C', 'B', 'A', # 46-50
    'C', 'B', 'A', 'C', 'B', # 51-55
    'A', 'C', 'B', 'A', 'C', # 56-60
    'B', 'A', 'C', 'B', 'A', # 61-65
    'C', 'B', 'A', 'C', 'B', # 66-70
    'A', 'C', 'B', 'A', 'C', # 71-75
    'B', 'A', 'C', 'B', 'A', # 76-80
    'C', 'B', 'A', 'C', 'B', # 81-85
    'A', 'C', 'B', 'A', 'C', # 86-90
    'B', 'A', 'C', 'B', 'A', # 91-95
    'C', 'B', 'A', 'C', 'B'  # 96-100
]
#https://chatgpt.com/share/959a1908-2839-482a-8327-835db25a39a7
print(len(singles_15))
count_A_15 = singles_15.count('A')
count_B_15 = singles_15.count('B')
count_C_15 = singles_15.count('C')



singles_16=[
    'A', 'B', 'C', 'C', 'A',
    'B', 'A', 'B', 'C', 'C',
    'A', 'C', 'A', 'B', 'C',
    'A', 'B', 'A', 'B', 'A',
    'B', 'A', 'C', 'C', 'B',
    'A', 'B', 'C', 'A', 'B',
    'C', 'A', 'B', 'C', 'A',
    'B', 'C', 'A', 'B', 'C',
    'A', 'B', 'C', 'A', 'B',
    'C', 'A', 'B', 'C', 'A',
    'B', 'C', 'A', 'B', 'C',
    'A', 'B', 'C', 'A', 'B',
    'C', 'A', 'B', 'C', 'A',
    'B', 'C', 'A', 'B', 'C',
    'A', 'B', 'C', 'A', 'B',
    'C', 'A', 'B', 'C', 'A',
    'B', 'C', 'A', 'B', 'C',
    'A', 'B', 'C', 'A', 'B',
    'C', 'A', 'B', 'C', 'A',
    'B', 'C', 'A', 'B', 'C'
]
#https://chatgpt.com/share/8b0b1c68-48be-4919-b43d-fd4a0970e5a7
print(len(singles_16))
count_A_16 = singles_16.count('A')
count_B_16 = singles_16.count('B')
count_C_16 = singles_16.count('C')



singles_17=['A', 'B', 'C', 'A', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'B', 'B', 'C', 'A', 'B', 'C', 'B', 'A', 'C', 'A', 'C', 'B', 'B', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A']

#https://chatgpt.com/share/4d0f456e-9c5c-4609-b28a-01afaa56d960
print(len(singles_17))
count_A_17 = singles_17.count('A')
count_B_17 = singles_17.count('B')
count_C_17 = singles_17.count('C')



singles_18=[
    'A', 'B', 'C', 'A', 'B',
    'A', 'B', 'A', 'B', 'B',
    'A', 'A', 'C', 'A', 'B',
    'A', 'B', 'C', 'A', 'B',
    'A', 'B', 'A', 'A', 'B',
    'C', 'A', 'B', 'A', 'B',
    'A', 'B', 'B', 'A', 'C',
    'B', 'B', 'C', 'A', 'C',
    'B', 'A', 'A', 'B', 'A',
    'B', 'A', 'B', 'B', 'A',
    'B', 'B', 'A', 'A', 'C',
    'B', 'A', 'B', 'A', 'B',
    'A', 'B', 'B', 'A', 'B',
    'A', 'A', 'B', 'B', 'B',
    'A', 'C', 'A', 'B', 'A',
    'B', 'C', 'B', 'B', 'A',
    'B', 'A', 'C', 'B', 'B',
    'A', 'A', 'B', 'B', 'A',
    'C', 'B', 'B', 'A', 'B',
    'B', 'A', 'B', 'C', 'B'
]
#https://chatgpt.com/share/4cc496d8-ca1d-4860-8cce-f71c0e386eb5
print(len(singles_18))
count_A_18 = singles_18.count('A')
count_B_18 = singles_18.count('B')
count_C_18 = singles_18.count('C')

singles_19=[
    'C', 'B', 'A', 'A', 'B', 'B', 'A', 'C', 'C', 'B', 'A', 'B', 'C', 'B', 'C',
    'B', 'C', 'B', 'A', 'C', 'A', 'B', 'A', 'B', 'C', 'C', 'B', 'A', 'B', 'A',
    'B', 'C', 'A', 'C', 'B', 'A', 'C', 'C', 'B', 'B', 'A', 'A', 'B', 'C', 'B',
    'C', 'A', 'B', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'B', 'C', 'B', 'A',
    'C', 'B', 'C', 'A', 'A', 'B', 'C', 'A', 'B', 'B', 'A', 'C', 'B', 'C', 'A',
    'B', 'B', 'C', 'A', 'C', 'A', 'C', 'C', 'B', 'A', 'B', 'A', 'C', 'C', 'A',
    'B', 'B', 'A', 'A', 'C', 'B', 'C', 'A', 'B',  'C'
]
#https://chatgpt.com/share/bee4e2df-7141-4903-b92f-577ce887689c
print(len(singles_19))
count_A_19 = singles_19.count('A')
count_B_19 = singles_19.count('B')
count_C_19 = singles_19.count('C')



singles_20=[
    'A', 'A', 'B', 'A', 'A', 'B', 'C', 'B', 'A', 'A',
    'C', 'B', 'A', 'B', 'C', 'C', 'A', 'C', 'B', 'C',
    'B', 'A', 'B', 'A', 'A', 'B', 'A', 'C', 'B', 'B',
    'A', 'B', 'A', 'A', 'B', 'C', 'B', 'A', 'C', 'B',
    'A', 'A', 'B', 'A', 'A', 'B', 'C', 'B', 'A', 'B',
    'C', 'C', 'A', 'B', 'A', 'A', 'A', 'C', 'B', 'B',
    'A', 'C', 'A', 'C', 'A', 'A', 'A', 'C', 'B', 'A',
    'C', 'B', 'A', 'A', 'A', 'C', 'B', 'B', 'A', 'A',
    'B', 'B', 'C', 'B', 'B', 'A', 'A', 'B', 'B', 'C',
    'B', 'A', 'C', 'B', 'A', 'A', 'B', 'C', 'A', 'C'
]
#https://chatgpt.com/share/5cfe4d4b-d4a9-4371-9c29-17f1c9d77bb6
print(len(singles_20))
count_A_20 = singles_20.count('A')
count_B_20 = singles_20.count('B')
count_C_20 = singles_20.count('C')


singles_21=['C', 'A', 'A', 'B', 'C',  'A', 'C', 'A', 'B', 'A', 'C', 'B', 'C', 'B', 'C', 'A', 'C', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C']

#https://chatgpt.com/share/b7955b82-024e-43ff-8a4d-590697f8c2b9
print(len(singles_21))
count_A_21 = singles_21.count('A')
count_B_21 = singles_21.count('B')
count_C_21 = singles_21.count('C')


singles_22=[
    'A', 'B', 'A', 'C', 'A', 'A', 'C', 'B', 'B', 'C',
    'A', 'A', 'B', 'B', 'A', 'B', 'A', 'A', 'B', 'B',
    'C', 'B', 'A', 'B', 'A', 'C', 'B', 'B', 'A', 'B',
    'C', 'C', 'B', 'B', 'B', 'B', 'A', 'B', 'C', 'C',
    'A', 'A', 'A', 'B', 'B', 'C', 'C', 'B', 'A', 'C',
    'B', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'B', 'B',
    'A', 'B', 'A', 'A', 'B', 'C', 'C', 'B', 'A', 'A',
    'C', 'A', 'C', 'B', 'B', 'B', 'A', 'A', 'A', 'C',
    'C', 'C', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'B',
    'C', 'B', 'A', 'C', 'C', 'B', 'C', 'B', 'A', 'B'
]
#https://chatgpt.com/share/83117f30-8c55-4656-a03f-88532d947802
print(len(singles_22))
count_A_22 = singles_22.count('A')
count_B_22 = singles_22.count('B')
count_C_22 = singles_22.count('C')



singles_23=['C', 'A', 'B', 'A', 'B', 'A', 'B', 'C', 'A', 'C', 'A', 'B', 'C', 'B', 'A', 'B', 'C', 'B', 'A', 'C',
 'B', 'A', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A',
 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C',
 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A',  'C', 'A', 'B', 'C']


#https://chatgpt.com/share/dcf4d16f-bb09-45ce-ad11-fd63f666ab9e
print(len(singles_23))
count_A_23 = singles_23.count('A')
count_B_23 = singles_23.count('B')
count_C_23 = singles_23.count('C')




singles_24= [
    'A', 'B', 'A', 'A', 'B', 'A', 'B', 'B', 'C', 'B',
    'C', 'A', 'A', 'A', 'B', 'C', 'C', 'B', 'B', 'A',
    'C', 'A', 'B', 'C', 'A', 'C', 'C', 'A', 'A', 'B',
    'C', 'B', 'C', 'B', 'A', 'B', 'B', 'C', 'A', 'B',
    'A', 'B', 'C', 'A', 'C', 'C', 'B', 'B', 'A', 'B',
    'B', 'C', 'B', 'A', 'C', 'A', 'B', 'A', 'A', 'C',
    'A', 'C', 'B', 'B', 'B', 'C', 'A', 'B', 'A', 'C',
    'A', 'C', 'C', 'B', 'A', 'B', 'C', 'B', 'C', 'C',
    'B', 'C', 'A', 'A', 'A', 'C', 'A', 'C', 'B', 'A',
    'A', 'B', 'A', 'B', 'B', 'C', 'B', 'B', 'A', 'A'
]


#https://chatgpt.com/share/57864155-dfc7-4229-a399-44d012d0917f
print(len(singles_24))
count_A_24 = singles_24.count('A')
count_B_24 = singles_24.count('B')
count_C_24 = singles_24.count('C')


singles_25=['C', 'B', 'B', 'A', 'A', 'B', 'A', 'C', 'A', 'B',
              'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'A',
              'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
              'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C',
              'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A',
              'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
              'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C',
              'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A',
              'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B',
              'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C']


#https://chatgpt.com/share/a4d1ea9a-823d-4582-a0c3-115a555eb28b
print(len(singles_25))
count_A_25 = singles_25.count('A')
count_B_25 = singles_25.count('B')
count_C_25 = singles_25.count('C')



singles_26=['A', 'B', 'A', 'C', 'B', 'A', 'A', 'C', 'C',  'A', 'B', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'B', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'A', 'B', 'A', 'A', 'B', 'B', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'B']



#https://chatgpt.com/share/10c756ff-971c-4490-98e5-871ddc1a3a9b
print(len(singles_26))
count_A_26 = singles_26.count('A')
count_B_26 = singles_26.count('B')
count_C_26 = singles_26.count('C')



singles_27= [
    'B', 'A', 'C', 'A', 'B', 'B', 'C', 'A', 'C', 'B', 'C', 'B', 'A', 'C', 'A',
    'B', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'A', 'B', 'B', 'C', 'B', 'A', 'C',
    'A', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'B', 'A', 'C', 'B', 'A', 'C',
    'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A', 'C', 'A', 'B', 'C', 'A',
    'B', 'A', 'C', 'A', 'B', 'C', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'B', 'A',
    'C', 'A', 'B', 'C', 'A', 'B', 'A', 'C', 'B', 'A', 'C', 'B', 'A', 'C', 'B',
    'C', 'A', 'B', 'C', 'A', 'B', 'C', 'B', 'A', 'C'
]


#https://chatgpt.com/share/12a82263-2193-462b-a644-c743fb3d0957
print(len(singles_27))
count_A_27 = singles_27.count('A')
count_B_27 = singles_27.count('B')
count_C_27 = singles_27.count('C')

all_singles = []
for i in range(1,28):
    all_singles.extend(locals()[f'singles_{i}'])
csv_filename = "./merged_singles.csv"

# Write the list to a CSV file
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["String"])  # Write header
    for single in all_singles:
        writer.writerow([single])

count_A = all_singles.count('A')
count_B = all_singles.count('B')
count_C = all_singles.count('C')
#a:958 - 36,48 %
#b951 - 35,22 %
#791 -29,9%
