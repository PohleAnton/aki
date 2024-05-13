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
df = pd.read_csv("LetAIEntertainYou/Posts/current/posts_best_of_n.csv", encoding='utf-8', sep=";")

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

#column_nam es wird hier sehr lang gewählt, weil das modell manchmal mehr als 5 einträge erzeugt
column_names=['Subject line A', 'Subject line B', 'Subject line C', 'Subject line D', 'Subject line E', 'Subject line F', 'Subject line G', 'Subject line H','Subject line I','Subject line J','Subject line K','Subject line L','Subject line M', ]
new_df =pd.DataFrame(columns=column_names)
#setzt hier examplarisch nach einem error ein
for i in range(2122, 2701):
    if pd.notna(df.loc[i, 'Posts']):
        output = gen_llame(df.loc[i, 'Posts'])
        output = output.replace("[", "").replace("]", "").split(";")
        output = [x.strip() for x in output]  # Clean any whitespace from the splits
        row_data = pd.Series(output, index=column_names[:len(output)])
        row_df = pd.DataFrame([row_data])
        new_df = pd.concat([new_df, row_df], ignore_index=True)
        print(row_data)


def gen_llame_single(row):
    """
           5 Zeilen generieren funktioniert nicht zuverlässig genug, daher wird 1 versucht

           Args:
               row (str): ein post, aus dem eine betreffzeile erzeugt wird
           Returns:
               base line generated subjectline
           """

    messages = [
        {
            "role": "system",
            "content": f"You are a  LLM that generates a subject line for a given post while following the following set of rules: \n\n {set_of_instruction_2} \n\n Your Output is only the generated subject line without any further comments."
        },
        {
            "role": "user",
            "content": f"Please generate a subject line for the following post: \n\n {row} \n\n Based on the following set of rules: \n\n {set_of_instruction_2}",
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




#diese zeilen wurden fehlerhaft erzeug
missing=[2626,2594,2569,2522,2503,2474,2239,2192,2189,2161,2060,2061,2025,1714,1708,1682,1672,1667,1587,1571,1487,1439,1432,1405,1395,1336,1225,1216,1211,1182,1100,1092,1031,972,106,1052,1087,]
new_missing=[x - 2 for x in missing]
new_missing.sort()
subject_line_cols = ['Subject Line A', 'Subject Line B', 'Subject Line C', 'Subject Line D', 'Subject Line E']

results_df = pd.DataFrame()
for i in new_missing:
    if i < len(df) and pd.notna(df.loc[i, 'Posts']):
        new_row = {}
        for col in subject_line_cols:
            new_row[col] = gen_llame_single(df.loc[i, 'Posts'])

        row_df = pd.DataFrame([new_row])
        results_df = pd.concat([results_df, row_df], ignore_index=True)
        print(row_df)


#results_df.to_csv('LetAIEntertainYou/Posts/current/posts_best_of_n_2_9.csv', sep=';', encoding='utf-8', index=False)

