import openai
import yaml
import json
import csv
import random
import copy
import pandas as pd
import os



openai.api_key = yaml.safe_load(open("./LetAIEntertainYou/config.yml")).get('KEYS', {}).get('openai')
model_dev = 'gpt-3.5-turbo-0125'
model = 'gpt-4-turbo-2024-04-09'

filename = './LetAIEntertainYou/Posts/posts.csv'
liste = []
generated = []
generated_dev=[]
with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        liste.append(row[0])

liste_small = random.sample(liste, 10)
provided_string = "\n".join(f" {i + 1}. {entry}" for i, entry in enumerate(liste_small))

set_of_instruction = """
1. Extract the phrase as-is. Do not change any single character.
2. Do not paraphrase. Copy the exact phrase. If the phrase you selected has stop words like "but", "and", "the", keep
them in the output.
3. Do not insert or remove any word.
3. If you cannot choose the most interesting phrase, summarize.
5. Try to keep it within 10 words. If you cannot complete within 10 words, generate an incomplete line with "..."
6. Put the most important words in the beginning.
7. If the first 10 words of the post contain unique and interesting words, reuse it.
8. Make a subject line that brings curiosity. If the subject line gets too long, cut the phrase before the last part. For
example, if the post has "Yesterday, my son found a dog barking at other people", output "Yesterday, my son found a
dog barking at ..."
9. If the first 10 words of the post contain informal words, you can keep these words in the subject line. We want to
respect the post content in the subject line.
10. If the post has a phrase starting with "I" in the first 10 words, please use the same words in the subject line. It will
make the subject line more personal. For example, if the post has "Hi All, I left my phone", use "I left my phone" in the
subject line.
11. If the some part of the post is all capitals, it is okay to extract that part. That part is what user wanted to emphasize.
For example, extract all capital phrases like "CRIME ALERT".
12. Do not use people’s names in the subject line.
13. Do not add "Subject line:" in the output. Just output the content of the subject line.
14. Capitalize the first character of the subject line. If the part you selected starts with a lower-cased character, capitalize
the character
"""


#um gpt3 nicht zu überfordern, zunächst 100 einträge
def split_into_lists(full_list, chunk_size=10):
    # List to store the smaller lists
    sublists = []

    # Calculate the number of full chunks
    num_full_chunks = len(full_list) // chunk_size

    # Add full chunks to sublists
    for i in range(num_full_chunks):
        start_index = i * chunk_size
        sublists.append(full_list[start_index:start_index + chunk_size])

    # Check if there's a remaining chunk to be added
    remaining_elements = len(full_list) % chunk_size
    if remaining_elements:
        sublists.append(full_list[-remaining_elements:])

    return sublists


result_lists = split_into_lists(liste)

functions = [
    {
        "name": "write_subject_lines",
        "description": "A function that outputs the most interesting phrase for every enumerated entry in a provided_string following a set_of_instruction while keeping the original order",
        "parameters": {
            "type": "object",
            "properties": {
                "subject_lines": {
                    "type": "array",
                    "description": "A list that contains the generated subject lines",
                    "items": {
                        "type": "string",
                        "description": "The generated subject line "
                    }
                }
            },
            "required": ["provided_string", "set_of_instruction"]
        }
    }
]

for i in range(34,37):
    sublist = result_lists[i]
    provided_string = "\n".join(f" {i + 1}. {entry}" for i, entry in enumerate(sublist))
    test = openai.ChatCompletion.create(
        model=model_dev,
        messages=[
            {'role': 'user',
             'content': f"write_subject_lines for every enumerated entry in  based on {provided_string}. Write according to {set_of_instruction}. Make sure the generated lines are in the same order as in provided string"}
        ],
        functions=functions,
        function_call={'name': 'write_subject_lines'}
    )
    argument_string_prod_5 = test['choices'][0]['message']['function_call']['arguments']
    data = json.loads(argument_string_prod_5)
    for subject_line in data["subject_lines"]:
        generated_dev.append(subject_line)
    print('good')
generated_dev = generated_dev[:-1]
generated_dev = generated_dev[10:]
safety = copy.deepcopy(generated_dev)
folder_path='./LetAIEntertainYou/Posts/RuleGenerated/'
output_file ="base_2.csv"

with open(output_file, 'w', newline='') as csvfile:
    csv_writer=csv.writer(csvfile)

    for item in generated_dev:
        csv_writer.writerow([item])


output_file_rules = "rules_2.csv"
data=[]
for i in range(1, 351):
        file_path = os.path.join(folder_path, f'processed_file_{i}.txt')
        print(i)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            data.append({ 'content': content})

df = pd.DataFrame(data)
print(f'DataFrame size: {df.shape}')
df.to_csv(output_file_rules, index=False)
