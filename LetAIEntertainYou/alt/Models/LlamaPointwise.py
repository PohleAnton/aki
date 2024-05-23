import os

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import pandas as pd
import csv
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW
import pandas as pd
import json
from sklearn.model_selection import train_test_split


model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

data = pd.read_csv('LetAIEntertainYou/Models/new_2.csv', delimiter=';')
structured_data = []

for index, row in data.iterrows():
    entry_a = {
        "post": row['Posts'],
        "subject_line": row['Subject Line A'],
        "reward": 1 if row['Target'] == 'A' else 0
    }
    entry_b = {
        "post": row['Posts'],
        "subject_line": row['Subject Line B'],
        "reward": 1 if row['Target'] == 'B' else 0
    }
    structured_data.extend([entry_a, entry_b])

structured_df = pd.DataFrame(structured_data)

# Save the structured data to JSON
structured_df.to_json('structured_data.json', orient='records', lines=True)

print("Loading data...")
with open('structured_data.json', 'r') as f:
    data = [json.loads(line) for line in f]
print("Data loaded.")


# Define a custom dataset
class CustomDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        item = self.data[index]
        inputs = self.tokenizer(
            item['post'],
            item['subject_line'],
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        inputs = {k: v.squeeze() for k, v in inputs.items()}
        inputs['labels'] = torch.tensor(item['reward'], dtype=torch.float)

        # Debug statements
        print(f"Index: {index}")
        print(f"Post: {item['post']}")
        print(f"Subject Line: {item['subject_line']}")
        print(f"Inputs: {inputs}")

        return inputs


# Initialize the tokenizer


# Split the data into train and validation sets
print("Splitting data into train and validation sets...")
train_data, val_data = train_test_split(data, test_size=0.1, random_state=42)

# Create data loaders
print("Creating data loaders...")
train_dataset = CustomDataset(train_data, tokenizer)
val_dataset = CustomDataset(val_data, tokenizer)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8)

# Check if data loaders are working
print("Checking data loaders...")
try:
    for i, batch in enumerate(train_loader):
        print(f"Batch {i} loaded.")
        if i == 1:  # Check only the first couple of batches
            break
except Exception as e:
    print(f"Error loading batch: {e}")
# Training loop
optimizer = AdamW(model.parameters(), lr=5e-5)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)



for epoch in range(4):  # Number of epochs
    model.train()
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        inputs = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**inputs)
        loss = torch.nn.functional.mse_loss(outputs.logits.squeeze(), inputs['labels'])
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_train_loss = total_loss / len(train_loader)
    print(f'Epoch {epoch + 1}, Loss: {avg_train_loss}')

    model.eval()
    total_eval_loss = 0
    for batch in val_loader:
        with torch.no_grad():
            inputs = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**inputs)
            loss = torch.nn.functional.mse_loss(outputs.logits.squeeze(), inputs['labels'])
            total_eval_loss += loss.item()

    avg_val_loss = total_eval_loss / len(val_loader)
    print(f'Epoch {epoch + 1}, Validation Loss: {avg_val_loss}')
