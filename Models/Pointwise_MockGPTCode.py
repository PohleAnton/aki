import pandas as pd
import jsonlines
import time
import openai


openai.api_key = '...'

# Upload the file
response = openai.File.create(
  file=open("LetAIEntertainYou/data/pointwise.jsonl"),
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


