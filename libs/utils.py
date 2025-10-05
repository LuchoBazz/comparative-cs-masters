import tiktoken
import json


def clean_content(content: str) -> str:
    content = content.replace("```json", "").replace("```", "").strip()
    content = content.replace("\n", "")
    return content


def parse_and_dump_json(answer: str) -> str:
    data = json.loads(answer)
    json_str = json.dumps(data)
    return json_str


def append_json_to_file(output_file_path: str, json_str: str) -> None:
    with open(output_file_path, mode="a", encoding="utf-8") as file:
        file.write(json_str + "\n")


def count_tokens(prompt: str, model: str) -> int:
    enc = tiktoken.encoding_for_model(model)
    prompt_encoded = enc.encode(prompt)
    tokens_number = len(prompt_encoded)

    print(f"[INFO] Model {model} / Tokens used: {tokens_number}")
    return tokens_number
