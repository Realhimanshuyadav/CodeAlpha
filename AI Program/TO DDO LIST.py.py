import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# Define the filename for storing tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Loads tasks from the JSON file."""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Handle empty or malformed JSON file
            return []
    return []

def save_tasks(tasks):
    """Saves tasks to the JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

class TodoApp:
    def __init__(self, master):
        """Initializes the To-Do List application GUI."""
        self.master = master
        master.title("My To-Do List")
        master.geometry("500x550") # Set initial window size
        master.resizable(False, False) # Make window non-resizable for simplicity

        # Load existing tasks
        self.tasks = load_tasks()

        # --- GUI Elements ---

        # Frame for input and add button
        self.input_frame = tk.Frame(master, padx=10, pady=10)
        self.input_frame.pack(fill=tk.X)

        self.task_entry = tk.Entry(self.input_frame, width=40, font=('Arial', 12))
        self.task_entry.pack(side=tk.LEFT, padx=(0, 10), pady=5, expand=True, fill=tk.X)
        self.task_entry.bind("<Return>", self.add_task_event) # Bind Enter key to add task

        self.add_button = tk.Button(self.input_frame, text="Add Task", command=self.add_task,
                                    bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'),
                                    activebackground='#45a049', relief=tk.RAISED, bd=3,
                                    cursor="hand2")
        self.add_button.pack(side=tk.RIGHT, pady=5)

        # Frame for task list and scrollbar
        self.list_frame = tk.Frame(master, padx=10, pady=5)
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(self.list_frame, height=15, width=50,
                                       font=('Arial', 12), bd=2, relief=tk.GROOVE,
                                       selectmode=tk.SINGLE, activestyle='none')
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Frame for action buttons
        self.button_frame = tk.Frame(master, padx=10, pady=10)
        self.button_frame.pack(fill=tk.X)

        self.mark_complete_button = tk.Button(self.button_frame, text="Mark Complete", command=self.mark_task_complete,
                                             bg='#2196F3', fg='white', font=('Arial', 10, 'bold'),
                                             activebackground='#1976D2', relief=tk.RAISED, bd=3,
                                             cursor="hand2")
        self.mark_complete_button.pack(side=tk.LEFT, padx=(0, 5), expand=True, fill=tk.X)

        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task,
                                       bg='#F44336', fg='white', font=('Arial', 10, 'bold'),
                                       activebackground='#D32F2F', relief=tk.RAISED, bd=3,
                                       cursor="hand2")
        self.delete_button.pack(side=tk.LEFT, padx=(5, 0), expand=True, fill=tk.X)

        # Initial display of tasks
        self.update_task_listbox()

    def update_task_listbox(self):
        """Clears and repopulates the listbox with current tasks."""
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            status = "✓" if task["completed"] else " "
            display_text = f"[{status}] {task['description']}"
            self.task_listbox.insert(tk.END, display_text)
            # Apply strikethrough for completed tasks
            if task["completed"]:
                self.task_listbox.itemconfig(i, {'fg': 'gray', 'selectforeground': 'gray'})
            else:
                self.task_listbox.itemconfig(i, {'fg': 'black', 'selectforeground': 'black'})


    def add_task_event(self, event=None):
        """Event handler for adding a task (e.g., via Enter key)."""
        self.add_task()

    def add_task(self):
        """Adds a new task to the list and updates the display."""
        description = self.task_entry.get().strip()
        if description:
            self.tasks.append({"description": description, "completed": False})
            self.task_entry.delete(0, tk.END) # Clear the input field
            self.update_task_listbox()
            save_tasks(self.tasks)
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty!")

    def mark_task_complete(self):
        """Marks the selected task as complete and updates the display."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            if 0 <= selected_index < len(self.tasks):
                self.tasks[selected_index]["completed"] = not self.tasks[selected_index]["completed"] # Toggle status
                self.update_task_listbox()
                save_tasks(self.tasks)
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark complete.")

    def delete_task(self):
        """Deletes the selected task from the list and updates the display."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            if 0 <= selected_index < len(self.tasks):
                # Use a custom confirmation dialog instead of alert()
                if messagebox.askyesno("Delete Task", "Are you sure you want to delete the selected task?"):
                    del self.tasks[selected_index]
                    self.update_task_listbox()
                    save_tasks(self.tasks)
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()