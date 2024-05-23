import pandas as pd
import jsonlines
import openai
import time

file_path = 'Mappe1.xlsx'
df = pd.read_excel(file_path)


data = []
for _, row in df.iterrows():
    subject_a = row['Subject Line A']
    subject_b = row['Subject Line B']
    target = row['Target']

    if target == 'A':
        completion = 'A'
    else:
        completion = 'B'

    prompt = f"Which subject line is more engaging?\nA: {subject_a}\nB: {subject_b}\nAnswer:"
    data.append({"prompt": prompt, "completion": f" {completion}"})


with jsonlines.open('training_data.jsonl', mode='w') as writer:
    for entry in data:
        writer.write(entry)

openai.api_key = '...'


response = openai.File.create(
  file=open("training_data.jsonl"),
  purpose='fine-tune'
)

file_id = response['id']

# Fine-tune the model
fine_tune_response = openai.FineTune.create(
  training_file=file_id,
  model="davinci"
)


while True:
    status = openai.FineTune.retrieve(fine_tune_response['id'])
    print(f"Status: {status['status']}")
    if status['status'] == 'succeeded':
        break
    time.sleep(60)


fine_tuned_model_id = status['fine_tuned_model']


response = openai.Completion.create(
  model=fine_tuned_model_id,
  prompt="Which subject line is more engaging?\nA: Amazing deals just for you!\nB: Exclusive discounts available now!\nAnswer:",
  max_tokens=1
)

print(response['choices'][0]['text'].strip())