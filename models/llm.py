import google.generativeai as genai

def ask_gemini(prompt: str, model: str = "models/gemini-1.5-flash") -> str:
    llm = genai.GenerativeModel(model)
    response = llm.generate_content(prompt)
    return response.text
