import openai
import yaml
import json
import os
import csv
import random
import re

from LetAIEntertainYou.DataGen import entries

examples = entries
#entries_small = random.sample(entries, 5)
#these_examples = "\n".join(f"{index + 1}. {string}" for index, string in enumerate(entries_small))
output_dir = "./LetAIEntertainYou/Posts/Text"
os.makedirs(output_dir, exist_ok=True)
csv_filename = "./LetAIEntertainYou/Posts/posts.csv"
file_exists = os.path.isfile(csv_filename)

openai.api_key = yaml.safe_load(open("./LetAIEntertainYou/config.yml")).get('KEYS', {}).get('openai')
model = 'gpt-4-turbo-2024-04-09'
model_dev = 'gpt-3.5-turbo-0125'

functions = [
    {
        "name": "write_posts",
        "description": "A function that writes this_count number of posts for a neighbourhood website based on these_examples, following certain these_instructions ",
        "parameters": {
            "type": "object",
            "properties": {
                "posts": {
                    "type": "array",
                    "description": "A list that contains this_count number of posts",
                    "items": {
                        "type": "string",
                        "description": "The post that was written following these_instructions, loosely based on these_examples "
                    }
                }
            },
            "required": ["this_count", "these_examples", "these instructions"]
        }
    },
    {
        "name": "write_posts_2",
        "description": "A function that writes this_count number of posts for a neighbourhood website following certain these_instructions ",
        "parameters": {
            "type": "object",
            "properties": {
                "posts": {
                    "type": "array",
                    "description": "A list that contains this_count number of posts",
                    "items": {
                        "type": "string",
                        "description": "The post that was written following these_instructions"
                    }
                }
            },
            "required": ["this_count", "these instructions"]
        }
    },

    {
        "name": "write_posts_3",
        "description": "A function that writes number_of_posts posts for a neighbourhood website in the style and length of these_examples ",
        "parameters": {
            "type": "object",
            "properties": {
                "posts": {
                    "type": "array",
                    "description": "A list that contains number_of_posts posts",
                    "items": {
                        "type": "string",
                        "description": "The post that was written,  loosely based on these_examples in length and style"
                    }
                }
            },
            "required": ["these_examples", "number_of_posts"]
        }
    },
    {
        "name": "write_posts_4",
        "description": "A function that writes number_of_posts posts for a neighbourhood website in the style and length of these_examples ",
        "parameters": {
            "type": "object",
            "properties": {
                "posts": {
                    "type": "array",
                    "description": "A list that contains number_of_posts posts",
                    "items": {
                        "type": "string",
                        "description": "The post that was written,  loosely based on these_examples in length and style, following these_instructions"
                    }
                }
            },
            "required": ["these_examples", "number_of_posts", "these_instructions"]
        }
    }
]

these_instructions = """
1. Create Diverse Content: Produce various types of posts such as lost and found notices, event announcements, volunteer calls, service offerings, public service announcements, and casual community meet-ups to mirror the diversity of topics found in a community setting.
2. Use an Informal Tone: Adopt a conversational and informal tone in your posts to make them feel personal and approachable, similar to the way a neighbor might communicate. This approach helps build a sense of community and makes the information more accessible.
3. Include Specific Details: Ensure each post contains specific details like times, locations, or identifiable items (e.g., "a pair of prescription glasses at the bus stop on 5th and Main"). This specificity makes the posts realistic, useful, and actionable.
4. Incorporate a Call to Action: Embed a direct call to action in many posts, encouraging community engagement. This could involve requests for information (e.g., sightings of a missing pet), invitations to events, or prompts to join activities or groups.
5. Vary Post Length and Complexity: Adjust the length and complexity of the posts to reflect the natural variation seen in a community bulletin board or social media feed. Some posts should be concise and straightforward, while others might offer more detailed explanations or background to engage readers further.
6. Describe Relatable Scenarios: Focus on scenarios that are commonly experienced in many communities, such as local events, school activities, and neighborhood issues. This ensures that the posts are relatable and realistically grounded.
7. Avoid flashy, 3 word introductions
"""
number_of_posts = 30
posts = []


# test = openai.ChatCompletion.create(
#     model=model,
#     messages=[
#         {'role': 'user',
#          'content': f"write_posts based on {these_examples}, following {these_instructions}. Write {this_count} number of posts"}
#     ],
#     functions=functions,
#     function_call={'name': 'write_posts'}
# )
#
# argument_string_3 = test['choices'][0]['message']['function_call']['arguments']


# test = openai.ChatCompletion.create(
#         model=model,
#         messages=[
#             {'role': 'user',
#              'content': f"write_posts_2 following {these_instructions}. Write {this_count} number of posts"}
#         ],
#         functions=functions,
#         function_call={'name': 'write_posts_2'}
#     )
# argument_string_prod = test['choices'][0]['message']['function_call']['arguments']
# data = json.loads(argument_string_prod)

def fetch_reponse():
    #take new examples each time
    entries_small = random.sample(entries, 5)
    these_examples = "\n".join(f"{index + 1}. {string}" for index, string in enumerate(entries_small))

    test = openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role': 'user',
             'content': f"write_posts_3 based on {these_examples}. Write {number_of_posts} posts"}
        ],
        functions=functions,
        function_call={'name': 'write_posts_3'}
    )
    argument_string_prod = test['choices'][0]['message']['function_call']['arguments']
    data = json.loads(argument_string_prod)
    return data


def append_posts(data):
    for post in data["posts"]:
        posts.append(post)


def clean_strings(string_list):
    cleaned_list = []
    for content in string_list:
        # Check if the string starts with a number followed by '.'
        if re.match(r'^\d+\.', content):
            # Remove the number and the dot, and any spaces immediately after
            content = re.sub(r'^\d+\.\s*', '', content)
        cleaned_list.append(content)
    return cleaned_list


def find_highest_index(directory):
    highest = 0
    for filename in os.listdir(directory):
        if filename.startswith("file_") and filename.endswith(".txt"):
            index_part = filename[5:-4]  # Extract the number from "file_1.txt"
            if index_part.isdigit():
                highest = max(highest, int(index_part))
    return highest


def persist_posts(posts_cleaned_up, starting_index_calc):
    for index, string in enumerate(posts_cleaned_up, start=starting_index_calc + 1):
        filename = os.path.join(output_dir, f"file_{index}.txt")
        with open(filename, 'w') as file:
            file.write(string)

    with open(csv_filename, 'a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['String'])

        for string in posts_cleaned_up:
            writer.writerow([string])
    print('done')
    #posts_clean=[]


# def read_files_in_directory(directory):
#     all_texts = []
#     for filename in os.listdir(directory):
#         if filename.endswith(".txt"):
#             file_path = os.path.join(directory, filename)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as file:
#                     content = file.read().strip()
#             except UnicodeDecodeError:
#                 # Try reading with a different encoding if UTF-8 fails
#                 with open(file_path, 'r', encoding='windows-1252') as file:
#                     content = file.read().strip()
#
#             # Check if the content starts with a number followed by '.'
#             if re.match(r'^\d+\.', content):
#                 # Remove the number and the dot
#                 content = re.sub(r'^\d+\.\s*', '', content)
#             all_texts.append(content)
#     return all_texts
#
# directory_path = './LetAIEntertainYou/Posts/Text'
# texts = read_files_in_directory(directory_path)

#be VERY careful with the range!
for _ in range(10):
    mocks = fetch_reponse()
    append_posts(mocks)
print('done')

posts_clean = clean_strings(posts)
starting_index = find_highest_index(output_dir)
persist_posts(posts_clean, starting_index)
