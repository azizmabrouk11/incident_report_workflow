import google.generativeai as genai
import os

def embed_text(text: str) -> list[float]:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return response["embedding"]
