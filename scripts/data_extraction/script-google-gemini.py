import os
import json

from google import genai
from google.auth.exceptions import DefaultCredentialsError
from google.genai.errors import APIError
from dotenv import load_dotenv

load_dotenv()

def format_prompt(university):
    prompt = f'''
    UNIVERSITY_NAME: {university}
    Please research this university for me.
    I would like to pursue a Master's degree in Computer Science or related areas.
    I am an international Colombian student (NON-EU).

    Please summarize very briefly (not too much text) how much one year of this Master's program costs, and how much monthly accommodation costs at the university or in the city.
    Is it possible to complete the Master's in English?
    Provide the entire answer in English, with all amounts in euros.
    How many semesters does the Master's take to complete?
    Which English tests are required, and what English level is required (A1, A2, B1, B2, C1, C2)?
    Include official references with links.

    I would like you to research the following information using internet data from UNIVERSITY_NAME, from the university's official webpages, for admissions in 2026:

    * Is it possible to complete that Master's degree entirely in English?
    * If the previous answer is YES, what English level is required: A1, A2, B1, B2, C1, or C2?
    * How many semesters does the Master's require to be completed?
    * How much does one year of the Master's cost? All amounts in euros.
    * reference links, where I can verify only the tuition fee of the master's degree; I don't care about verifying the other fields, make sure the links work.

    Notes:

    * Only consider data from official pages.

    Analyze the data step by step.

    First, identify the values and then evaluate their correctness.

    Finally deliver the data in this JSON format:
    
    {{
      "university_name": "UNIVERSITY_NAME",
      "is_possible_in_english": true | false, # boolean
      "tuition_per_year_euro": 1000, # number
      "master_duration_semesters": 4, # number
      "language_proficiency_level": "B1" # enum: A1, A2, B1, B2, C1, C2,
      "tuition_fee_reference_links": ["link1", "link2"]
    }}
    

    The response should only be a JSON with the values above, nothing else and nothing unnecessary.
    I also do not want any comments explaining the code.
    '''

    print(prompt)

    return prompt


def run_gemini():
    try:
        client = genai.Client()

        print("✅ Connection successful. Generating content...")

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=format_prompt("Eotvos Lorand University")
        )

        print("\n--- Answer ---")
        answer = response.text.replace("```json", "").replace("```", "").strip()
        answer = answer.replace("\n", "")

        data = json.loads(answer)
        json_str = json.dumps(data)  

        with open("data.txt", "a", encoding="utf-8") as f:
            f.write(json_str + "\n")
        
        print(json_str)
        
        print()
        print("-------------")

    except DefaultCredentialsError:
        print("\n❌ ERROR: Missing Gemini API key.")
        print("Please make sure to set your key in the environment variable 'GEMINI_API_KEY'.")
        print("Example (Linux/macOS): export GEMINI_API_KEY=\"YOUR_KEY\"")
    except APIError as e:
        print(f"\n❌ Gemini API ERROR: {e}")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_gemini()
