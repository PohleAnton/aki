import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, GPT2Tokenizer, BertModel
import pandas as pd
import pickle
import numpy as np
import os
import torch.nn.functional as F

### Weil das Programm im Ordner Models startet
#os.chdir("../")
#os.chdir("../")
# Load the dataset
df_2 = pd.read_csv('LetAIEntertainYou/Posts/current/posts_rules_base_judged_neu.csv', delimiter=';')

# Initialize tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()

#embeddings für daten schon gemacht, können so geladen werden:
#müssen mit dem größeren datensatz erneut gemacht werden...

with open('LetAIEntertainYou/Posts/Vectors_retry/vector_a_neu.pkl', 'rb') as f:
    vector_a = pickle.load(f)

with open('LetAIEntertainYou/Posts/Vectors_retry/vector_b_neu.pkl', 'rb') as f:
    vector_b = pickle.load(f)

with open('LetAIEntertainYou/Posts/Vectors_retry/vector_posts.pkl', 'rb') as f:
    vector_posts = pickle.load(f)

df_2['Vector A'] = [torch.tensor(v) for v in vector_a]
df_2['Vector B'] = [torch.tensor(v) for v in vector_b]
df_2['Vector Posts'] = [torch.tensor(v) for v in vector_posts]
df_2['Target'] = df_2['Target'].apply(lambda x: 0 if x == 'A' else 1)  # Convert to binary labels


def text_to_vector(text, max_length=512):
    with torch.no_grad():
        text = str(text)
        inputs = tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=max_length)
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]  # Get the embedding for the [CLS] token
    return cls_embedding


df_2['Vector A'] = df_2['Subject Line A'].apply(lambda x: text_to_vector(x).numpy())
df_2['Vector B'] = df_2['Subject Line B'].apply(lambda x: text_to_vector(x).numpy())
df_2['Vector Posts'] = df_2['Posts'].apply(lambda x: text_to_vector(x).numpy())

data_a = []
df_2['Vector A'].apply(lambda x: data_a.append(x))

data_b = []
df_2['Vector B'].apply(lambda x: data_b.append(x))

data_posts = []
df_2['Vector Posts'].apply(lambda x: data_posts.append(x))

file = open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_a_neu.pkl', 'wb')
pickle.dump(data_a, file)
file.close()

# Vector B
file = open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_b_neu.pkl', 'wb')
pickle.dump(data_b, file)
file.close()

# Vector Posts
file = open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_posts.pkl', 'wb')
pickle.dump(data_posts, file)
file.close()


print('fertig')
train_data, test_data = train_test_split(df_2, test_size=0.2, random_state=42)

class SubjectLineDataset(Dataset):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        vector_posts = row['Vector Posts'].clone().detach().float()
        vector_a = row['Vector A'].clone().detach().float()
        vector_b = row['Vector B'].clone().detach().float()
        target = torch.tensor(row['Target'], dtype=torch.float)
        return vector_posts, vector_a, vector_b, target





class ComparisonModel(nn.Module):
    def __init__(self):
        super(ComparisonModel, self).__init__()
        self.fc1 = nn.Linear(768, 2304)  # Assuming output of BERT (768 features) and no concatenation before pooling
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(2304, 512)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.5)
        self.output = nn.Linear(512, 1)

    def forward(self, post, vector_a, vector_b):
        # Apply max pooling across the sequence length (dim=1)
        post = F.max_pool1d(post.transpose(1, 2), post.size(1)).squeeze(2)
        vector_a = F.max_pool1d(vector_a.transpose(1, 2), vector_a.size(1)).squeeze(2)
        vector_b = F.max_pool1d(vector_b.transpose(1, 2), vector_b.size(1)).squeeze(2)

        x = torch.cat((post, vector_a, vector_b), dim=1)
        x = self.dropout1(self.relu1(self.fc1(x)))
        x = self.dropout2(self.relu2(self.fc2(x)))
        x = self.output(x)
        return x


train_dataset = SubjectLineDataset(train_data)
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)

# Model, Loss, and Optimizer
model = ComparisonModel()
#criterion = nn.CrossEntropyLoss()
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=25, gamma=0.5)
# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    for posts, vectors_a, vectors_b, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(posts, vectors_a, vectors_b).squeeze()
        targets = targets.float()
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
    scheduler.step()
    print(f'Epoch {epoch+1}, Loss: {loss.item()}')

test_dataset = SubjectLineDataset(test_data)
test_loader = DataLoader(test_dataset, batch_size=2, shuffle=True)

model.eval()
correct = 0
total = 0
all_predictions = []
all_targets = []

with torch.no_grad():
    for posts, vectors_a, vectors_b, targets in test_loader:
        outputs = model(posts, vectors_a, vectors_b).squeeze()  # Get model outputs
        predicted_prob = torch.sigmoid(outputs)  # Apply sigmoid to convert logits to probabilities
        predicted_classes = (predicted_prob > 0.5).int()  # Threshold probabilities to get binary predictions
        total += targets.size(0)
        correct += (predicted_classes == targets).sum().item()
        all_predictions.extend(predicted_classes.numpy())  # Store predictions
        all_targets.extend(targets.numpy())  # Assuming targets were also loaded as tensors

accuracy = correct / total
print(f'Accuracy of the model on the test data: {accuracy*100:.2f}%')

from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

    # Assuming all_predictions and all_targets are available
print("Confusion Matrix:")
print(confusion_matrix(all_targets, all_predictions))
print("\nClassification Report:")
print(classification_report(all_targets, all_predictions))

"""
#tokenization und embedding: nur einmal nötig
def text_to_vector(text):
    with torch.no_grad():
        text = str(text)
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.squeeze()

### Bei mir konnte utf-8 einige Bytes nicht dekodieren, deshalb habe ich eine Kopie angelegt, wo ich diese durch utf-8 freundliche Äquivalente ersetzt
df_2 = pd.read_csv('LetAIEntertainYou/Posts/current/posts_rules_base_judged_neu.csv', delimiter=';', encoding="utf-8")

df_2['Vector A'] = df_2['Subject Line A'].apply(lambda x: text_to_vector(x).numpy())
df_2['Vector B'] = df_2['Subject Line B'].apply(lambda x: text_to_vector(x).numpy())
df_2['Vector Posts'] = df_2['Posts'].apply(lambda x: text_to_vector(x).numpy())

### Überführung in Pickle-files
import pickle

data_a = []
df_2['Vector A'].apply(lambda x: data_a.append(x))

data_b = []
df_2['Vector B'].apply(lambda x: data_b.append(x))

data_posts = []
df_2['Vector Posts'].apply(lambda x: data_posts.append(x))

# Vector A
file = open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_a_neu.pkl', 'wb')
pickle.dump(data_a, file)
file.close()

# Vector B
file = open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_b_neu.pkl', 'wb')
pickle.dump(data_b, file)
file.close()

# Vector Posts
file = open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_posts.pkl', 'wb')
pickle.dump(data_posts, file)
file.close()
"""