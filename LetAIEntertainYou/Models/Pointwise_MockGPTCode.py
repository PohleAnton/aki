import pandas as pd
import jsonlines
import time
import openai

file_path = 'Mappe1.xlsx'
df = pd.read_excel(file_path)


data = []
for _, row in df.iterrows():
    subject_a = row['Subject Line A']
    subject_b = row['Subject Line B']
    target = row['Target']

    prompt_a = f"Context: Which subject line is more engaging?\nGenerated answer: A: {subject_a}\nIs this a good answer?"
    prompt_b = f"Context: Which subject line is more engaging?\nGenerated answer: B: {subject_b}\nIs this a good answer?"

    if target == 'A':
        data.append({"prompt": prompt_a, "completion": " Yes"})
        data.append({"prompt": prompt_b, "completion": " No"})
    else:
        data.append({"prompt": prompt_a, "completion": " No"})
        data.append({"prompt": prompt_b, "completion": " Yes"})


with jsonlines.open('training_data_pointwise.jsonl', mode='w') as writer:
    for entry in data:
        writer.write(entry)

openai.api_key = '...'

# Upload the file
response = openai.File.create(
  file=open("/mnt/data/training_data_pointwise.jsonl"),
  purpose='fine-tune'
)

file_id = response['id']

fine_tune_response = openai.FineTune.create(
  training_file=file_id,
  model="davinci"
)

import time

while True:
    status = openai.FineTune.retrieve(fine_tune_response['id'])
    print(f"Status: {status['status']}")
    if status['status'] == 'succeeded':
        break
    time.sleep(60)


fine_tuned_model_id = status['fine_tuned_model']

#gpt sagt, dass sollte funktionieren
response = openai.Completion.create(
  model=fine_tuned_model_id,
  prompt="Context: Which subject line is more engaging?\nGenerated answer: A: Amazing deals just for you!\nIs this a good answer?",
  max_tokens=1,
  logprobs=5
)

# diese könnte man dann für das rejection sampling nutzen
logprobs = response['choices'][0]['logprobs']['top_logprobs'][0]


