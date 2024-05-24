import  pandas as pd

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

df.to_csv('LetAIEntertainYou/data/for_llama3_appended.csv', index=False)