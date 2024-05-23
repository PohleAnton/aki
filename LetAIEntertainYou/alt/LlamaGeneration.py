'''
altes setup. letztlich wurde Llama3SubjectLines.py verwendet
'''


import json
import os

import openai
from groq import Groq
from dotenv import load_dotenv
import time
import pandas as pd


def gen_llama(row):
    try:
        print("Input: " + str(row))
        start = time.perf_counter()

        """
        prompt = (f'Please write a baseline for the following post:\n\n {row} \n\n')
        output = model.generate(
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>"

            f"{set_of_instruction}<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>"

            f"{prompt}<|eot_id|>"
            f"<|start_header_id|>assistant<|end_header_id|>", max_tokens=1000, temp=0.6)

        print("Output: " + output)
        return output
        """
        """
        # Build the Request
        api_request_json = {
            'model': 'llama-13b-chat',
            'functions': [
                {
                    "name": "write_subject_lines",
                    "description": "A function that outputs the most interesting phrase for every enumerated entry in a provided_string following a set_of_instruction while keeping the original order",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "subject_line": {
                                "type": "string",
                                "description": "The generated subject line"
                            }
                        },
                        "required": ["provided_string", "set_of_instruction"]
                    }
                }
            ],
            'function_call': {'name': 'write_subject_lines'},
            'messages': [
                {'role': 'user',
                 'content': f"Please write a baseline for the following post:\n\n {row}.\n\n Write according to {set_of_instruction}."}],
        }

        functions = [
                {
                    "name": "write_subject_lines",
                    "description": "A function that outputs the most interesting phrase for every enumerated entry in a provided_string following a set_of_instruction while keeping the original order",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "subject_line": {
                                "type": "string",
                                "description": "The generated subject line"
                            }
                        },
                        "required": ["provided_string", "set_of_instruction"]
                    }
                }
            ]

        api_request_json = {
            "messages": [
                {'role': 'user',
                 'content': f"Write a subject line for the following post: \n\n {str(row)} \n\n Write according to the following rules: \n\n {set_of_instruction}."}
            ],
            "functions": functions,
            "function_call": {'name': 'write_subject_lines'}
        }

        # Execute the Request
        response = llama.run(api_request_json)

        # Save the answer
        data = response.json()['choices'][0]['message']['function_call']['arguments']
        try:
            output = data["subject_line"]
        except Exception as e:
            output = data
        #output = response.json()['choices'][0]['message']['function_call']['arguments']['subject_line']

        print(output)
        stop = time.perf_counter()
        print(f"Seconds passed: {stop - start:0.4f}")

        return output
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You are a  LLM that generates a subject line for a given post while following the following set of rules: \n\n {set_of_instruction} \n\n Your Output is only the generated subject line without any further comments."
                },
                {
                    "role": "user",
                    "content": f"Please generate a subject line for the following post: \n\n {row} \n\n Based on the following set of rules: \n\n {set_of_instruction}",
                }
            ],
            model="llama3-8b-8192",
        )

        output = chat_completion.choices[0].message.content
        print("Output: " + output)
        stop = time.perf_counter()
        print(f"Seconds passed: {stop - start:0.4f}")

        if len(output.split(" ")) > 10:
            output = ' '.join(output.split(" ")[0:10]) + '...'

        global i

        i += 1
        if i >= 30:
            time.sleep(61)
            i = 1

        return output
    except Exception as e:
        return ""


def gen_chatgpt_based(row):
    try:
        print("Input: " + str(row))
        start = time.perf_counter()

        functions = [
            {
                "name": "write_subject_lines",
                "description": "A function that outputs the most interesting phrase for a given post following a set_of_instruction",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject_line": {
                            "type": "string",
                            "description": "A generated subject line"
                        }
                    },
                    "required": ["row", "set_of_instruction"]
                }
            }
        ]

        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0125',
            messages=[
                {'role': 'user',
                 'content': f"write_subject_lines for the following post: \n\n {row} \n\n Write according to the following set of instructions: \n\n {set_of_instruction}"}
            ],
            functions=functions,
            function_call={'name': 'write_subject_lines'}
        )
        output = json.loads(response['choices'][0]['message']['function_call']['arguments'])['subject_line']

        print("Output: " + output)
        stop = time.perf_counter()
        print(f"Seconds passed: {stop - start:0.4f}")

        if len(output.split(" ")) > 10:
            output = ' '.join(output.split(" ")[0:10]) + '...'

        return output
    except Exception as e:
        return ""


def gen_rule_based(row):
    return ' '.join(row.split(" ")[0:10]) + '...'


# model = GPT4All('Meta-Llama-3-8B-Instruct.Q4_0.gguf')
# llama = LlamaAPI("LL-nGmL3RPSzqGWilWDPoUuQ51hdsuIo1TBg8ls576gZMj4h5KfYwztRts46qxdxnnA")

load_dotenv()
client = Groq(api_key=os.getenv('LLAMA_ACCESS_KEY'))
MODEL = 'llama3-8b-8192'

openai.api_key = os.getenv('OPENAI_ACCESS_KEY')

set_of_instruction = """
    We will send an email containing a post from a Nextdoor user. We want to use the most interesting part of the post as an email subject line.
    Task description: Given a post, output the most interesting phrase in the post.
    Here are the requirements:
    1. Extract the phrase as-is. Do not change any single character.
    2. Do not paraphrase. Copy the exact phrase. If the phrase you selected has stop words like "but", "and", "the", keep them in the output.
    3. Do not insert or remove any word.
    4. If you cannot choose the most interesting phrase, return the first 10 words of the post.
    5. Try to keep it within 10 words. If you cannot complete within 10 words, generate an incomplete line with "..."
    6. Put the most important words in the beginning.
    7. If the first 10 words of the post contain unique and interesting words, reuse it.
    8. Make a subject line that brings curiosity. If the subject line gets too long, cut the phrase before the last part. For example, if the post has "Yesterday, my son found a dog barking at other people", output "Yesterday, my son found a dog barking at ..."
    9. If the first 10 words of the post contain informal words, you can keep these words in the subject line. We want to respect the post content in the subject line.
    10. If the post has a phrase starting with "I" in the first 10 words, please use the same words in the subject line. It will make the subject line more personal. For example, if the post has "Hi All, I left my phone", use "I left my phone" in the subject line.
    11. If the some part of the post is all capitals, it is okay to extract that part. That part is what user wanted to emphasize. For example, extract all capital phrases like "CRIME ALERT".
    12. Do not use people’s names in the subject line.
    13. Do not add "Subject line:" in the output. Just output the content of the subject line.
    14. Capitalize the first character of the subject line. If the part you selected starts with a lower-cased character, capitalize the character.
    """

csv = pd.read_csv("../Posts/llama.csv", encoding='utf-8-sig', sep=";")

i = 1
#csv["Llama Baseline"] = csv.loc[:, "Posts"].apply(gen_llama)
#csv["Rule-based Baseline"] = csv.loc[:, "Posts"].apply(gen_rule_based)
csv["ChatGPT-3.5-Turbo Baseline"] = csv.loc[:, "Posts"].apply(gen_chatgpt_based)

csv.to_csv(path_or_buf='../Posts/llama_und_ChatGPT.csv', index=False, encoding='utf-8-sig', sep=";")
