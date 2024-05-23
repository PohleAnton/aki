import os
import pandas as pd
import torch
from torch.nn import MSELoss
from torch.utils.data import DataLoader, Dataset
from torch.optim import AdamW
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv('LetAIEntertainYou/Models/posts_rules_base_judged_neu.csv', delimiter=';', encoding="utf-8",
                   na_filter=False)
data.reset_index(drop=True, inplace=True)

# Define the model and tokenizer

# Load the configuration of BERT and modify it for regression
config = BertConfig.from_pretrained('bert-base-uncased')
config.num_labels = 1  # Change from classification to regression (scalar output)

# Load BERT with the modified configuration
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', config=config)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


class SubjectLineDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_len):
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __getitem__(self, index):
        # Calculate which post and which subject line we're dealing with
        row_idx = index // 2
        line_idx = index % 2  # 0 for Subject Line A, 1 for Subject Line B

        post = self.data.iloc[row_idx]['Posts']
        subject_line = self.data.iloc[row_idx][f'Subject Line {"A" if line_idx == 0 else "B"}']
        target = self.data.iloc[row_idx]['Target']

        # Assign score based on the target column
        score = 1.0 if (target == 'A' and line_idx == 0) or (target == 'B' and line_idx == 1) else 0.0

        # Build the prompt text based on which subject line is being evaluated
        prompt_text = f"Text: {post} Subject line: {subject_line} Is this an excellent subject line? An excellent subject line is coherent, informative, and engaging."

        encoding = self.tokenizer.encode_plus(
            prompt_text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'score': torch.tensor(score, dtype=torch.float)
        }

    def __len__(self):
        return len(self.data) * 2


# Data preparation
max_len = 256  # Increased to accommodate longer texts
batch_size = 16

# Split the data into train and test sets
train_data, test_data = train_test_split(data, test_size=0.1)
train_dataset = SubjectLineDataset(train_data, tokenizer, max_len)
test_dataset = SubjectLineDataset(test_data, tokenizer, max_len)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# Setting device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Optimizer
optimizer = AdamW(model.parameters(), lr=5e-5)
criterion = MSELoss()

# Training loop
model.train()
for epoch in range(4):  # Adjust the number of epochs according to your need
    total_loss = 0
    for batch in train_loader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        scores = batch['score'].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits.squeeze()  # Get the logits

        loss = criterion(logits, scores)  # Calculate the MSE loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    # Calculate average loss over the entire training loader
    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1}, Loss: {avg_loss:.4f}")

# Save the model to a directory
model_save_path = 'LetAIEntertainYou/Models/persisted_pointwise/model'
model.save_pretrained(model_save_path)
tokenizer_save_path = 'LetAIEntertainYou/Models/persisted_pointwise/tokenizer'
tokenizer.save_pretrained(tokenizer_save_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
untrained_model = BertForSequenceClassification(config)
untrained_model.to(device)
untrained_model.eval()
# Evaluate the model
def predict_scores(model, post, subject_line):
    prompt_text = f"Text: {post} Subject line: {subject_line} Is this an excellent subject line? An excellent subject line is coherent, informative, and engaging."
    with torch.no_grad():
        inputs = tokenizer(prompt_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(device) for k, v in inputs.items()}  # Move inputs to the correct device
        outputs = model(**inputs)
        predicted_score = outputs.logits.squeeze()
    return predicted_score.item()


test_results = []

# Loop over each row in the test set and calculate scores for Subject Line A and B
for idx, row in test_data.iterrows():
    post = row['Posts']
    subject_line_a = row['Subject Line A']
    subject_line_b = row['Subject Line B']

    # Predict scores
    score_a = predict_scores(untrained_model, post, subject_line_a)
    score_b = predict_scores(untrained_model, post, subject_line_b)

    # Determine the winner
    predicted_winner = 'A' if score_a > score_b else 'B'
    actual_winner = row['Target']

    # Append the result to the list
    test_results.append((idx, predicted_winner, actual_winner, score_a, score_b))

# Convert test results to a DataFrame for better visualization
test_results_df = pd.DataFrame(test_results,
                               columns=['Index', 'Predicted Winner', 'Actual Winner', 'Score A', 'Score B'])

# Calculate accuracy
correct_predictions = sum(test_results_df['Predicted Winner'] == test_results_df['Actual Winner'])
accuracy = correct_predictions / len(test_results_df)
print(f"Accuracy on test set: {accuracy:.4f}")
# List to store the results
results = []

# Loop over each row and calculate scores for Subject Line A and B
for idx, row in data.iterrows():
    post = row['Posts']
    subject_line_a = row['Subject Line A']
    subject_line_b = row['Subject Line B']

    # Predict scores
    score_a = predict_scores(post, subject_line_a)
    score_b = predict_scores(post, subject_line_b)

    # Determine the winner
    winner = 'A' if score_a > score_b else 'B'

    # Append the result to the list
    results.append((idx, winner, score_a, score_b))

# Convert results to a DataFrame for better visualization
results_df = pd.DataFrame(results, columns=['Index', 'Winner', 'Score A', 'Score B'])

# Print the results
print(results_df)