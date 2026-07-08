import os
from pathlib import Path

from langchain_chroma import Chroma
from agent_v2.embeddings import embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import SystemMessage, HumanMessage

from agent_v2.llm import llm


BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "chroma_db"
DATA_PATH = BASE_DIR / "data"






vectorstore = None


def load_documents():

    documents = []

    pdf_files = list(DATA_PATH.glob("*.pdf"))

    if not pdf_files:
        print("⚠️ No PDF files found in data folder.")
        return []

    for pdf in pdf_files:

        print(f"📄 Loading {pdf.name}")

        loader = PyPDFLoader(str(pdf))

        documents.extend(loader.load())

    return documents



def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    return splitter.split_documents(documents)




def get_vectorstore():

    global vectorstore


    # Already loaded
    if vectorstore is not None:
        return vectorstore


    # Load existing Chroma DB
    if os.path.exists(DB_PATH) and os.listdir(DB_PATH):

        print("📂 Loading existing Chroma database...")

        vectorstore = Chroma(
            persist_directory=str(DB_PATH),
            embedding_function=embeddings,
        )

        return vectorstore



    # Create new Chroma DB
    print("📄 Creating new Chroma database...")


    documents = load_documents()


    if not documents:
        return None


    chunks = split_documents(documents)


    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_PATH),
    )


    return vectorstore




def retrieve(query: str):

    store = get_vectorstore()


    if store is None:
        return "No documents available for retrieval."


    docs = store.similarity_search(
        query,
        k=10
    )


    return "\n\n".join(
        doc.page_content
        for doc in docs
    )



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
        )
    ]


    response = llm.invoke(messages)


    return {
        "messages": [response]
    }