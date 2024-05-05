from gpt4all import GPT4All
model = GPT4All('Meta-Llama-3-8B-Instruct.Q4_0.gguf')
prompt = 'Who won the world cup soccer in 2014?'
output = model.generate("<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n" + prompt +
                        "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n", max_tokens=1000, temp=0.6)
print(output)
