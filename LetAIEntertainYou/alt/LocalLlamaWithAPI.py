"""
dieses vicuna modell ist llama2 basiert, bringt eine openAI kombatible schnittstelle und unterstützt function calls
funktionert alles in allem gut, ist aber wenig performant und nur mit gewissen aufwand zu installieren
https://huggingface.co/lmsys/vicuna-7b-v1.5
es sei bemerkt, dass die browseroberflöche nicht funktioniert, alles andere aber schon.
der api dienst kann mit
python -m fastchat.serve.openai_api_server --host localhost --port 8000
gestartet werden. funktioniert für mich nur mit diesem modell: vicuna-7b-v1.5

war ein versuch, geht nur auf gpu, deswegen  nicht weiter verwendet - aber sehr cool
"""



import openai
import csv
from gpt4all import GPT4All

openai.api_key = "EMPTY"
openai.base_url = "http://localhost:8000/v1/"

model = "vicuna-7b-v1.5"

filename = './LetAIEntertainYou/Posts/current/posts_neu.csv'
liste = []
with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        liste.append(row[0])

liste.pop(0)
llama2_posts = []

set_of_instruction = """
    We will send an email containing a post from a Nextdoor user. We want to use the most interesting part of the post as an email subject line.
    Task description: Given a post, output the most interesting phrase in the post.
    Here are the requirements:
    1. Extract the phrase as-is. Do not change any single character.
    2. Do not paraphrase. Copy the exact phrase. If the phrase you selected has stop words like "but", "and", "the", keep them in the output.
    3. Do not insert or remove any word.
    4. If you cannot choose the most interesting phrase, return the first 10 words of the post.
    5. Try to keep it within 10 words. If you cannot complete within 10 words, generate an incomplete line with "..."
    6. Put the most important words in the beginning.
    7. If the first 10 words of the post contain unique and interesting words, reuse it.
    8. Make a subject line that brings curiosity. If the subject line gets too long, cut the phrase before the last part. For example, if the post has "Yesterday, my son found a dog barking at other people", output "Yesterday, my son found a dog barking at ..."
    9. If the first 10 words of the post contain informal words, you can keep these words in the subject line. We want to respect the post content in the subject line.
    10. If the post has a phrase starting with "I" in the first 10 words, please use the same words in the subject line. It will make the subject line more personal. For example, if the post has "Hi All, I left my phone", use "I left my phone" in the subject line.
    11. If the some part of the post is all capitals, it is okay to extract that part. That part is what user wanted to emphasize. For example, extract all capital phrases like "CRIME ALERT".
    12. Do not use people’s names in the subject line.
    13. Do not add "Subject line:" in the output. Just output the content of the subject line.
    14. Capitalize the first character of the subject line. If the part you selected starts with a lower-cased character, capitalize the character.
    """

for i in range(0, 2):
    row = liste[i]
    completion = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Please generate a subject line for the following post: \n\n {row} \n\n Based on the following set of rules: \n\n {set_of_instruction}",
            }
        ]
    )
    llama2_posts.append(completion.choices[0].message.content)
print(llama2_posts)
# print the completion
#print(completion.choices[0].message.content)



#experiment mit anderem modell, welche function calls unterstützt und nicht den attention mask bug aufweist, buuuuut.....

model_2 = GPT4All('Meta-Llama-3-8B-Instruct.Q4_0')

prompt_3 = f"""[{{
    "role": "system",
    "content": "You are a LLM that generates a subject line for a given post while following the following set of rules. Your Output is only the generated subject line"
}}, {{
    "role": "user",
    "content": "Please generate a subject line for the following post: \\n\\n {row} \\n\\n Based on the following set of rules: \\n\\n {set_of_instruction}"
}}]"""
print(prompt_3)
output = model_2.generate(prompt_3)
print(output)
#...this model is shit