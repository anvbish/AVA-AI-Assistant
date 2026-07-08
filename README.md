# 🤖 AVA — Multi-Agent AI Assistant

AVA is a multi-agent AI assistant that understands user queries, routes them to the appropriate specialized agent, retrieves information from documents when needed, and generates accurate, context-aware responses through an interactive Streamlit interface.

Built as a hands-on exploration of **Agentic AI**, **LangGraph orchestration**, and **Retrieval-Augmented Generation (RAG)**.

---

## 🌟 Features

- 🧭 Multi-agent architecture with a Supervisor Agent for intelligent query routing
- 📚 Retrieval-Augmented Generation (RAG) over custom PDF documents
- 🗂️ ChromaDB vector database for semantic document retrieval
- 💬 Context-aware conversational responses powered by Google Gemini
- ✅ Built-in task management agent
- ⚡ Lazy-loaded RAG pipeline for improved performance
- 🎨 Modern, interactive Streamlit interface
- ☁️ Cloud deployed on Streamlit

---

# 🏗️ Architecture

The Supervisor Agent serves as the entry point for every user query. Based on the user's intent, it intelligently routes the request to one of three specialized agents:

- 💬 Conversation Agent
- 📚 RAG Agent
- ✅ Task Management Agent

If external knowledge is required, the RAG agent retrieves the most relevant document chunks from ChromaDB before generating the final response with Gemini.

---

# 🧠 How AVA Works

1. User submits a query through the Streamlit interface.
2. The Supervisor Agent analyzes the user's intent.
3. The query is routed to the appropriate specialized agent.
4. If document knowledge is required, the RAG agent retrieves relevant chunks from ChromaDB.
5. Google Gemini generates a context-aware response using both the retrieved context and the user's query.
6. The final response is displayed in the interface along with the responding agent.

---

# 🛠️ Tech Stack

## AI / Backend

- Python
- LangGraph — Multi-Agent Orchestration
- LangChain
- Google Gemini 2.5 Flash Lite
- ChromaDB — Vector Database
- Ollama Embeddings (nomic-embed-text)

## Frontend

- Streamlit
- HTML
- CSS

## Tooling

- Git
- GitHub

---

# 📂 Project Structure

```
AVA-AI-Assistant/
│
├── app.py                     # Streamlit UI
├── styles.css                 # Custom styling
├── chats.json                 # Chat history
├── tasks.json                 # Task persistence
│
├── agent_v2/
│   ├── graph.py               # LangGraph workflow
│   ├── llm.py                 # Gemini configuration
│   ├── agents/
│   │   ├── rag.py             # RAG implementation
│   │   ├── conversation.py
│   │   └── task.py
│   └── data/                  # Source PDF documents
│
├── chroma_db/                 # Persistent vector database
├── requirements.txt
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.12+
- Google Gemini API Key

## 1. Clone the Repository

```bash
git clone <repository-url>
cd AVA-AI-Assistant
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Alternatively, for Streamlit Cloud deployments, add the key through **Streamlit Secrets**.

## 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

# 📖 Retrieval-Augmented Generation (RAG)

AVA uses Retrieval-Augmented Generation (RAG) to answer questions grounded in user-provided documents rather than relying solely on the language model's internal knowledge.

When a query requires document understanding:

- PDFs are chunked and embedded.
- Embeddings are stored in ChromaDB.
- Relevant chunks are retrieved through semantic similarity search.
- Retrieved context is combined with the user's query.
- Google Gemini generates a grounded, context-aware response.

---

# ☁️ Deployment

This branch is configured for deployment on **Streamlit Cloud** using **Google Gemini** as the language model.

Sensitive credentials such as the API key are securely managed through **Streamlit Secrets**.

---

# 🗺️ Roadmap

- ✅ Cloud Deployment
- ⬜ Voice Interaction
- ⬜ Long-Term Memory
- ⬜ Additional Specialized Agents
- ⬜ Improved UI Animations

---

# ✍️ Author

**Anvesha Bishnoi**

Built as a practical exploration of **Agentic AI**, **LangGraph workflows**, **multi-agent systems**, and **Retrieval-Augmented Generation (RAG)**.
 Improved UI animations
