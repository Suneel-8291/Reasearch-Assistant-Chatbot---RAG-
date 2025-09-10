import os
from dotenv import load_dotenv
import google.generativeai as genai
# Load .env file
load_dotenv()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Serper
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY not set. Add it to your .env file.")

if not SERPER_API_KEY:
    raise ValueError("⚠️ SERPER_API_KEY not set. Add it to your .env file.")
# Configure Gemini once, globally
genai.configure(api_key=GEMINI_API_KEY)