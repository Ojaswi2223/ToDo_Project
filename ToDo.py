"""
A todo list in plain Python. No web framework, no database.

Run with:
    python todo.py

The classes hold no input() or print() calls, which is what makes them
testable. All user interaction lives in main().
"""


class Todo:
    """A single todo item — holds the data for one task."""

    def __init__(self, todo_id, title, description=None):
        self.id = todo_id              # unique number, assigned by TodoList
        self.title = title             # what the task is
        self.description = description # optional extra detail
        self.completed = False         # every new todo starts unfinished

    def toggle(self):
        """Flip completed: done becomes not-done, and vice versa."""
        self.completed = not self.completed

    def __str__(self):
        """How this todo looks when printed. Called by print() and f-strings."""
        mark = "x" if self.completed else " "   # space, not "", keeps columns aligned
        return f"[{mark}] {self.id}. {self.title}"


class TodoList:
    """The collection — owns all the Todo objects and hands out their ids."""

    def __init__(self):
        self.todos = []      # holds Todo objects
        self.next_id = 1     # counter for the next id to assign

    def add(self, title, description=None):
        """Create a todo, store it, and return it."""
        todo = Todo(self.next_id, title, description)
        self.todos.append(todo)
        self.next_id += 1    # bump so the next todo gets a fresh id
        return todo

    def all(self):
        """Return every todo."""
        return self.todos

    def find(self, todo_id):
        """Return the todo with this id, or None if there isn't one."""
        for todo in self.todos:
            if todo.id == todo_id:
                return todo
        return None          # outside the loop: only after checking every todo

    def delete(self, todo_id):
        """Remove the todo with this id. Returns it, or None if not found."""
        todo = self.find(todo_id)
        if todo is not None:
            self.todos.remove(todo)
        return todo

    def count_completed(self):
        """How many todos are done. Needs to see all of them, so it lives here."""
        return sum(1 for todo in self.todos if todo.completed)


# ============================================================
#  TERMINAL INTERFACE — all input() and print() lives here
# ============================================================

def ask_for_id(prompt):
    """Read an id from the user. Returns an int, or None if invalid."""
    raw = input(prompt).strip()
    if not raw.isdigit():
        print("Please enter a number.")
        return None
    return int(raw)


def main():
    todo_list = TodoList()

    while True:
        print("\n1. Add  2. List  3. Toggle  4. Delete  5. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            todo = todo_list.add(title)
            print(f"Added: {todo.title}")

        elif choice == "2":
            todos = todo_list.all()
            if not todos:
                print("No todos yet.")
                continue
            for todo in todos:
                print(todo)
            print(f"{todo_list.count_completed()} of {len(todos)} completed")

        elif choice == "3":
            todo_id = ask_for_id("ID to toggle: ")
            if todo_id is None:
                continue
            todo = todo_list.find(todo_id)
            if todo is None:
                print("Todo not found.")
            else:
                todo.toggle()
                print(todo)

        elif choice == "4":
            todo_id = ask_for_id("ID to delete: ")
            if todo_id is None:
                continue
            todo = todo_list.delete(todo_id)
            print(f"Deleted: {todo.title}" if todo else "Todo not found.")

        elif choice == "5":
            print("Bye!")
            break

        else:
            print("Invalid choice.")


# Only run the menu when this file is executed directly.
# Without this guard, importing todo.py in a test would start the menu.
if __name__ == "__main__":
    main()