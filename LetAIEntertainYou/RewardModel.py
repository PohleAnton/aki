import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, GPT2Tokenizer, BertModel
import pandas as pd
import pickle

# Load the dataset
df_2 = pd.read_csv('LetAIEntertainYou/Posts/llama_und_base_judged.csv', delimiter=';')


# Initialize tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()

#embeddings für daten schon gemacht, können so geladen werden:
with open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_a.pkl', 'rb') as f:
    vector_a = pickle.load(f)

with open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_b.pkl', 'rb') as f:
    vector_b = pickle.load(f)

df_2['Vector A'] = [torch.tensor(v) for v in vector_a]
df_2['Vector B'] = [torch.tensor(v) for v in vector_b]
#ende des ladens

def text_to_vector(text):
    with torch.no_grad():
        text = str(text)
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.squeeze()

df_2['Vector A'] = df_2['Subject Line A'].apply(lambda x: text_to_vector(x).numpy())
df_2['Vector B'] = df_2['Subject Line B'].apply(lambda x: text_to_vector(x).numpy())


print('fertig')

with open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_a.pkl', 'wb') as f:
    pickle.dump(df_2['Vector A'].tolist(), f)

with open('LetAIEntertainYou/Posts/Vectors/llama_und_base/vector_b.pkl', 'wb') as f:
    pickle.dump(df_2['Vector B'].tolist(), f)
