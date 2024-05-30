'''
so ähnlich könnte man das policy model finetunen - das können wir nicht wirklich versuchen, weil wir nicht die hardware dafür haben
bzw. gpt sehr kostenintensiv sein könnte.
'''
import torch
from datasets import Dataset
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoTokenizer, AutoModelForCausalLM, DataCollatorForSeq2Seq
import pandas as pd
from torch.optim import AdamW
model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

device = torch.device("cpu")
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)

# Load the dataset
df = pd.read_csv('LetAIEntertainYou/data/data_for_policy.csv', delimiter=';')
def format_with_prompt(example):
    prompt_text = "We will send an email containing a post from a Nextdoor user. We want to use the most interesting part of the post as an email subject line. Given a post, output the most interesting phrase in the post. Post: {}"
    example['formatted_post'] = prompt_text.format(example['post'])
    example['selected_subject_line'] = example['subject line']
    return example

# Create and format the dataset
dataset = Dataset.from_pandas(df)
formatted_dataset = dataset.map(format_with_prompt)

# Tokenization
def tokenize_function(examples):
    model_inputs = tokenizer(examples['formatted_post'], truncation=True, padding="max_length", max_length=512)
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples['selected_subject_line'], truncation=True, padding="max_length", max_length=512)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = formatted_dataset.map(tokenize_function, batched=True)

# Convert data to TensorDataset
def convert_to_tensordataset(dataset):
    input_ids = torch.tensor(dataset['input_ids'], dtype=torch.long)
    attention_mask = torch.tensor(dataset['attention_mask'], dtype=torch.long)
    labels = torch.tensor(dataset['labels'], dtype=torch.long)
    return TensorDataset(input_ids, attention_mask, labels)

# Optimizer
optimizer = AdamW(model.parameters(), lr=1e-5)

for param in model.parameters():
    param.requires_grad = False

last_layer_name = 'lm_head'
for name, param in model.named_parameters():
    if last_layer_name in name:
        param.requires_grad = True
criterion = torch.nn.CrossEntropyLoss()
# Training function
def train_model(model, train_loader, optimizer, num_epochs):
    model.train()
    for epoch in range(num_epochs):
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()

            inputs = batch[0].to(device)
            attention_mask = batch[1].to(device)
            labels = batch[2].to(device)

            outputs = model(input_ids=inputs, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss if 'loss' in outputs else criterion(outputs.logits, labels)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch + 1}, Average Loss: {total_loss / len(train_loader)}, Total Loss: {total_loss}")

# Training on subsets of data

subsets = [(0,2),(0, 25), (25, 75), (75, 175)]  # Start and end indices for each subset
for start_index, end_index in subsets:
    print(f"Training on entries {start_index} to {end_index - 1}")
    subset_indices = range(start_index, end_index)
    subset_dataset = tokenized_datasets.select(subset_indices)
    subset_train_tensor_dataset = convert_to_tensordataset(subset_dataset)
    subset_train_loader = DataLoader(subset_train_tensor_dataset, batch_size=16, shuffle=True)
    train_model(model, subset_train_loader, optimizer, 3)