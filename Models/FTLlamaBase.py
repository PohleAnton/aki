import pandas as pd
import torch
from datasets import Dataset
from huggingface_hub import login
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer,  AdamW, \
    get_linear_schedule_with_warmup, LlamaForSequenceClassification
from torch.utils.data import DataLoader, RandomSampler
import os

df=pd.read_csv('LetAIEntertainYou/data/for_llama3.csv')

text_col=[]
for  _, row in df.iterrows():
    prompt= 'Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request\n\n'
    instruction = str(row['instruction'])
    input_query = str(row['input'])
    response = str(row['output'])

    text=prompt + "### Instruction: " + instruction + "\n###Response:\n" + response

    text_col.append(text)

df.loc[:, "text"] = text_col
print(df.head())

df.to_csv('LetAIEntertainYou/data/data.csv', index=False)

df_first_50_rows = df.head(50)

# Save the result to a new CSV file
output_path = 'LetAIEntertainYou/data/test/data_small.csv'  # Replace with the desired output path
df_first_50_rows.to_csv(output_path, index=False)

''''
with this, 
autotrain llm --train --project-name my-llm --model hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode --data-path LetAIEntertainYou/data/test --peft --quantization int4 --lr 2e-4 --batch-size 8 --epochs 1 --trainer sft

kann das model trainiert werden - ich haben einen testdatensatz mit 50 v. 5000 einträgen versucht, das soll 11 stunden dauern. deswegen versuche ich mal etwas anderes...

'''

df=df.drop(columns='instruction')
df['text']=df['input']
df['label']=df['output']
df['text']=df['text'].astype(str)
df=df.drop(columns=['input','output' ])

df_first_50_rows = df.head(50)

##df_first_50_rows.loc[:, 'label'] = df_first_50_rows['label'].apply(lambda x: 1 if x == 'Yes' else 0)


#benötigt ein huggingface token
token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
if token:
    print("Token is set successfully")
else:
    print("Token is not set")

login(token)
device=torch.device("cpu")
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
model = LlamaForSequenceClassification.from_pretrained(model_id, num_labels=2, local_files_only=True).to(device)
model.config.pad_token_id=model.config.eos_token_id
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

model.config.pad_token_id=model.config.eos_token_id
#wichtig für freezing
classifier_head = model.score
def tokenize_function(examples):
    model_inputs = tokenizer(examples['text'], padding='max_length', truncation=True, max_length=512)
    labels = [1 if label == 'Yes' else 0 for label in examples['label']]
    model_inputs['labels'] = labels
    return model_inputs


train_df, test_df = train_test_split(df_first_50_rows, test_size=0.2, random_state=42)

train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

train_tokenized = train_dataset.map(tokenize_function, batched=True)
test_tokenized = test_dataset.map(tokenize_function, batched=True)
train_tokenized.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])
test_tokenized.set_format(type='torch', columns=['input_ids', 'attention_mask', 'labels'])


batch_size = 8


train_dataloader = DataLoader(train_tokenized, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_tokenized, batch_size=batch_size, shuffle=False)
for param in model.parameters():
    param.requires_grad = False


for param in model.score.parameters():
    param.requires_grad = True

print(model.model.layers)




optimizer = AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=2e-5)

num_training_steps = len(train_dataloader) * 3


lr_scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=num_training_steps)
criterion = torch.nn.CrossEntropyLoss()

model.train()

for epoch in range(1):
    total_loss = 0
    for batch in train_dataloader:
        optimizer.zero_grad()

        inputs, labels = batch['input_ids'], batch['labels']
        attention_mask = batch['attention_mask']
        outputs = model(input_ids=inputs, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss if 'loss' in outputs else criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        total_loss += loss.item()

    print(f"Epoch {epoch + 1}, Average Loss: {total_loss / len(train_dataloader)}")

model_save_path = "LetAIEntertainYou/Models/persist/llama_base_ft.pth"
torch.save(model.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")

import pickle


def load_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def tokenize_text(text, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.tokenize(text)
    return tokenizer, tokens


def save_to_pickle(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)


def main(text_file_path, model_name, output_file_path):
    # Load text from file
    text = load_text_file(text_file_path)

    # Tokenize text
    tokenizer, tokens = tokenize_text(text, model_name)

    # Gather results
    results = {
        'file_name': text_file_path,
        'tokenizer_name': model_name,
        'number_of_tokens': len(tokens),
    }

    # Save results to pickle file
    #save_to_pickle(results, output_file_path)

    # Optional: Display results
    print(f"File Name: {results['file_name']}")
    print(f"Tokenizer Name: {results['tokenizer_name']}")
    print(f"Number of Tokens: {results['number_of_tokens']}")

# Define file paths and model name
text_file_path = 'LetAIEntertainYou/Models/t.txt'  # Replace with your text file path
model_name = model_id # Replace with your chosen model name
output_file_path = 'corpus_total_tokencount.pkl'  # Output pickle file path

# Run the main function
main(text_file_path, model_name, output_file_path)

os.getcwd()