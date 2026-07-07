from langchain_core.tools import tool
import json

def load_tasks():

    with open("tasks.json", "r") as file:
        tasks = json.load(file)

    return tasks

def save_tasks(tasks):

    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

@tool
def create_task(title: str):
    """
    Create a new task.
    """

    tasks = load_tasks()

    tasks.append(
    {
        "title": title,
        "completed": False
    }
    )

    save_tasks(tasks)

    return f"Task '{title}' created."

@tool
def list_tasks():
    """
    Use this tool ONLY when the user explicitly asks to
    view, list, show, display, or check their tasks.
    Do NOT use this tool for greetings or general conversation.
    """

    tasks = load_tasks()

    if not tasks:
        return "You don't have any tasks yet."

    output = ""

    for task in tasks:

        if task["completed"]:
            output += f"✅ {task['title']}\n"

        else:
            output += f"❌ {task['title']}\n"

    return output

@tool
def delete_task(title: str):
    """
    Use this tool when the user wants to delete or remove a task from their task list.

    Examples include:
    - "Delete Buy Milk."
    - "Remove my milk task."
    - "I don't need this task anymore."
    - "Delete my assignment task."

    Do NOT use this tool for greetings or general conversation.
    """

    tasks = load_tasks()

    for task in tasks:
        if task["title"].lower() == title.lower():
            tasks.remove(task)
            save_tasks(tasks)
            return f"Task '{title}' deleted."
    
    return "Task not found."


@tool
def complete_task(title: str):
    """
    Use this tool when the user indicates that they have completed or finished a task.
    Examples include:
    - "I finished my assignment."
    - "I bought the milk."
    - "Mark Buy Milk as completed."
    - "Complete my task."
    Do NOT use this tool for greetings or general conversation.
    """

    tasks = load_tasks()

    for task in tasks:
        if task["title"] == title:
            task["completed"] = True
            save_tasks(tasks)
            return f"Task '{title}' marked as completed."
    
    return "Task not found."