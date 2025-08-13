# Simple Command-Line To-Do List Application

import sys
import os
import json

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f)

def list_tasks(tasks):
    if not tasks:
        print("No tasks!")
    for i, t in enumerate(tasks, 1):
        status = "[x]" if t["done"] else "[ ]"
        print(f"{i}. {status} {t['task']}")

def add_task(tasks, text):
    tasks.append({"task": text, "done": False})
    save_tasks(tasks)
    print(f"Added: {text}")

def complete_task(tasks, idx):
    try:
        tasks[idx]["done"] = True
        save_tasks(tasks)
        print(f"Marked as done: {tasks[idx]['task']}")
    except IndexError:
        print("No such task.")

def delete_task(tasks, idx):
    try:
        task = tasks.pop(idx)
        save_tasks(tasks)
        print(f"Deleted: {task['task']}")
    except IndexError:
        print("No such task.")

def print_help():
    print("Commands:")
    print("  list                  Show all tasks")
    print("  add <task>            Add new task")
    print("  done <number>         Mark task as done")
    print("  delete <number>       Delete task")
    print("  help                  Show this help")
    print("  quit                  Exit")

def main():
    tasks = load_tasks()
    print("Simple To-Do List. Type 'help' for commands.")

    while True:
        cmd = input("> ").strip()
        if cmd == "list":
            list_tasks(tasks)
        elif cmd.startswith("add "):
            add_task(tasks, cmd[4:])
            tasks = load_tasks()
        elif cmd.startswith("done "):
            try:
                complete_task(tasks, int(cmd[5:])-1)
                tasks = load_tasks()
            except ValueError:
                print("Please provide a valid number.")
        elif cmd.startswith("delete "):
            try:
                delete_task(tasks, int(cmd[7:])-1)
                tasks = load_tasks()
            except ValueError:
                print("Please provide a valid number.")
        elif cmd == "help":
            print_help()
        elif cmd == "quit":
            break
        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()