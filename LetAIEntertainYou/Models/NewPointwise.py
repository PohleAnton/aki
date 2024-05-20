import pandas as pd
import torch
from torch import device as torch_device, no_grad
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification, AutoTokenizer, AutoModelForCausalLM
from sklearn.model_selection import train_test_split
import os
# Load data
os.getcwd()
data = pd.read_csv('LetAIEntertainYou/Posts/current/posts_best_of_n_complete_with_target.csv', delimiter=';', encoding="utf-8")
data.reset_index(drop=True, inplace=True)


model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Tokenizer and Model
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = BertForSequenceClassification.from_pretrained('bert-base-cased', num_labels=2)

class SubjectLineDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_len):
        self.len = len(dataframe)
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __getitem__(self, index):
        post = str(self.data.iloc[index]['Posts'])
        subject_lines = [
            str(self.data.iloc[index]['Subject Line A']),
            str(self.data.iloc[index]['Subject Line B'])
        ]
        target_label = str(self.data.iloc[index]['Target'])


        inputs = []
        for subject_line in subject_lines:
            prompt_text = f"{post} [SEP] Is this an excellent subject line? {subject_line}"
            tokenized_input = self.tokenizer.encode_plus(
                prompt_text,
                add_special_tokens=True,
                max_length=self.max_len,
                padding='max_length',
                return_token_type_ids=True,
                truncation=True
            )
            inputs.append(tokenized_input)


        label = ord(target_label) - ord('A')


        ids = inputs[label]['input_ids']
        mask = inputs[label]['attention_mask']

        return {
            'input_ids': torch.tensor(ids, dtype=torch.long),
            'attention_mask': torch.tensor(mask, dtype=torch.long),
            'labels': torch.tensor(label, dtype=torch.long)
        }

    def __len__(self):
        return self.len

# Data preparation
max_len = 128
batch_size = 16

train, test = train_test_split(data, test_size=0.1)
train_dataset = SubjectLineDataset(train, tokenizer, max_len)
test_dataset = SubjectLineDataset(test, tokenizer, max_len)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=True)

# Setting device
device = torch_device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Optimizer
optimizer = AdamW(model.parameters(), lr=1e-5)

# Training loop
model.train()
for epoch in range(3):  # Adjust the number of epochs based on your requirements
    for batch_index, batch_data in enumerate(train_loader):
        ids = batch_data['input_ids'].to(device)
        mask = batch_data['attention_mask'].to(device)
        labels = batch_data['labels'].to(device)

        # Forward pass
        outputs = model(ids, mask, labels=labels)
        loss = outputs.loss

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Print loss and debug info every 10 batches
        if batch_index % 10 == 0:
            print(f"Epoch: {epoch}, Batch: {batch_index}, Loss: {loss.item()}")

# Evaluate the model
def evaluate_model(model, test_loader, device):
    model.eval()
    correct_predictions = 0
    total_predictions = 0

    with no_grad():
        for batch in test_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            _, predictions = torch.max(outputs.logits, dim=1)

            correct_predictions += (predictions == labels).sum().item()
            total_predictions += labels.size(0)

    accuracy = correct_predictions / total_predictions
    print(f"Accuracy: {accuracy:.4f}")

# Call the evaluation
evaluate_model(model, test_loader, device)
