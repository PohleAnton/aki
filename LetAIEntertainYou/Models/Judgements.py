import json

import pandas as pd
import openai
import yaml

singles_1=[
    "B", "B", "A", "B", "A", "A", "B", "B", "A", "A", "B", "A", "B", "B", "A",
    "B", "B", "A", "B", "A", "B", "B", "A", "B", "A", "B", "B", "A", "B", "A",
    "B", "B", "A", "B", "A", "B", "B", "A", "B", "A", "B", "B", "A", "B", "A",
    "B", "B", "A", "B", "A", "B", "B", "A", "B", "A", "B", "B", "A", "B", "A",
    "B", "B", "A", "B", "A", "B", "B", "A", "B", "A", "B", "B", "A", "B", "A",
    "B", "B", "A", "B", "A", "B", "B", "A", "B", "A", "B", "B", "A", "B", "A",
    "B", "B", "A", "B", "A", "B", "B", "A", "B", "A", "B", "B", "A", "B", "A",
    "B", "B", "A", "B", "A", "B", "B", "A", "B", "A", "B", "B", "A", "B", "A"
]
print(len(singles_1))
count_A_1 = singles_1.count('A')
#https://chat.openai.com/share/a1c88486-9b0e-4a1a-83fa-a34acd9de4e4



df=pd.read_csv('LetAIEntertainYou/Posts/current/chunks/reverse_fullprompt/output_2.csv', sep=';', encoding='iso-8859-1')



functions = [
    {
        "name": "compare_subject_lines",
        "description": "A function asses which subject line is more engaging, meaning a user is more likely to click on: subject_line_a or subject_line_b. it evaluates like a human would and focuses on on factors like engagement, specificity, urgency, and relevance",
        "parameters": {
            "type": "object",
            "properties": {
                "letter": {
                    "type": "string",
                    "description": "the letter of the winning subject line, 'A' or 'B' only"
                }
            },
            "required": ["subject_line_a", "subject_line_b",'letter']
        }
        }
    ]

openai.api_key = yaml.safe_load(open("./LetAIEntertainYou/config.yml")).get('KEYS', {}).get('openai')
list_neu=[]
for r in df.values:
    print(r[0])
    subject_line_a =r[0]
    subject_line_b =r[1]
    response = openai.ChatCompletion.create(
        model='gpt-4-turbo',
        messages=[
            {'role': 'user',
            'content': f"compare_subject_lines {subject_line_a} and {subject_line_b}"}
             ],
             functions=functions,
             function_call={'name': 'compare_subject_lines'}
         )
    output = json.loads(response['choices'][0]['message']['function_call']['arguments'])
    try:
        letter = output['letter']
    except:
        print(output)
    print(letter)
    list_neu.append(letter)
print('fertig')

asa=0
for str in list_neu:
    if 'A' in str:
        asa=asa+1

