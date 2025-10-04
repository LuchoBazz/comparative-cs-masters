import tiktoken

prompt = "Some Prompt"
enc = tiktoken.encoding_for_model("gpt-4o")

prompt_encoded = enc.encode(prompt)
tokens_number = len(prompt_encoded)

print(tokens_number)
print(prompt_encoded)