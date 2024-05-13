import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
import pandas as pd
import pickle
import os
import numpy as np
#os.chdir("../")
os.getcwd()
# Load the dataset
df_2 = pd.read_csv('LetAIEntertainYou/Posts/current/posts_rules_base_judged_neu.csv', delimiter=';')

# Initialize tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()

# Tokenize and convert text to BERT embeddings with padding
def text_to_vector(text):
    with torch.no_grad():
        text = str(text)
        inputs = tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=512)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.squeeze()
    return embeddings

# Apply the function to both columns and store the embeddings
df_2['Vector A'] = df_2['Subject Line A'].apply(lambda x: text_to_vector(x))
df_2['Vector B'] = df_2['Subject Line B'].apply(lambda x: text_to_vector(x))
df_2['Target'] = df_2['Target'].apply(lambda x: 0 if x == 'A' else 1)  # Convert to binary labels

# Save the vectors to avoid recomputing
vector_a = df_2['Vector A'].tolist()
vector_b = df_2['Vector B'].tolist()
print('fertig')
with open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_a.pkl', 'wb') as f:
    pickle.dump(vector_a, f)

with open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_b.pkl', 'wb') as f:
    pickle.dump(vector_b, f)

# Split the data
train_data, test_data = train_test_split(df_2, test_size=0.2, random_state=42)

class SubjectLineDataset(Dataset):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        vector_a = row['Vector A']
        vector_b = row['Vector B']
        target = torch.tensor(row['Target'], dtype=torch.float)
        return vector_a, vector_b, target

def pad_collate(batch):
    (vectors_a, vectors_b, targets) = zip(*batch)
    vectors_a = [v.unsqueeze(0) for v in vectors_a]
    vectors_b = [v.unsqueeze(0) for v in vectors_b]
    vectors_a = torch.nn.utils.rnn.pad_sequence(vectors_a, batch_first=True, padding_value=0)
    vectors_b = torch.nn.utils.rnn.pad_sequence(vectors_b, batch_first=True, padding_value=0)
    targets = torch.stack(targets)
    return vectors_a, vectors_b, targets

class ComparisonModel(nn.Module):
    def __init__(self):
        super(ComparisonModel, self).__init__()
        self.fc1 = nn.Linear(768 * 2, 1536)  # Adjust input size for concatenated vectors
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(1536, 512)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.5)
        self.output = nn.Linear(512, 1)

    def forward(self, vector_a, vector_b):
        vector_a = vector_a.mean(dim=1)  # Average over the padded sequences
        vector_b = vector_b.mean(dim=1)  # Average over the padded sequences
        x = torch.cat((vector_a, vector_b), dim=-1)  # Concatenate on the last dimension
        x = self.dropout1(self.relu1(self.fc1(x)))
        x = self.dropout2(self.relu2(self.fc2(x)))
        x = self.output(x)
        return x

train_dataset = SubjectLineDataset(train_data)
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, collate_fn=pad_collate)

# Model, Loss, and Optimizer
model = ComparisonModel()
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=25, gamma=0.5)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    for vectors_a, vectors_b, targets in train_loader:
        optimizer.zero_grad()
        vectors_a = vectors_a.float()
        vectors_b = vectors_b.float()
        outputs = model(vectors_a, vectors_b).squeeze()
        targets = targets.float()
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
    scheduler.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

test_dataset = SubjectLineDataset(test_data)
test_loader = DataLoader(test_dataset, batch_size=2, shuffle=True, collate_fn=pad_collate)

model.eval()
correct = 0
total = 0
all_predictions = []
all_targets = []

with torch.no_grad():
    for vectors_a, vectors_b, targets in test_loader:
        vectors_a = vectors_a.float()
        vectors_b = vectors_b.float()
        outputs = model(vectors_a, vectors_b).squeeze()
        predicted_prob = torch.sigmoid(outputs)
        predicted_classes = (predicted_prob > 0.5).int()
        total += targets.size(0)
        correct += (predicted_classes == targets).sum().item()
        all_predictions.extend(predicted_classes.numpy())
        all_targets.extend(targets.numpy())

accuracy = correct / total
print(f'Accuracy of the model on the test data: {accuracy*100:.2f}%')

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

print("Confusion Matrix:")
print(confusion_matrix(all_targets, all_predictions))
print("\nClassification Report:")
print(classification_report(all_targets, all_predictions))
