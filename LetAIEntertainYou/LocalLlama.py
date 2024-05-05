import openai
import csv
import random

openai.api_key = "EMPTY"
openai.base_url = "http://localhost:8000/v1/"

model = "vicuna-7b-v1.5"

filename = './LetAIEntertainYou/Posts/posts.csv'
liste = []
with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        liste.append(row[0])


llama2_posts=[]

for i in range(0, 5):
    liste_small = random.sample(liste, 5)
    provided_string = "\n".join(f" {i + 1}. {entry}" for i, entry in enumerate(liste_small))
    prompt = f"Write a single post with a structure very similar to the examples provided in {provided_string}. Only write the post without any explanation"

    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    llama2_posts.append(completion.choices[0].message.content)
# print the completion
#print(completion.choices[0].message.content)


