# Solution will be added here
import json # <--- New Import for file handling
from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------------- Dummy data (Python list) ----------------
tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build Task Manager API", "done": False}
]

# --- Helper Function to Save JSON to File ---
def save_tasks_to_file(data, filename="tasks_response.json"):
    """Saves the current list of tasks to a local JSON file."""
    try:
        with open(filename, 'w') as f:
            # json.dump is used to write a Python object to a JSON file
            # indent=4 makes the JSON file human-readable
            json.dump(data, f, indent=4)
        print(f"\n[INFO] Current tasks list saved to {filename}")
    except Exception as e:
        print(f"\n[ERROR] Could not save tasks to file: {e}")

# ---------------- Home route (optional) ----------------
@app.route('/')
def home():
    return "Welcome to Task Manager API! Use /tasks endpoint to view tasks."

# ---------------- GET /tasks ----------------
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # 1. Create the data structure for the response
    response_data = tasks
    
    # 2. Save the data to a file before returning the response
    save_tasks_to_file(response_data) # This will create 'tasks_response.json'
    
    # 3. Return the standard Flask JSON response
    return jsonify(response_data), 200

# ---------------- POST /tasks ----------------
@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.get_json()
    if not new_task or not new_task.get("title"):
        return jsonify({"error": "Task title is required"}), 400

    new_id = tasks[-1]['id'] + 1 if tasks else 1
    task = {"id": new_id, "title": new_task["title"], "done": False}
    tasks.append(task)
    
    # Optional: Save updated list after creation
    save_tasks_to_file(tasks)
    
    return jsonify({"message": "Task added successfully!", "task": task}), 201

# ---------------- PUT /tasks/<id> ----------------
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["done"] = data.get("done", task["done"])
            
            # Optional: Save updated list after modification
            save_tasks_to_file(tasks)
            
            return jsonify({"message": "Task updated successfully!", "task": task})
    return jsonify({"error": "Task not found"}), 404

# ---------------- DELETE /tasks/<id> ----------------
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks # Need global keyword to modify the list directly
    initial_length = len(tasks)
    
    # Re-assign tasks list without the deleted item
    tasks = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) < initial_length:
        # Optional: Save updated list after deletion
        save_tasks_to_file(tasks)
        return jsonify({"message": "Task deleted successfully!"})
        
    return jsonify({"error": "Task not found"}), 404

# ---------------- Run Flask app ----------------
if __name__ == '__main__':
    app.run(debug=True)