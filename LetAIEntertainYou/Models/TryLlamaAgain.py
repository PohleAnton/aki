import  pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from torch import no_grad
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AdamW, get_scheduler, \
    get_linear_schedule_with_warmup, LlamaForSequenceClassification, AutoModelForCausalLM, LlamaTokenizer, \
    BitsAndBytesConfig, BertForSequenceClassification, BertTokenizer
from torch.utils.data import DataLoader, RandomSampler
import bitsandbytes as bnb

from torch.cuda.amp import autocast, GradScaler

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

model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")

#für quantization, erlaubt leider kein freezing
# nf4_config = BitsAndBytesConfig(
#    load_in_4bit=True,
#    bnb_4bit_quant_type="nf4",
#    bnb_4bit_use_double_quant=True,
#    bnb_4bit_compute_dtype=torch.bfloat16
# )
model = LlamaForSequenceClassification.from_pretrained(model_id, num_labels=2).to(device)

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

#unfreeze one more layer
num_layers = len(model.model.layers)
for param in model.model.layers[num_layers - 1].parameters():
    param.requires_grad = True


optimizer = AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=2e-5)

num_training_steps = len(train_dataloader) * 3


lr_scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=num_training_steps)


model.train()
for epoch in range(1):
    total_loss = 0
    for batch in train_dataloader:
        optimizer.zero_grad()

        inputs, labels = batch['input_ids'], batch['labels']
        attention_mask = batch['attention_mask']
        outputs = model(input_ids=inputs, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        lr_scheduler.step()

        total_loss += loss.item()

    print(f"Epoch {epoch + 1}, Average Loss: {total_loss / len(train_dataloader)}")

model_save_path = "LetAIEntertainYou/Models/persist/llama_2_epoch_3.pth"
torch.save(model.state_dict(), model_save_path)
print(f"Model saved to {model_save_path}")


#vergleiche:
#bert untrained: 0.47
#bert trained, 20 epochs: 0.53

#das dataset für bert sieht anders aus, weil ich hier ein pre-processing für den autotrainer vorgenommen habe.
#funktional ist es aber identisch. test methode findet sich in Pointwise_BERT eval_model


device_l = torch.device( "cpu")
model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model_l = LlamaForSequenceClassification.from_pretrained(model_id, num_labels=2, ).to(device_l)
model_l.config.pad_token_id=model_l.config.eos_token_id
model_l_save_path="LetAIEntertainYou/Models/persist/llama_2_epoch_2.pth"
model_l.load_state_dict(torch.load(model_l_save_path))

def evaluate_model(model, dataloader, device):
    model.eval()  # Set model to evaluation mode
    true_labels = []
    predictions = []

    with torch.no_grad():  # No need to track gradients during evaluation
        for batch in dataloader:
            inputs, labels = batch['input_ids'].to(device), batch['labels'].to(device)
            attention_mask = batch['attention_mask'].to(device)

            outputs = model(input_ids=inputs, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1)

            predictions.extend(preds.detach().cpu().numpy())
            true_labels.extend(labels.detach().cpu().numpy())

    accuracy = accuracy_score(true_labels, predictions)
    return accuracy

# Calculate accuracy on the test set
accuracy = evaluate_model(model, test_dataloader, device)
print(f"Test Accuracy: {accuracy}")
