from enum import Enum
import os
import time
import json

from openai import OpenAI
from dotenv import load_dotenv
import tiktoken

load_dotenv()


class ChatGPTModels(Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O = "gpt-4o"


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

universities = [
    "Universidad Nacional de Colombia",
    "Universidad de Buenos Aires",
    "Universidad Complutense de Madrid",
    "Universidad de Chile",
]

prompt_template = """
UNIVERSITY_NAME: {university}

Please research this university's Master's programs in Computer Science or related areas. 
I am an international Colombian student (NON-EU), looking for admissions in 2026.

Focus only on:
- If the Master's can be fully completed in English.
- The required English proficiency level (A1, A2, B1, B2, C1, or C2).
- The program's duration in semesters.
- The tuition cost per year (convert and report in EUR).
- Official tuition fee reference links (max 3, must be working links).

Only consider official university sources.
"""


output_file_path = "universities.txt"

system_content = """
You are a web-research assistant. Use ONLY official university webpages (official university domains or official government/education portals) to find up-to-date information for the admissions year 2026 about the specified university. Follow these rules exactly:

1) Retrieve and confirm these fields from official sources: 
   - whether the Master's can be completed entirely in English (boolean),
   - tuition per year (converted to EUR as a NUMBER),
   - master duration in semesters (NUMBER),
   - required English proficiency level (one of: A1, A2, B1, B2, C1, C2 or None),
   - up to 2 official URLs that explicitly verify the tuition fee.

2) Convert any tuition/fee amounts to euros using a current, authoritative exchange rate (e.g., ECB) and round to the nearest euro. If the page lists tuition per semester, convert to per year.

3) If a value cannot be strictly confirmed on official pages, set it to null (for numeric/string fields). Set "is_possible_in_english" to false if you cannot confirm it.

4) Output ONLY a single VALID JSON object that matches this schema exactly (no extra keys, no comments, no explanation, no markdown):

{
  "university_name": "UNIVERSITY_NAME",
  "is_possible_in_english": true | false,
  "tuition_per_year_euro": 1000 | null,
  "master_duration_semesters": 4 | null,
  "language_proficiency_level": "B1" | null,
  "tuition_fee_reference_links": ["https://...","https://..."]
}

5) The final output must be in English. Numeric fields must be numbers (no currency symbols), booleans must be true/false, links must be absolute HTTPS URLs.

6) Do NOT output any other text or explanation. Perform your step-by-step analysis internally but do not show it. Be concise and deterministic.
"""

system_message = {
    "role": "system",
    "content": system_content,
}

delay_between_requests = 1.0


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


def query_university(university: str, model: str) -> str:
    user_prompt = prompt_template.format(university=university)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[system_message, {"role": "user", "content": user_prompt}],
            stream=False,
        )
        content = response.choices[0].message.content
        return clean_content(content)
    except Exception as e:
        print(f"[ERROR] UnknownException | university={university}")
        return '{"university_name": "{university}", "status": "ERROR"}'.format(
            university=university
        )


def main():
    total_tokens = 0

    model = ChatGPTModels.GPT_4O_MINI.value

    for university in universities:
        print(f"Querying: {university}")
        answer = query_university(university, model)
        user_prompt = prompt_template.format(university=university)
        total_tokens += count_tokens(user_prompt, model)
        json_str = parse_and_dump_json(answer)
        append_json_to_file(output_file_path, json_str)
        time.sleep(delay_between_requests)

    print(f"All responses saved to {output_file_path}")
    print(f"[INFO] Model {model} / Total Tokens used: {total_tokens}")


if __name__ == "__main__":
    main()

# black scripts/data_extraction/script-chatgpt.py
# python scripts/data_extraction/script-chatgpt.py
