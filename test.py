from typing import Literal
from typing_extensions import TypedDict

from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2", temperature=0)

class Route(TypedDict):
    next: Literal[
        "conversation_agent",
        "task_agent",
        "rag_agent",
    ]

router = llm.with_structured_output(Route)

print(
    router.invoke("Create a task called gym")
)