# Solution will be added here
import sqlite3

# 1. Database connection and table creation
conn = sqlite3.connect('tasks.db')  # database file create hogi same folder me
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT
)
''')
conn.commit()

# 2. Functions for CRUD operations

def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    status = input("Enter task status (Pending/Done): ")
    cursor.execute('INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)', (title, description, status))
    conn.commit()
    print("Task added successfully!\n")

def view_tasks():
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    if tasks:
        print("\nAll Tasks:")
        for task in tasks:
            print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Status: {task[3]}")
    else:
        print("No tasks found.")
    print()

def update_task():
    task_id = input("Enter task ID to update: ")
    title = input("Enter new title: ")
    description = input("Enter new description: ")
    status = input("Enter new status (Pending/Done): ")
    cursor.execute('UPDATE tasks SET title=?, description=?, status=? WHERE id=?', (title, description, status, task_id))
    conn.commit()
    print("Task updated successfully!\n")

def delete_task():
    task_id = input("Enter task ID to delete: ")
    cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()
    print("Task deleted successfully!\n")

# 3. Main menu loop
while True:
    print("------ Task Manager ------")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_task()
    elif choice == '2':
        view_tasks()
    elif choice == '3':
        update_task()
    elif choice == '4':
        delete_task()
    elif choice == '5':
        print("Exiting... Goodbye!")
        break
    else:
        print("Invalid choice! Try again.\n")

# Close connection at the end
conn.close()

