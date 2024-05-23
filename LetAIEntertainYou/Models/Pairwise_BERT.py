import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
import pandas as pd
import pickle
import os


df = pd.read_csv('LetAIEntertainYou/data/full_training_set.csv', delimiter=';', encoding="utf-8")


device = torch.device("cpu")

tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = BertModel.from_pretrained('bert-base-cased')
model.to(device)
model.eval()

def text_to_vector(text):
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.squeeze()


df['Vector Posts'] = df['Posts'].apply(lambda x: text_to_vector(x).numpy())
df['Vector A'] = df['Subject Line A'].apply(lambda x: text_to_vector(x).numpy())
df['Vector B'] = df['Subject Line B'].apply(lambda x: text_to_vector(x).numpy())




df['Target'] = df['Target'].apply(lambda x: 0 if x == 'A' else 1)


train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

class SubjectLineDataset(Dataset):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        vector_posts = torch.tensor(row['Vector Posts'], dtype=torch.float)
        vector_a = torch.tensor(row['Vector A'], dtype=torch.float)
        vector_b = torch.tensor(row['Vector B'], dtype=torch.float)
        target = torch.tensor(row['Target'], dtype=torch.float)
        return vector_posts, vector_a, vector_b, target

class ComparisonModel(nn.Module):
    def __init__(self):
        super(ComparisonModel, self).__init__()
        self.fc1 = nn.Linear(2304, 4608)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(4608, 2304)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(2304, 512)
        self.relu3 = nn.ReLU()
        self.output = nn.Linear(512, 1)

    def forward(self, post, vector_a, vector_b):
        x = torch.cat((post, vector_a, vector_b), dim=1)
        x = self.dropout1(self.relu1(self.fc1(x)))
        x = self.dropout2(self.relu2(self.fc2(x)))
        x = self.relu3(self.fc3(x))
        x = self.output(x)
        return x



train_dataset = SubjectLineDataset(train_data)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

test_dataset = SubjectLineDataset(test_data)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=True)


model = ComparisonModel()
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=25, gamma=0.5)


num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    for i, (posts, vectors_a, vectors_b, targets) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(posts, vectors_a, vectors_b).squeeze()
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        if i == 0:
            print(f'Epoch {epoch + 1}, Batch {i + 1} Start Loss: {loss.item()}')
        if i == len(train_loader) - 1:
            print(f'Epoch {epoch + 1}, Batch {i + 1} End Loss: {loss.item()}')
    scheduler.step()


model.eval()
correct = 0
total = 0
all_predictions = []
all_targets = []

with torch.no_grad():
    for posts, vectors_a, vectors_b, targets in test_loader:
        outputs = model(posts, vectors_a, vectors_b).squeeze()
        predicted_prob = torch.sigmoid(outputs)
        predicted_classes = (predicted_prob > 0.5).int()
        total += targets.size(0)
        correct += (predicted_classes == targets).sum().item()
        all_predictions.extend(predicted_classes.numpy())
        all_targets.extend(targets.numpy())

accuracy = correct / total
print(f'Accuracy of the model on the test data: {accuracy*100:.2f}%')

from sklearn.metrics import confusion_matrix, classification_report
print("Confusion Matrix:")
print(confusion_matrix(all_targets, all_predictions))
print("\nClassification Report:")
print(classification_report(all_targets, all_predictions))

# with open('LetAIEntertainYou/Models/persist/embeddings/vector_posts.pkl', 'wb') as f:
#     pickle.dump(df['Vector Posts'].tolist(), f)
#
# with open('LetAIEntertainYou/Models/persist/embeddings/vector_a.pkl', 'wb') as f:
#     pickle.dump(df['Vector A'].tolist(), f)
#
# with open('LetAIEntertainYou/Models/persist/embeddings/vector_b.pkl', 'wb') as f:
#     pickle.dump(df['Vector B'].tolist(), f)