from agent_v2.graph import graph
from langchain_core.messages import HumanMessage

print("=" * 40)
print("🤖 AI Task Assistant")
print("Type 'exit' to quit.")
print("=" * 40)

while True:

    user_input = input("\n👤 You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("\n👋 Goodbye!")
        break

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ]
        }
    )

    messages = result["messages"]

    assistant_message = messages[-1]

    print("\n🤖 Assistant:")
    print(assistant_message.content)