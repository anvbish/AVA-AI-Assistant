import streamlit as st
import json
from pathlib import Path
from datetime import datetime

from langchain_core.messages import HumanMessage

from agent_v2.graph import graph, get_route

CHAT_FILE = Path("chats.json")


def load_chats():

    if CHAT_FILE.exists():

        with open(CHAT_FILE, "r") as f:
            return json.load(f)

    return {
        "New Chat": []
    }



def save_chats():

    with open(CHAT_FILE, "w") as f:
        json.dump(
            st.session_state.chats,
            f,
            indent=4
        )


st.set_page_config(
    page_title="Ava",
    page_icon="🌸",
    layout="centered",
)

st.markdown(
    """
<style>

div[data-testid="stSpinner"] > div {
    border-top-color: #ff69b4 !important;
}

div[data-testid="stSpinner"] p {
    color: #ff69b4 !important;
    font-weight: 600;
}

</style>
""",
    unsafe_allow_html=True
)


if "chats" not in st.session_state:

    st.session_state.chats = load_chats()


if "current_chat" not in st.session_state:

    st.session_state.current_chat = list(
        st.session_state.chats.keys()
    )[0]

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

messages = st.session_state.chats[st.session_state.current_chat]

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_documents():
    data_path = Path("agent_v2/data")
    return sorted([pdf.name for pdf in data_path.glob("*.pdf")])


def get_tasks():
    with open("tasks.json", "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)

with st.sidebar:

    st.markdown(
        """
        <div class="logo-block">
            <div class="logo-avatar">👩</div>
            <div class="logo-text">Ava<span>🌸</span></div>
        </div>
        
      <div class="credit-line">  <p style="align-items: center;">Made with ❤️ by <br> <b>Anvesha Bishnoi</b>
        <a href="https://github.com/anvbish" target="_blank">@anvbish</a></p></div>
        """,
    unsafe_allow_html=True,
)

    
    if st.button(
    "➕ New Chat",
    use_container_width=True,
    ):

        chat_name = f"Chat {len(st.session_state.chats)+1}"

        st.session_state.chats[chat_name] = []

        st.session_state.current_chat = chat_name

        save_chats()

        st.rerun()

    st.markdown('<div class="sidebar-section-label">💬 Chats</div>', unsafe_allow_html=True)

    for chat in list(st.session_state.chats.keys()):

        icon = "🟣" if chat == st.session_state.current_chat else "⚪"

        col1, col2 = st.columns([6, 1])

        with col1:
            if st.button(
                f"{icon} {chat}",
                key=f"chat_{chat}",
                use_container_width=True,
            ):
                st.session_state.current_chat = chat
                st.rerun()

        with col2:
            if len(st.session_state.chats) > 1:
                if st.button(
                    "🗑️",
                    key=f"delete_{chat}",
                    use_container_width=True,
                ):
                    del st.session_state.chats[chat]

                    save_chats()

                    if st.session_state.current_chat == chat:
                        st.session_state.current_chat = next(
                            iter(st.session_state.chats)
                        )

                    st.rerun()

    st.markdown("---")


    
    doc_header_col1, doc_header_col2 = st.columns([3, 1])
    with doc_header_col1:
        st.markdown('<div class="sidebar-section-label">📁 Documents</div>', unsafe_allow_html=True)
    with doc_header_col2:
        st.session_state.setdefault("show_uploader", False)
        if st.button("➕ Add", key="toggle_uploader", use_container_width=True):
            st.session_state.show_uploader = not st.session_state.show_uploader

    if st.session_state.show_uploader:
        uploaded_file = st.file_uploader(
            "Choose a PDF",
            type=["pdf"],
            label_visibility="collapsed"
        )
        if uploaded_file is not None:

            save_path = Path("agent_v2/data") / uploaded_file.name

            if not save_path.exists():

                with open(save_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.success(f"{uploaded_file.name} uploaded successfully!")

                st.session_state.show_uploader = False

                st.rerun()

            else:
                st.info("This PDF already exists.")

    docs = get_documents()

    if docs:
        doc_cards_html = '<div class="doc-list">'
        for doc in docs:
            doc_cards_html += (
                '<div class="doc-card">'
                '<div class="doc-card-icon">📄</div>'
                '<div class="doc-card-info">'
                f'<div class="doc-card-name">{doc}</div>'
                '<div class="doc-card-status">Uploaded</div>'
                '</div>'
                '<div class="doc-card-check">✅</div>'
                '</div>'
            )
        doc_cards_html += "</div>"
        st.markdown(doc_cards_html, unsafe_allow_html=True)
    else:
        st.markdown('<p class="empty-hint">No documents yet.</p>', unsafe_allow_html=True)

    st.markdown("---")

    
    task_header_col1, task_header_col2 = st.columns([3, 1])
    with task_header_col1:
        st.markdown('<div class="sidebar-section-label">📋 Tasks</div>', unsafe_allow_html=True)
    with task_header_col2:
        st.session_state.setdefault("show_new_task", False)
        if st.button("➕ New", key="toggle_new_task", use_container_width=True):
            st.session_state.show_new_task = not st.session_state.show_new_task

    if st.session_state.show_new_task:
        with st.form("new_task_form", clear_on_submit=True):
            new_task_title = st.text_input(
                "Task title",
                label_visibility="collapsed",
                placeholder="What needs doing?"
            )
            submitted = st.form_submit_button("Add task", use_container_width=True)

            if submitted and new_task_title.strip():
                tasks = get_tasks()
                tasks.append({"title": new_task_title.strip(), "completed": False})
                save_tasks(tasks)
                st.session_state.show_new_task = False
                st.rerun()

    tasks = get_tasks()

    tasks_html = '<div class="task-list">'
    for task in tasks:
            if task["completed"]:
                tasks_html += (
                    '<div class="task-item task-done">'
                    '<div class="task-check task-check-done">✓</div>'
                    f'<div class="task-title">{task["title"]}</div>'
                    '</div>'
                )
            else:
                tasks_html += (
                    '<div class="task-item">'
                    '<div class="task-check"></div>'
                    f'<div class="task-title">{task["title"]}</div>'
                    '</div>'
                )
    tasks_html += "</div>"
    st.markdown(tasks_html, unsafe_allow_html=True)
            #workspace stats
    num_docs = len(get_documents())
    num_tasks = len(get_tasks())
    num_messages = len(messages)

    st.markdown(f"""
    <div class="workspace-card">

    <h3>📊 Workspace</h3>

    <div class="workspace-item">
    📄 Documents
    <span>{num_docs}</span>
    </div>

    <div class="workspace-item">
    📋 Tasks
    <span>{num_tasks}</span>
    </div>

    <div class="workspace-item">
    💬 Messages
    <span>{num_messages}</span>
    </div>

    <div class="workspace-item">
    🟢 Status
    <span>Ready</span>
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="sidebar-footer-plant">🪴</div>
            <div class="sidebar-footer-bubble">
                Have a great day! <br>(｡•́‿•̀｡) 💕
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



if len(messages) == 0:
    st.markdown("""
    <div class="header">
        <h1>Ava✨</h1>
        <p>💖 Your Multi-Agent AI Assistant 🌸</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="header">
        <h1>Ava✨</h1>
    </div>
    """, unsafe_allow_html=True)

if len(messages) == 0:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-text">
            <h2>Hi! I'm Ava👋</h2>
            <p>
                Your AI companion for conversations, 
                task management, and intelligent document search.</h2>
            </p>
        </div>
        <div class="welcome-mascot">🤖</div>
    </div>
    """, unsafe_allow_html=True)



prompt = st.chat_input("Ask Ava anything...")

if prompt and prompt.strip():

    if (
        st.session_state.current_chat
        and st.session_state.current_chat.startswith("Chat")
        and len(messages) == 0
    ):

        title = prompt[:30].strip()

        if len(prompt) > 30:
            title += "..."

        base_title = title
        count = 2

        while title in st.session_state.chats:
            title = f"{base_title} ({count})"
            count += 1

        st.session_state.chats[title] = st.session_state.chats.pop(
            st.session_state.current_chat
        )

        st.session_state.current_chat = title

        messages = st.session_state.chats[title]


    
    messages.append(
        {
            "role": "user",
            "content": prompt,
            "time": datetime.now().strftime("%I:%M %p"),
        }
    )

    agent = get_route(
        HumanMessage(content=prompt)
    )


    

    with st.spinner("🤖 Ava is thinking..."):

        response = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=prompt)
                ]
            }
        )


        ai_message = response["messages"][-1].content


    messages.append(
        {
            "role": "assistant",
            "content": ai_message,
            "agent": agent,
            "time": datetime.now().strftime("%I:%M %p"),
        }
    )


    save_chats()

    st.rerun()

avatars = {
    "user": "👩",
    "assistant": "🤖"
}
if len(messages) > 0:
    st.markdown(
        f"""
        <div style="
            font-size:22px;
            font-weight:600;
            color:#555;
            margin:10px 0 20px 0;
        ">
            💬 {st.session_state.current_chat}
        </div>
        """,
        unsafe_allow_html=True,
    )

for message in messages:

    with st.chat_message(
        message["role"],
        avatar=avatars.get(message["role"], "💬")
    ):

        top_row = '<div class="msg-top-row">'

        # Show agent badge for assistant messages
        if message["role"] == "assistant":

            badge = {
                "conversation_agent": (
                    "💬 Conversation Agent",
                    "#DBEAFE",
                    "#1D4ED8"
                ),
                "task_agent": (
                    "📋 Task Agent",
                    "#D9FBE8",
                    "#047857"
                ),
                "rag_agent": (
                    "📚 RAG Agent",
                    "#EADCF8",
                    "#6B46C1"
                ),
            }.get(message.get("agent"))

            if badge:
                text, bg, color = badge

                top_row += f"""
                <div class="agent-badge" style="background:{bg};color:{color};">
                    {text}
                </div>
                """
            else:
                top_row += '<div class="agent-badge" style="background:#F1F1F1;color:#555;">🤖 Assistant</div>'

        else:
            top_row += '<div></div>'

        if message.get("time"):
            top_row += f'<div class="msg-time">{message["time"]}</div>'

        top_row += "</div>"

        st.markdown(top_row, unsafe_allow_html=True)

        st.markdown(message["content"])

