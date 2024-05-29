import logging
import os

from datasets import Dataset
from huggingface_hub import login
from sklearn.model_selection import train_test_split
from torch.nn import CrossEntropyLoss
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, \
    AutoModelForCausalLM, TrainerCallback, LlamaForSequenceClassification, BertForSequenceClassification, BertTokenizer
import torch
import pandas as pd
from torch import device as torch_device, no_grad
from torch.utils.data import DataLoader

#still waiting for authorization...
#ist nur wichtig f. meta-llama/... - also NICHT für das hier verwendete tuning
token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
if token:
    print("Token is set successfully")
else:
    print("Token is not set")

# login(token)
# model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     torch_dtype=torch.bfloat16,
#     device_map="auto",
# )

# mit diesem model dauert alles EWIG!!!! - ich kann gar nicht genug ausrufezeichen dahinter machen
#model_id = "meta-llama/Meta-Llama-3-8B"
#anderes, auch zum erzeugen verwendetes model
model_id = "hiieu/Meta-Llama-3-8B-Instruct-function-calling-json-mode"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token




#device = torch_device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=2).to(device)
model.config.pad_token_id=model.config.eos_token_id
# ich hätte das gerne mit diesem modell (und das würde auch dem paper entsprechen, also das gleiche modell nehmen) gemacht - allerdings ist dabei mein computer explodiert - deswegen wird weiter unten bert trainiert:



data = pd.read_csv('LetAIEntertainYou/data/full_training_set.csv', delimiter=';', encoding="utf-8",
                   na_filter=False)
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




pointwise_df = pd.DataFrame(pointwise_data)
train_df, eval_df = train_test_split(pointwise_df, test_size=0.2, random_state=42)
train_dataset = Dataset.from_pandas(train_df)
eval_dataset = Dataset.from_pandas(eval_df)
def tokenize_function(examples):
    concatenated = [post + ' ' + subject for post, subject in zip(examples['Post'], examples['Subject Line'])]
    model_inputs = tokenizer(concatenated, padding='max_length', truncation=True)
    labels = [1 if label == 'Yes' else 0 for label in examples['Label']]
    model_inputs['labels'] = labels
    return model_inputs

train_tokenized = train_dataset.map(tokenize_function, batched=True)
eval_tokenized = eval_dataset.map(tokenize_function, batched=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#vor allem um zu bestätigen, dass das training überhaupt stattfindet
class CustomCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None and 'loss' in logs:
            logger.info(f"Step: {state.global_step}, Loss: {logs['loss']:.4f}")
        else:
            logger.info(f"Step: {state.global_step}, No loss available for this step.")


training_args = TrainingArguments(
    output_dir='LetAIEntertainYou/Models/results',
    eval_strategy='epoch',
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=4,
    logging_dir='./logs'
)

#trotz zahlreicher versuche bekomme ich immer noch eine Gpu fehlermeldung - daher hier nochmal explizit training auf Cpu verlagert

def data_collator(features):
    batch = tokenizer.pad(
        features,
        padding=True,
        return_tensors="pt",
    )
    batch = {k: v.to(device) for k, v in batch.items()}
    return batch


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized,
    eval_dataset=eval_tokenized,
    data_collator=data_collator,
    callbacks=[CustomCallback()],
)

trainer.train()

# das *sollte* funktionieren. ich habe hier nach knapp vier stunden zwar keine fehlermeldung (fortschritt) - aber bin leider
#immer noch bei 0 % - wir nehmen deswegen BERT. siehe Pointwise_BERT.py
# so lame