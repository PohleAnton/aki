import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
import csv

model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

data = pd.read_csv('LetAIEntertainYou/Models/posts_rules_base_judged_neu.csv', delimiter=';', encoding="utf-8",
                   na_filter=False)

def gen_point(post, subject_line):
    messages = [
        {
            "role": "system",
            "content": f"You are an assistant to answer which email subject line is more"
                       f" engaging given the Text and subject line a and subject line b. Only answer a or b"
        },
        {
            "role": "user",
            "content": f"Text: {post}Subject line: {subject_line} Question: Is the above an excellent subject line for an email post of the"
                       f"given text? An excellent subject line is coherent, informative, and engaging. "
                       f"We will send this email to our users hoping the users find it interesting and"
                       f"want to click on the email. Answer with yes or no.Answer:",
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
    return res



data['Answer A'] = data.apply(lambda row: gen_point(row['Posts'], row['Subject Line A']), axis=1)
data['Answer B'] = data.apply(lambda row: gen_point(row['Posts'], row['Subject Line B']), axis=1)

data.to_csv('LetAIEntertainYou/Models/posts_rules_base_pointwise_columns.csv', sep=';')