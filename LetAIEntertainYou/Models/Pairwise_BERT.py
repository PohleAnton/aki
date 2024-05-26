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


model =BertModel.from_pretrained('bert-base-cased')
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
'''
ich habe leider vergessen, mit vielen epochen trainiert...40? die genauigkeit ist (wie im paper) ohnehin nicht gut (50.1)
model_save_path = "LetAIEntertainYou/Models/persist/BERT_pairwise.pth"
model.load_state_dict(torch.load(model_save_path))
'''
criterion = nn.BCEWithLogitsLoss()
optimizer = AdamW(model.parameters(), lr=2e-5)
total_steps = len(train_loader) * 3
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)


num_epochs = 1
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


# das dient vor allem um zu checken, ob beide labesl vorhergesagt werden können - es kam oft vor, dass nur 1 vorhergesagt wurde
accuracy = accuracy_score(true_labels, predictions)
print(f'Accuracy: {accuracy * 100:.2f}%')
print("Confusion Matrix:")
print(confusion_matrix(true_labels, predictions))
print("\nClassification Report:")
print(classification_report(true_labels, predictions))


model_save_path = "LetAIEntertainYou/Models/persist/BERT_pairwise.pth"
torch.save(model.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")


#pick winner best of n
data = pd.read_csv('LetAIEntertainYou/data/posts_best_of_n_complete.csv', delimiter=';', encoding="utf-8", na_filter=True)




#das könnte genutzt werden, um pairwise alle 5 samples zu vergleichen...im paper wird pointwise genutzt, deswegen machen wir das auch vorerste
def compare_subject_lines(model, tokenizer, context, subject_line1, subject_line2):

    inputs1 = tokenizer(context + " " + subject_line1, return_tensors='pt', padding='max_length', truncation=True, max_length=512)
    inputs2 = tokenizer(context + " " + subject_line2, return_tensors='pt', padding='max_length', truncation=True, max_length=512)


    input_ids = torch.cat([inputs1['input_ids'], inputs2['input_ids']], dim=0).unsqueeze(0).to(device)
    attention_mask = torch.cat([inputs1['attention_mask'], inputs2['attention_mask']], dim=0).unsqueeze(0).to(device)
    token_type_ids = torch.cat([inputs1['token_type_ids'], inputs2['token_type_ids']], dim=0).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(input_ids, attention_mask, token_type_ids).squeeze()


    logits_value = logits.item()
    if logits_value > 0:
        return subject_line1
    else:
        return subject_line2


def find_best_subject_line(model, tokenizer, row):
    context = row['Posts']
    current_winner = row['Subject Line A']
    for i in range(1, 5):  # From B to E
        next_contender = row[f'Subject Line {chr(65+i)}']
        current_winner = compare_subject_lines(model, tokenizer, context, current_winner, next_contender)

    return current_winner

# Apply to DataFrame
data['Best Subject Line'] = data.apply(lambda row: find_best_subject_line(model, tokenizer, row), axis=1)

def trim_subject_line(subject):
    words = subject.split()
    if len(words) > 10:
        return ' '.join(words[:10]) + '...'
    else:
        return subject
data['Best Subject Line'] = data['Best Subject Line'].apply(trim_subject_line)
data.to_csv('LetAIEntertainYou/data/pair_rejection_results.csv', sep=';', encoding='utf-8', index=False)
