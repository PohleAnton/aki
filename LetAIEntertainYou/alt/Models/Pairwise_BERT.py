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
os.getcwd()
### Weil das Programm im Ordner Models startet
#os.chdir("../../")
#os.chdir("../../")
# Load the dataset
df_2 = pd.read_csv('LetAIEntertainYou/data/posts_rules_base_judged_neu.csv', delimiter=';')

# Initialize tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = BertModel.from_pretrained('bert-base-cased')
model.eval()

#embeddings für daten schon gemacht, können so geladen werden:
#müssen mit dem größeren datensatz erneut gemacht werden...


# with open('LetAIEntertainYou/Models/persist/embeddings/vector_posts.pkl', 'rb') as f:
#     vector_posts = pickle.load(f)
#
# with open('LetAIEntertainYou/Models/persist/embeddings/vector_a.pkl', 'rb') as f:
#     vector_a = pickle.load(f)
#
# with open('LetAIEntertainYou/Models/persist/embeddings/vector_b.pkl', 'rb') as f:
#     vector_b = pickle.load(f)
def text_to_vector(text):
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.squeeze()

df_2['Vector A'] = df_2['Posts'].apply(lambda x: text_to_vector(x).numpy())
df_2['Vector B'] = df_2['Subject Line A'].apply(lambda x: text_to_vector(x).numpy())
df_2['Vector Posts'] = df_2['Subject Line B'].apply(lambda x: text_to_vector(x).numpy())
df_2['Target'] = df_2['Target'].apply(lambda x: 0 if x == 'A' else 1)  # Convert to binary labels


train_data, test_data = train_test_split(df_2, test_size=0.2, random_state=42)

class SubjectLineDataset(Dataset):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        vector_posts = torch.tensor(row['Vector Posts']).float()
        vector_a = torch.tensor(row['Vector A']).float()
        vector_b = torch.tensor(row['Vector B']).float()
        target = torch.tensor(row['Target'], dtype=torch.float)
        return vector_posts, vector_a, vector_b, target



class ComparisonModel(nn.Module):
    def __init__(self):
        super(ComparisonModel, self).__init__()
        self.fc1 = nn.Linear(2304, 4608)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.5)  # Adding dropout
        self.fc2 = nn.Linear(4608, 1536)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.5)  # Adding dropout
        self.output = nn.Linear(1536, 1)

    def forward(self, post, vector_a, vector_b):
        x = torch.cat((post, vector_a, vector_b), dim=1)
        x = self.dropout1(self.relu1(self.fc1(x)))
        x = self.dropout2(self.relu2(self.fc2(x)))
        x = self.output(x)
        return x
class EnhancedComparisonModel(nn.Module):
    def __init__(self):
        super(EnhancedComparisonModel, self).__init__()
        self.fc1 = nn.Linear(2304, 4608)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(4608, 3072)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(3072, 1536)
        self.relu3 = nn.ReLU()
        self.dropout3 = nn.Dropout(0.5)
        self.output = nn.Linear(1536, 1)

    def forward(self, post, vector_a, vector_b):
        x = torch.cat((post, vector_a, vector_b), dim=1)
        x = self.dropout1(self.relu1(self.fc1(x)))
        x = self.dropout2(self.relu2(self.fc2(x)))
        x = self.dropout3(self.relu3(self.fc3(x)))
        x = self.output(x)
        return x

# Model, Loss, and Optimizer
model = EnhancedComparisonModel()



train_dataset = SubjectLineDataset(train_data)
train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)

# Model, Loss, and Optimizer
model = ComparisonModel()
#criterion = nn.CrossEntropyLoss()
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=25, gamma=0.5)
# Training loop
num_epochs = 15
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


def convert_to_tensor(embedding):
    return torch.tensor(embedding, dtype=torch.float32)


# Apply conversion
df_2['Vector A'] = df_2['Vector A'].apply(convert_to_tensor)
df_2['Vector B'] = df_2['Vector B'].apply(convert_to_tensor)
df_2['Vector Posts'] = df_2['Vector Posts'].apply(convert_to_tensor)

import numpy as np
import torch
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Ensure embeddings are numpy arrays
df_2['Vector A'] = df_2['Vector A'].apply(lambda x: np.array(x))
df_2['Vector B'] = df_2['Vector B'].apply(lambda x: np.array(x))
df_2['Vector Posts'] = df_2['Vector Posts'].apply(lambda x: np.array(x))


# Function to visualize embeddings
def visualize_embeddings(df, column, label_column):
    embeddings = df[column].tolist()
    embeddings = np.stack(embeddings)

    # Reduce dimensions for visualization
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(embeddings)

    # Plot
    plt.figure(figsize=(8, 6))
    for label in df[label_column].unique():
        idx = df[df[label_column] == label].index
        plt.scatter(reduced_embeddings[idx, 0], reduced_embeddings[idx, 1], label=label)
    plt.legend()
    plt.title(f'PCA of {column}')
    plt.show()


# Visualize embeddings for 'Vector Posts'
visualize_embeddings(df_2, 'Vector Posts', 'Target')