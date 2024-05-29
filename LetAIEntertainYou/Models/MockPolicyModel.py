'''
so ähnlich könnte man das policy model finetunen - das können wir nicht wirklich versuchen, weil wir nicht die hardware dafür haben
bzw. gpt sehr kostenintensiv sein könnte.
'''
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd

model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(model_id)


#diese datein entält: einen post, sowie wie den sieger aus rules based generation vs. sieger aus rejection sampling
df=pd.read_csv('LetAIEntertainYou/data/data_for_policy.csv', delimiter=';')

def format_with_prompt(example):
    prompt_text = "We will send an email containing a post from a Nextdoor user. We want to use the most interesting part of the post as an email subject line. Given a post, output the most interesting phrase in the post. Post: {}"
    example['formatted_post'] = prompt_text.format(example['post'])
    example['selected_subject_line'] = example['subject line']
    return example

dataset = Dataset.from_pandas(df)
formatted_dataset = dataset.map(format_with_prompt)

def tokenize_function(examples):
    model_inputs = tokenizer(examples['post'], truncation=True, padding="max_length", max_length=512)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples['subject line'], truncation=True, padding="max_length", max_length=512)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(tokenize_function, batched=True)

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],
    data_collator=data_collator,
)

trainer.train()
