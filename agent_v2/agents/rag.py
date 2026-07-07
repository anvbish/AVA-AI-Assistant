import os
from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import SystemMessage, HumanMessage

from agent_v2.llm import llm

# ----------------------
# Paths
# ----------------------

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "chroma_db"

DATA_PATH = BASE_DIR / "data"
# ----------------------
# Embeddings
# ----------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# ----------------------
# Load PDF
# ----------------------

def load_documents():

    documents = []

    pdf_files = list(DATA_PATH.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the data folder.")

    for pdf in pdf_files:
        print(f"📄 Loading {pdf.name}")

        loader = PyPDFLoader(str(pdf))

        documents.extend(loader.load())

    return documents

# ----------------------
# Split Documents
# ----------------------

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    return splitter.split_documents(documents)

# ----------------------
# Build Vector Store
# ----------------------

def get_vectorstore():

    # If Chroma already exists, load it
    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):
        print("📂 Loading existing Chroma database...")

        return Chroma(
            persist_directory=str(DB_PATH),
            embedding_function=embeddings,
        )

    print("📄 Creating new Chroma database...")

    documents = load_documents()

    chunks = split_documents(documents)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_PATH),
    )

    return vectorstore


vectorstore = get_vectorstore()

# ----------------------
# Retrieval
# ----------------------

def retrieve(query: str):

    docs = vectorstore.similarity_search(query, k=10)

    return "\n\n".join(doc.page_content for doc in docs)

# ----------------------
# RAG Agent
# ----------------------

def rag_agent(state):

    question = state["messages"][-1].content

    context = retrieve(question)

    messages = [
        SystemMessage(
    content="""
    You are a RAG assistant.

    Answer ONLY using the provided context.

    Rules:
    - Never use outside knowledge.
    - Never make assumptions.
    - Never infer information that is not explicitly stated.
    - If the context contains enough information, answer normally.
    - If the user asks for a summary, summarize ONLY the provided context.
    - Only say "I don't know." when the context truly does not contain the answer.
    """
    ),
        HumanMessage(
            content=f"""
Context:

{context}

Question:

{question}
"""
        ),
    ]

    response = llm.invoke(messages)

    return {
    "messages": [response]
}