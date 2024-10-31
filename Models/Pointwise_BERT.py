
import pandas as pd
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from torch import no_grad
from torch.utils.data import DataLoader
from transformers import BertForSequenceClassification, BertTokenizer, AdamW, AutoTokenizer, \
    AutoModelForSequenceClassification

print(torch.cuda.is_available())
print(torch.version.cuda)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_b = BertForSequenceClassification.from_pretrained('bert-base-cased', num_labels=2)
model_b.to(device)

model_b.to(device)
model_save_path = "LetAIEntertainYou/Models/persist/BERT_pointwise.pth"
model_b.load_state_dict(torch.load(model_save_path))
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

# Load and process data
data = pd.read_csv('LetAIEntertainYou/data/full_training_set.csv', delimiter=';', encoding="utf-8", na_filter=False)

pointwise_data = []

for index, row in data.iterrows():
    post = row['Posts']
    subject_line_a = row['Subject Line A']
    subject_line_b = row['Subject Line B']
    target = row['Target']

    if target == 'A':
        pointwise_data.append({'Post': post, 'Subject Line': subject_line_a, 'Label': 'Yes'})
        pointwise_data.append({'Post': post, 'Subject Line': subject_line_b, 'Label': 'No'})
    else:
        pointwise_data.append({'Post': post, 'Subject Line': subject_line_a, 'Label': 'No'})
        pointwise_data.append({'Post': post, 'Subject Line': subject_line_b, 'Label': 'Yes'})

# Convert to DataFrame
pointwise_df = pd.DataFrame(pointwise_data)
pointwise_df.head()


train, test = train_test_split(pointwise_df, test_size=0.2, random_state=42)

train_dataset = Dataset.from_pandas(train)

test_dataset = Dataset.from_pandas(test)
instruction ="Given a Post and a possible Subject Line for an E-Mail: Determine if the Subject Line is Engaging. Answer Yes or No only"
# Tokenize function
def tokenize_function(examples):
    concatenated = [instruction + '' +post + ' ' + subject for post, subject in zip(examples['Post'], examples['Subject Line'])]
    model_inputs = tokenizer(concatenated, padding='max_length', truncation=True)
    labels = [1 if label == 'Yes' else 0 for label in examples['Label']]
    model_inputs['labels'] = labels
    return model_inputs


train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)



train_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])
test_dataset.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])


train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=16)


# Initialize optimizer
optimizer = AdamW(model_b.parameters(), lr=1e-5)
#sollte eigentlich von der huggingface lib standardmäßig gest
#criterion = torch.nn.CrossEntropyLoss()
# siehe_ https://github.com/huggingface/transformers/blob/9aeacb58bab321bc21c24bbdf7a24efdccb1d426/src/transformers/modeling_bert.py#L1353-L1360
# Training loop
model_b.train()
for epoch in range(20):
    for batch_index, batch_data in enumerate(train_loader):
        ids = batch_data['input_ids'].to(device)
        mask = batch_data['attention_mask'].to(device)
        labels = batch_data['labels'].to(device)
        outputs = model_b(ids, mask, labels=labels)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch_index % 10 == 0:
            print(f"Epoch: {epoch}, Batch: {batch_index}, Loss: {loss.item()}")

print("Training complete")


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
    return accuracy


test_accuracy = evaluate_model(model_b, test_loader, device)
print(f"Test Accuracy: {test_accuracy:.2f}")


model_save_path = "LetAIEntertainYou/Models/persist/BERT_pointwise_20_epochs.pth"
torch.save(model_b.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")




df = pd.DataFrame(pointwise_df)
df["instruction"] = "Given a Post and a possible Subject Line for an E-Mail: Determine if the Subject Line is Engaging. Answer Yes or No only"
df["input"] = "Post: " + df["Post"] + " Subject Line: " + df["Subject Line"]
df = df[["instruction", "input", "Label"]]
df = df.rename(columns={"Label": "output"})
df['input'][1]

output_path= 'LetAIEntertainYou/data/for_llama3.csv'
df.to_csv(output_path, index=False)

print("CSV file has been saved to", output_path)




'''
dieser code wird benutzt,um den gewinner aus best of n zu ermitteln:
'''
data = pd.read_csv('LetAIEntertainYou/data/posts_best_of_n_complete.csv', delimiter=';', encoding="utf-8", na_filter=True)

#hier wird das pointwise genutzt, um rejection sampling aus 5 samples durchzuführen. das dauert einen moment...
def score_subject_lines(row):
    post = row['Posts']
    subject_lines = ['Subject Line A', 'Subject Line B', 'Subject Line C', 'Subject Line D', 'Subject Line E']

    scores = []
    for subject in subject_lines:
        text = post + ' ' + row[subject]
        inputs = tokenizer(text, return_tensors='pt', padding='max_length', truncation=True).to(device)
        with torch.no_grad():
            outputs = model_b(**inputs)
        scores.append(outputs.logits[0][1].item())

    max_index = scores.index(max(scores))
    winning_string = row[subject_lines[max_index]]
    words = winning_string.split()
    #wird im paper auch nachträglich für llm generierte subject lines gemacht
    if len(words) > 10:
        winning_string = ' '.join(words[:10]) + '...'
    return winning_string


data['Target'] = data.apply(score_subject_lines, axis=1)
data.to_csv('LetAIEntertainYou/data/rejection_results.csv', sep=';', encoding='utf-8', index=False)
