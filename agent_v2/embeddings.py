from dotenv import load_dotenv
load_dotenv()

import os

provider = os.getenv("LLM_PROVIDER", "ollama")

if provider == "gemini":
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

else:
    from langchain_ollama import OllamaEmbeddings

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
    )