import torch
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from torch import nn
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertModel, AdamW, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random


df_2 = pd.read_csv('LetAIEntertainYou/data/posts_rules_base_judged_neu.csv', delimiter=';')
df_2['Target'] = df_2['Target'].apply(lambda x: 0 if x == 'A' else 1)  # Convert to binary labels


tokenizer = BertTokenizer.from_pretrained('bert-base-cased')



class PairwiseDataset(Dataset):
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.pairs = self.create_pairs()

    def create_pairs(self):
        pairs = []
        for idx, row in self.dataframe.iterrows():
            context = row['Posts']
            answer_a = row['Subject Line A']
            answer_b = row['Subject Line B']
            target = row['Target']

            if random.random() > 0.5:
                pairs.append((context, answer_a, answer_b, target))
            else:
                pairs.append((context, answer_b, answer_a, 1 - target))
        return pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        context, answer_a, answer_b, target = self.pairs[idx]
        inputs_a = tokenizer(context + " " + answer_a, return_tensors='pt', padding='max_length', truncation=True,
                             max_length=512)
        inputs_b = tokenizer(context + " " + answer_b, return_tensors='pt', padding='max_length', truncation=True,
                             max_length=512)

        inputs = {key: torch.cat((inputs_a[key], inputs_b[key]), dim=0) for key in inputs_a.keys()}
        inputs['labels'] = torch.tensor(target, dtype=torch.long)
        return inputs



train_data, test_data = train_test_split(df_2, test_size=0.2, random_state=42)


train_dataset = PairwiseDataset(train_data)
test_dataset = PairwiseDataset(test_data)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)



class PairwiseBERT(nn.Module):
    def __init__(self):
        super(PairwiseBERT, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-cased')
        self.classifier = nn.Linear(self.bert.config.hidden_size * 2, 1)

    def forward(self, input_ids, attention_mask, token_type_ids):
        outputs_a = self.bert(input_ids[:, 0, :], attention_mask=attention_mask[:, 0, :],
                              token_type_ids=token_type_ids[:, 0, :])
        outputs_b = self.bert(input_ids[:, 1, :], attention_mask=attention_mask[:, 1, :],
                              token_type_ids=token_type_ids[:, 1, :])

        pooled_output_a = outputs_a.pooler_output
        pooled_output_b = outputs_b.pooler_output

        combined_output = torch.cat((pooled_output_a, pooled_output_b), dim=1)
        logits = self.classifier(combined_output)
        return logits



device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = PairwiseBERT().to(device)
criterion = nn.BCEWithLogitsLoss()
optimizer = AdamW(model.parameters(), lr=2e-5)
total_steps = len(train_loader) * 3
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)


num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch in train_loader:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        token_type_ids = batch['token_type_ids'].to(device)
        labels = batch['labels'].to(device).float()

        outputs = model(input_ids, attention_mask, token_type_ids).squeeze()
        loss = criterion(outputs, labels)
        total_loss += loss.item()
        loss.backward()
        optimizer.step()
        scheduler.step()
    avg_train_loss = total_loss / len(train_loader)
    print(f'Epoch {epoch + 1}, Loss: {avg_train_loss}')


model.eval()
predictions, true_labels = [], []
with torch.no_grad():
    for batch in test_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        token_type_ids = batch['token_type_ids'].to(device)
        labels = batch['labels'].to(device)

        outputs = model(input_ids, attention_mask, token_type_ids).squeeze()
        preds = torch.sigmoid(outputs).round().cpu().numpy()
        predictions.extend(preds)
        true_labels.extend(labels.cpu().numpy())


accuracy = accuracy_score(true_labels, predictions)
print(f'Accuracy: {accuracy * 100:.2f}%')
print("Confusion Matrix:")
print(confusion_matrix(true_labels, predictions))
print("\nClassification Report:")
print(classification_report(true_labels, predictions))


model_save_path = "LetAIEntertainYou/Models/persist/BERT_pairwise.pth"
torch.save(model.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")