import pandas as pd
from torch import device as torch_device
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from sklearn.model_selection import train_test_split
from torch import no_grad
import os

os.chdir('../')
os.chdir('../')

data = pd.read_csv('LetAIEntertainYou/Posts/current/posts_rules_base_judged_neu.csv', delimiter=';')
data['label'] = (data['Target'] == 'B').astype(int)
data.reset_index(drop=True, inplace=True)

#model laden - achtung, dies ist das mit weniger datensätzen:
model = BertForSequenceClassification.from_pretrained('bert-base-cased', num_labels=2)
#model.load_state_dict(torch.load('LetAIEntertainYou/Models/pointwise_little_data_dict.pth'))


#mit dem folgenden code wurde auf grundlage des 1016 einträge datensatzes ein modell mit 93 genauigkeit trainiert
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

class SubjectLineDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_len):
        self.len = len(dataframe)
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __getitem__(self, index):
     # Use `.iloc` for robust index handling
        post = str(self.data.iloc[index]['Posts'])
        subject_line_a = str(self.data.iloc[index]['Subject Line A'])
        subject_line_b = str(self.data.iloc[index]['Subject Line B'])
        label = int(self.data.iloc[index]['label'])

        inputs_a = self.tokenizer.encode_plus(
            post + " [SEP] " + subject_line_a,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=True,
            truncation=True
        )
        inputs_b = self.tokenizer.encode_plus(
            post + " [SEP] " + subject_line_b,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=True,
            truncation=True
        )

        if label == 1:
            ids = inputs_b['input_ids']
            mask = inputs_b['attention_mask']
        else:
            ids = inputs_a['input_ids']
            mask = inputs_a['attention_mask']

        return {
            'input_ids': torch.tensor(ids, dtype=torch.long),
            'attention_mask': torch.tensor(mask, dtype=torch.long),
            'labels': torch.tensor(label, dtype=torch.long)
        }


    def __len__(self):
        return self.len


max_len = 128
batch_size = 16

train, test = train_test_split(data, test_size=0.1)
train_dataset = SubjectLineDataset(train, tokenizer, max_len)
test_dataset = SubjectLineDataset(test, tokenizer, max_len)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=True)

device = torch_device("cuda" if torch.cuda.is_available() else "cpu")
# Model
model = BertForSequenceClassification.from_pretrained('bert-base-cased', num_labels=2)
model.to(device)

# Optimizer
optimizer = AdamW(model.parameters(), lr=1e-5)

model.train()
for epoch in range(3):  # Adjust the number of epochs based on your requirements
    for batch_index, batch_data in enumerate(train_loader, 0):
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
            print(f"Sample Input IDs: {ids[0][:10]}")  # Print first 10 tokens of the first sample in the batch
            print(f"Sample Label: {labels[0]}")

def evaluate_model(model, test_loader, device):
    model.eval()  # Put the model in evaluation mode
    correct_predictions = 0
    total_predictions = 0

    with no_grad():  # Disable gradient computation during inference
        for batch in test_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            _, predictions = torch.max(outputs.logits, dim=1)

            correct_predictions += (predictions == labels).sum().item()
            total_predictions += labels.size(0)

    accuracy = correct_predictions / total_predictions
    return accuracy

# Assuming you have a 'test_loader' and your model and it is on the correct 'device'
test_accuracy = evaluate_model(model, test_loader, device)
print(f"Test Accuracy: {test_accuracy:.2f}")


def predict_subject_line_engagement(post, subject_line_a, subject_line_b):
    # Tokenize subject lines
    inputs_a = tokenizer.encode_plus(post + " [SEP] " + subject_line_a, return_tensors="pt", padding=True, truncation=True, max_length=128)
    inputs_b = tokenizer.encode_plus(post + " [SEP] " + subject_line_b, return_tensors="pt", padding=True, truncation=True, max_length=128)

    # Get logits from the model
    with torch.no_grad():
        logits_a = model(**inputs_a).logits
        logits_b = model(**inputs_b).logits

    # Apply softmax to convert logits to probabilities
    prob_a = torch.softmax(logits_a, dim=1)[:, 1]  # Probability of being engaging
    prob_b = torch.softmax(logits_b, dim=1)[:, 1]

    # Compare and select more engaging subject line
    if prob_a > prob_b:
        return "Subject Line A is more engaging"
    else:
        return "Subject Line B is more engaging"

# Example call
result = predict_subject_line_engagement("Hey neighbors! Just spotted a set of keys with a cute turtle keychain near the playground at Parkside Ave. If they're yours or you know whose they might be, please message me here or pick them up at my porch at 153 Parkside Ave. Let's get these keys back to their owner!",
                                         "Hey Neighbors! Found",
                                         "Hey neighbors! Just spotted a set of keys with a...")
print(result)


#nicht in github...nimmt zu viel speicher
#torch.save(model, 'LetAIEntertainYou/Models/pointwise_little_data.pth' )
#torch.save(model.state_dict(), 'LetAIEntertainYou/Models/pointwise_little_data_dict.pth')
