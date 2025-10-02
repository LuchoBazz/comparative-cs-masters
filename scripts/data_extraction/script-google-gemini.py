import os
from google import genai
from google.auth.exceptions import DefaultCredentialsError
from google.genai.errors import APIError
from dotenv import load_dotenv

load_dotenv()

def run_gemini():
    try:
        client = genai.Client()

        print("✅ Connection successful. Generating content...")

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Write a short poem about the sun.'
        )
        print("\n--- Answer ---")
        print(response.text)
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