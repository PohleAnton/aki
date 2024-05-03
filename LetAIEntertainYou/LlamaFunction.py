from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "mzbac/llama-3-8B-Instruct-function-calling-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",

)

tool = {
            "name": "search_web",
            "description": "Perform a web search for a given search terms.",
            "parameter": {
                "type": "object",
                "properties": {
                    "search_terms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The search queries for which the search is performed.",
                    "required": True,
                    }
                }
            },
        }

messages = [
            {
                "role": "system",
                "content": f"You are a helpful assistant with access to the following functions. Use them if required - {str(tool)}",
            },
            {"role": "user", "content": "Today's news in Melbourne, just for your information, today is April 27, 2014."},
        ]

input_ids = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt"
).to(model.device)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

outputs = model.generate(
    input_ids,
    max_new_tokens=256,
    eos_token_id=terminators,
    do_sample=True,
    temperature=0.1,
)
response = outputs[0]
print(tokenizer.decode(response))

# <|begin_of_text|><|start_header_id|>system<|end_header_id|>

# You are a helpful assistant with access to the following functions. Use them if required - {'name':'search_web', 'description': 'Perform a web search for a given search terms.', 'parameter': {'type': 'object', 'properties': {'search_terms': {'type': 'array', 'items': {'type':'string'}, 'description': 'The search queries for which the search is performed.','required': True}}}}<|eot_id|><|start_header_id|>user<|end_header_id|>

# Today's news in Melbourne, just for your information, today is April 27, 2014.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

# <functioncall> {"name": "search_web", "arguments": {"search_terms": ["Melbourne news", "April 27, 2014"]}}<|eot_id|>
