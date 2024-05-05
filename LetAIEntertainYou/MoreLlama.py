from gpt4all import GPT4All
import csv
import random


model = GPT4All('Meta-Llama-3-8B-Instruct.Q4_0.gguf')

filename = './LetAIEntertainYou/Posts/posts.csv'
liste = []
with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        liste.append(row[0])

set_of_instructions = """We will send an email containing a post from a Nextdoor user. We want to use the most interesting part of the post as an email subject line.
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

more_posts = []

liste_small = random.sample(liste, 5)
provided_string = "\n".join(f" {i + 1}. {entry}" for i, entry in enumerate(liste_small))

prompt = f"Write a post with a structure very similar to the examples provided in {provided_string}. Only write the post without any explanation"

output = model.generate("<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n" + prompt +
                        "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n")
print(output)

for i in range(0, 300):
    liste_small = random.sample(liste, 5)
    provided_string = "\n".join(f" {i + 1}. {entry}" for i, entry in enumerate(liste_small))

    prompt = f"{provided_string} contains 5 examples. Write one more post similar in structure. Only write the post without any explanation or anything else."

    output = model.generate("<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n" + prompt +
                            "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n")
    print(output)
    more_posts.append(output)
print('fertig')
print(len(more_posts))