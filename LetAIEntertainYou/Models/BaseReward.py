import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
import csv
from gpt4all import GPT4All


#old model, not finetunable:
model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"


#model_id ="meta-llama/Meta-Llama-3-8B"


tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

classification_head_attrs = ['classifier', 'classification_head', 'score', 'lm_head']

has_classification_head = any(hasattr(model, attr) for attr in classification_head_attrs)


data = pd.read_csv('LetAIEntertainYou/Models/posts_rules_base_judged_neu.csv', delimiter=';', encoding="utf-8",
                   na_filter=False)
data.head()


def gen_point(post, subject_line_a, subject_line_b):
    #old model:
    messages = [
        {
            "role": "system",
            "content": f"You are an assistant to answer which email subject line is more"
                       f" engaging given the Text and subject line a and subject line b. Only answer a or b"
        },
        {
            "role": "user",
            "content": f"Text: {post} "
                       f" Subject line a: {subject_line_a}"
                       f" Subject line b: {subject_line_b} "
                       f"Question: Which subject line is more engaging for an email post?"
                       f"An excellent subject line is coherent, informative, "
                       f"and engaging. We will send this email to our users hoping the users find it interesting and want to click on the email."
                       f" Answer with a or b"


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
        #pad_token_id=tokenizer.eos_token_id,
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

#new model: siehe Pointwise_TryLlamaFinetune.py

results = []

# Iterate over each row in the DataFrame
for index, row in data.iterrows():
    # Extract data from each row
    post = row['Posts']
    subject_line_a = row['Subject Line A']
    subject_line_b = row['Subject Line B']

    try:
        # Call the function to generate the point
        result = gen_point(post, subject_line_a, subject_line_b)
    except Exception as e:
        print(f"Error processing row {index}: {e}")
        result = None  # You could choose to set a default value or handle the error differently

    # Append the result to the list
    results.append(result)
data['result'] = results
data['result'] = data['result'].str.upper()
data.to_csv('LetAIEntertainYou/Models/new_2.csv', sep=';')