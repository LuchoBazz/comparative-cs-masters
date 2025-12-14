import time

from providers import ChatGPTModels, GoogleGeminiModels
from chatgpt import ChatGPT
from google_gemini import GoogleGemini
from utils import append_json_to_file

models = {
    ChatGPTModels.GPT_4O_MINI.value: ChatGPT(),
    ChatGPTModels.GPT_4O.value: ChatGPT(),
    ChatGPTModels.GPT_5_MINI.value: ChatGPT(),
    GoogleGeminiModels.FLASH_2_5.value: GoogleGemini(),
    GoogleGeminiModels.PRO_1_5.value: GoogleGemini(),
    GoogleGeminiModels.FLASH_2_0.value: GoogleGemini(),
}

output_file_path = "universities.json.output"

delay_between_requests = 1.0

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

prompt = """
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

default_value_university = '{{"university_name": "{university}", "status": "ERROR"}}'


def main():
    universities = [
        "University of Lisbon",
        "University of Porto",
        "University of Coimbra",
        "University of Minho",
        "University of Aveiro",
        "New University of Lisbon",
        "Polytechnic Institute of Lisbon",
        "University of Beira Interior",
        "Polytechnic Institute of Porto",
        "University Institute of Lisbon",
        "University of the Algarve",

        "University College Dublin",
        "Trinity College Dublin, University of Dublin",
        "University College Cork",
        "National University of Ireland, Galway",
        "Dublin City University",
        "University of Limerick",
        "Maynooth University",
        "Royal College of Surgeons in Ireland",
        "National University of Ireland, System",
        "Dublin Institute of Technology",
    ]

    # model = GoogleGeminiModels.FLASH_2_5.value
    model = ChatGPTModels.GPT_5_MINI.value
    client = models[model]
    client.initialize(model, system_content)
    print(model)

    for university in universities:
        print(f"Querying: {university}")
        default_value = default_value_university.format(university=university)

        json_str = client.run(prompt.format(university=university), default_value)
        append_json_to_file(output_file_path, json_str)
        time.sleep(delay_between_requests)

    print(f"All responses saved to {output_file_path}")


if __name__ == "__main__":
    main()
