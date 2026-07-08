from dotenv import load_dotenv
load_dotenv()

import os

provider = os.getenv("LLM_PROVIDER", "ollama")

if provider == "gemini":
    from .llm_gemini import llm
else:
    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model="llama3.2",
        temperature=0,
        streaming=True,
    )