# Solution will be added here
import json
import os

STORAGE_FILE = "students.json"


class Student:
    """Class to represent a student"""

    def __init__(self, name, roll_no, course):
        self.name = name
        self.roll_no = roll_no
        self.course = course

    def __str__(self):
        """Readable string format for student"""
        return f"Name: {self.name}, Roll No: {self.roll_no}, Course: {self.course}"

    def to_dict(self):
        """Convert Student object to dict for JSON storage"""
        return {"name": self.name, "roll_no": self.roll_no, "course": self.course}

    @staticmethod
    def from_dict(d):
        """Create Student object from dict"""
        return Student(d["name"], d["roll_no"], d["course"])


class StudentManagementSystem:
    """Class to manage students with JSON persistence"""

    def __init__(self):
        self.students = []  # List to store Student objects
        self.load_data()    # load stored students on startup

    def load_data(self):
        """Load students from JSON file (if exists)"""
        if not os.path.exists(STORAGE_FILE):
            # No file yet — start with empty list
            self.students = []
            return

        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # data expected to be a list of dicts
            self.students = [Student.from_dict(item) for item in data]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read {STORAGE_FILE}. Starting with empty list. ({e})")
            self.students = []

    def save_data(self):
        """Save current students list to JSON file"""
        try:
            with open(STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in self.students], f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error: Could not write to {STORAGE_FILE}: {e}")

    def add_student(self):
        """Add a new student"""
        name = input("Enter student name: ").strip()
        roll_no = input("Enter roll number: ").strip()
        course = input("Enter course: ").strip()

        # simple check: roll_no unique
        if any(s.roll_no == roll_no for s in self.students):
            print("A student with this roll number already exists. Use update instead.\n")
            return

        student = Student(name, roll_no, course)
        self.students.append(student)
        self.save_data()
        print("Student added successfully!\n")

    def view_students(self):
        """View all students"""
        if not self.students:
            print("No students found.\n")
            return

        print("\n--- Student List ---")
        for idx, student in enumerate(self.students, start=1):
            print(f"{idx}. {student}")
        print()

    def update_student(self):
        """Update existing student"""
        roll_no = input("Enter roll number of the student to update: ").strip()

        for student in self.students:
            if student.roll_no == roll_no:
                print(f"Editing student: {student.name} ({student.roll_no})")
                new_name = input("Enter new name (leave blank to keep current): ").strip()
                new_course = input("Enter new course (leave blank to keep current): ").strip()

                if new_name:
                    student.name = new_name
                if new_course:
                    student.course = new_course

                self.save_data()
                print("Student updated successfully!\n")
                return
        print("Student not found.\n")

    def delete_student(self):
        """Delete a student"""
        roll_no = input("Enter roll number of the student to delete: ").strip()

        for student in self.students:
            if student.roll_no == roll_no:
                confirm = input(f"Are you sure you want to delete {student.name}? (y/n): ").strip().lower()
                if confirm == "y":
                    self.students.remove(student)
                    self.save_data()
                    print("Student deleted successfully!\n")
                else:
                    print("Delete cancelled.\n")
                return
        print("Student not found.\n")

    def menu(self):
        """Main menu"""
        while True:
            print("===== Student Management System =====")
            print("1. Add Student")
            print("2. View Students")
            print("3. Update Student")
            print("4. Delete Student")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.update_student()
            elif choice == "4":
                self.delete_student()
            elif choice == "5":
                print("Exiting program. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    system = StudentManagementSystem()
    system.menu()
