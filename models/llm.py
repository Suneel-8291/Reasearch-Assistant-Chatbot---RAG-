import google.generativeai as genai


def ask_gemini(prompt: str, model: str = "gemini-2.0-flash") -> str:
    try:
        llm = genai.GenerativeModel(model)
        response = llm.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"LLM Error: {str(e)}"
