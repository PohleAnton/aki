"""
hier sollte vor allem mit einem modell experimentiert weren, welches function calls unterstützt
vor allem generiert dieses modell sehr zuverlässig posts und auch betreffzeilen.
das gegenwärtige setup produziert allerdings diesen fehler

The attention mask and the pad token id were not set. As a consequence, you may observe unexpected behavior. Please pass your input's `attention_mask` to obtain reliable results.
Setting `pad_token_id` to `eos_token_id`:128001 for open-end generation.

der dazu führt, dass das modell einfach immer weiter generiert, daher wird die range für die betreffzeilen weiter unten auch begrenzt
unabhängig davon sind geschwindigkeit und qualität des outputs aber sehr gut, deswegen wird dies voererst in kauf genommen
"""
import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
from accelerate import disk_offload
import csv

model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)


set_of_instruction = """
    We will send an email containing a post from a Nextdoor user. We want to use the most interesting part of the post as an email subject line.
    Task description: Given a post, output the most interesting phrase in the post.
    Here are the requirements:
    1. Extract the phrase as-is. Do not change any single character.
    2. Do not paraphrase. Copy the exact phrase. If the phrase you selected has stop words like "but", "and", "the", keep them in the output.
    3. Do not insert or remove any word.
    4. Make a subject line that brings curiosity. If the subject line gets too long, cut the phrase before the last part. For example, if the post has "Yesterday, my son found a dog barking at other people", output "Yesterday, my son found a dog barking at ..."
    5. Put the most important words in the beginning.
    6. If the first 10 words of the post contain unique and interesting words, reuse it.
    7. If the first 10 words of the post contain informal words, you can keep these words in the subject line. We want to respect the post content in the subject line.
    8. If the post has a phrase starting with "I" in the first 10 words, please use the same words in the subject line. It will make the subject line more personal. For example, if the post has "Hi All, I left my phone", use "I left my phone" in the subject line.
    9. If the some part of the post is all capitals, it is okay to extract that part. That part is what user wanted to emphasize. For example, extract all capital phrases like "CRIME ALERT".
    10. Do not use people’s names in the subject line.
    11. Do not add "Subject line:" in the output. Just output the content of the subject line.
    12. Capitalize the first character of the subject line. If the part you selected starts with a lower-cased character, capitalize the character.
    """

functions_metadata = [
    {
        "type": "function",
        "function": {
            "name": "write_subject_lines",
            "description": "A function that outputs the most interesting phrase for a given post following a set_of_instructions",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject_line": {
                        "type": "string",
                        "description": "A generated subject line"
                    }
                },
                "required": ["row", "set_of_instruction"]
            }
        }
    }
]
df = pd.read_csv("Posts/current/posts_best_of_n.csv", encoding='utf-8', sep=";")

def gen_llame(row):
    """
       Generiert eine base subject line

       Args:
           row (str): ein post, aus dem eine betreffzeile erzeugt wird
       Returns:
           base line generated subjectline
       """
    example = "[Subject line A; Subject line B; Subject line C; Subject line D; Subject line E]"
    messages = [
        {
            "role": "system",
            "content": f"You are a LLM that generates five different subject lines for a given post while following the following set of rules: \n\n {set_of_instruction} \n\n Your Output are only the generated subject lines without any further comments. Please format your response according to the following example: {example}. The instructions apply for each subject line, so your response can have more than 10 words."
        },
        {
            "role": "user",
            "content": f"Please generate five subject lines for the following post: \n\n {row} \n\n Based on the following set of rules: \n\n {set_of_instruction}",
        }
    ]
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    res = tokenizer.decode(response, skip_special_tokens=True)
    """
    if len(res.split(" ")) > 10:
    res = ' '.join(res.split(" ")[0:10]) + '...'
    """
    return res


#irgendwas weirdes mit attention mask...
for i in range(min(2793, len(df))):
    if pd.notna(df.loc[i, 'Posts']):  # Check if 'Posts' at row i is not NaN
        res = gen_llame(df.loc[i, 'Posts']).replace("[", "").replace("]", "").split(";")
        df.at[i, 'Subject Line A'] = res[0]
        df.at[i, 'Subject Line B'] = res[1]
        df.at[i, 'Subject Line C'] = res[2]
        df.at[i, 'Subject Line D'] = res[3]
        df.at[i, 'Subject Line E'] = res[4]
        print(df.iloc[i, ])

df.to_csv('Posts/current/posts_best_of_n.csv', sep=';', encoding='utf-8', index=False)
print('fertig')

'''
dies ist das original set of instructions - er sollen auch einmal damit daten erzeugt werden.
diese sind allerdings häufig identisch oder wenigstens sehr an nah an den regelbasierten ergebnissen, deswegen werden 2 datensätze erzeugt
'''

set_of_instruction_2 = """
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


def gen_llame_2(row):
    """
           Generiert eine base subject line

           Args:
               row (str): ein post, aus dem eine betreffzeile erzeugt wird
           Returns:
               base line generated subjectline
           """
    example = "[Subject line A; Subject line B; Subject line C; Subject line D; Subject line E]"
    messages = [
        {
            "role": "system",
            "content": f"You are a LLM that generates five different subject lines for a given post while following the following set of rules: \n\n {set_of_instruction_2} \n\n Your Output are only the generated subject lines without any further comments. Please format your response according to the following example: {example}. The instructions apply for each subject line, so your response can have more than 10 words."
        },
        {
            "role": "user",
            "content": f"Please generate five subject lines for the following post: \n\n {row} \n\n Based on the following set of rules: \n\n {set_of_instruction_2}",
        }
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    res = tokenizer.decode(response, skip_special_tokens=True)

    print(res)
    return res



for i in range(min(2793, len(df))):
    if pd.notna(df.loc[i, 'Posts']):
        res = gen_llame_2(df.loc[i, 'Posts']).replace("[", "").replace("]", "").split(";")
        df.at[i, 'Subject Line A'] = res[0]
        df.at[i, 'Subject Line B'] = res[1]
        df.at[i, 'Subject Line C'] = res[2]
        df.at[i, 'Subject Line D'] = res[3]
        df.at[i, 'Subject Line E'] = res[4]
        print(df.iloc[i,])

df.to_csv('LetAIEntertainYou/Posts/current/posts_best_of_n_2.csv', sep=';', encoding='utf-8', index=False)
print('fertig')
