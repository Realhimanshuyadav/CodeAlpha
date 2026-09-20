Of course! Converting the console-based application to a Graphical User Interface (GUI) makes it much more user-friendly. Below is the complete code for a GUI version using **PyQt6**, a popular and modern Python library for creating desktop applications.

### Prerequisites

You need to install the PyQt6 library first. You can do this using pip:

```bash
pip install PyQt6
```

### GUI Application Code

The structure is divided into two main parts:
1.  **Backend Logic (Slightly Modified)**: The original classes (`Person`, `Student`, `Professor`, `Course`, `UniversityManagementSystem`) are kept for the core logic. They are slightly modified to return data or status messages instead of printing directly to the console.
2.  **GUI Frontend (New Code)**: This part, built with PyQt6, creates the windows, dialogs, buttons, and tables for user interaction.

Here is the complete, runnable script:

```python
import sys
import uuid
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QLineEdit, QSpinBox, QMessageBox, QDialogButtonBox,
    QTabWidget, QLabel, QComboBox
)
from PyQt6.QtCore import Qt

# ==============================================================================
# 1. BACKEND LOGIC (Slightly modified from the original)
#    - Methods now return values/status instead of printing to the console.
#    - display_info methods return a formatted string.
# ==============================================================================

class Person:
    """Base class for all people in the university system."""
    def __init__(self, name, age, gender):
        self.id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.gender = gender

    def display_info(self):
        """Returns basic information about the person as a formatted string."""
        return (f"ID: {self.id[:8]}...\n"
                f"Name: {self.name}\n"
                f"Age: {self.age}\n"
                f"Gender: {self.gender}")

class Student(Person):
    """Represents a student in the university."""
    def __init__(self, name, age, gender, student_id):
        super().__init__(name, age, gender)
        self.student_id = student_id
        self.enrolled_courses = []

    def display_info(self):
        """Returns detailed information about the student as a formatted string."""
        info = super().display_info()
        info += f"\nStudent ID: {self.student_id}"
        if self.enrolled_courses:
            info += "\nEnrolled Courses:"
            for course in self.enrolled_courses:
                info += f"\n  - {course.course_code}: {course.title}"
        else:
            info += "\nNot enrolled in any courses."
        return info

class Professor(Person):
    """Represents a professor in the university."""
    def __init__(self, name, age, gender, faculty_id, department):
        super().__init__(name, age, gender)
        self.faculty_id = faculty_id
        self.department = department
        self.assigned_courses = []

    def display_info(self):
        """Returns detailed information about the professor as a formatted string."""
        info = super().display_info()
        info += f"\nFaculty ID: {self.faculty_id}\nDepartment: {self.department}"
        if self.assigned_courses:
            info += "\nAssigned Courses:"
            for course in self.assigned_courses:
                info += f"\n  - {course.course_code}: {course.title}"
        else:
            info += "\nNot assigned to any courses."
        return info

class Course:
    """Represents a course offered by the university."""
    def __init__(self, title, course_code, credits, max_capacity):
        self.id = str(uuid.uuid4())
        self.title = title
        self.course_code = course_code
        self.credits = credits
        self.max_capacity = max_capacity
        self.enrolled_students = []
        self.assigned_professor = None

    def display_info(self):
        """Returns detailed information about the course as a formatted string."""
        info = (f"Course ID: {self.id[:8]}...\n"
                f"Title: {self.title}\n"
                f"Course Code: {self.course_code}\n"
                f"Credits: {self.credits}\n"
                f"Capacity: {len(self.enrolled_students)}/{self.max_capacity}")
        
        if self.assigned_professor:
            info += f"\nProfessor: {self.assigned_professor.name}"
        else:
            info += "\nProfessor: Not Assigned"
            
        if self.enrolled_students:
            info += "\n\nEnrolled Students:"
            for student in self.enrolled_students:
                info += f"\n  - {student.name} ({student.student_id})"
        else:
            info += "\n\nNo students enrolled."
        return info

class UniversityManagementSystem:
    """Manages all entities (students, professors, courses) in the university."""
    def __init__(self):
        self.students = []
        self.professors = []
        self.courses = []

    def add_student(self, name, age, gender, student_id):
        if any(s.student_id == student_id for s in self.students):
            return False, f"Error: Student with ID '{student_id}' already exists."
        student = Student(name, age, gender, student_id)
        self.students.append(student)
        return True, f"Student '{name}' added successfully."

    def add_professor(self, name, age, gender, faculty_id, department):
        if any(p.faculty_id == faculty_id for p in self.professors):
            return False, f"Error: Professor with ID '{faculty_id}' already exists."
        professor = Professor(name, age, gender, faculty_id, department)
        self.professors.append(professor)
        return True, f"Professor '{name}' added successfully."

    def add_course(self, title, course_code, credits, max_capacity):
        if any(c.course_code == course_code for c in self.courses):
            return False, f"Error: Course with code '{course_code}' already exists."
        course = Course(title, course_code, credits, max_capacity)
        self.courses.append(course)
        return True, f"Course '{title}' added successfully."

    def find_student_by_id(self, student_id):
        return next((s for s in self.students if s.student_id == student_id), None)

    def find_professor_by_id(self, faculty_id):
        return next((p for p in self.professors if p.faculty_id == faculty_id), None)

    def find_course_by_code(self, course_code):
        return next((c for c in self.courses if c.course_code == course_code), None)

    def enroll_student_in_course(self, student_id, course_code):
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_code(course_code)

        if not student or not course:
            return False, "Invalid student ID or course code."
        
        if student in course.enrolled_students:
            return False, f"Student is already enrolled in '{course.title}'."
        if len(course.enrolled_students) >= course.max_capacity:
            return False, f"Course '{course.title}' is full."

        course.enrolled_students.append(student)
        student.enrolled_courses.append(course)
        return True, f"Student '{student.name}' enrolled in '{course.title}'."

    def assign_professor_to_course(self, faculty_id, course_code):
        professor = self.find_professor_by_id(faculty_id)
        course = self.find_course_by_code(course_code)

        if not professor or not course:
            return False, "Invalid professor ID or course code."

        if course.assigned_professor:
             # Remove course from old professor's assigned list
            old_professor = course.assigned_professor
            if course in old_professor.assigned_courses:
                old_professor.assigned_courses.remove(course)
        
        course.assigned_professor = professor
        professor.assigned_courses.append(course)
        return True, f"Professor '{professor.name}' assigned to '{course.title}'."


# ==============================================================================
# 2. GUI FRONTEND (PyQt6)
# ==============================================================================

class AddEntityDialog(QDialog):
    """A generic dialog for adding a new student, professor, or course."""
    def __init__(self, title, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QFormLayout(self)

        self.inputs = {}
        for key, label, widget_type in fields:
            if widget_type == "spin":
                widget = QSpinBox()
                widget.setRange(16, 100)
            else:
                widget = QLineEdit()
            self.inputs[key] = widget
            self.layout.addRow(label, widget)

        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def get_data(self):
        return {key: widget.text().strip() if isinstance(widget, QLineEdit) else widget.value() for key, widget in self.inputs.items()}

class AssignEnrollDialog(QDialog):
    """A generic dialog for assignments and enrollments."""
    def __init__(self, title, items1, items2, labels, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.layout = QFormLayout(self)
        
        self.combo1 = QComboBox()
        self.combo1.addItems([f"{item[0]} ({item[1]})" for item in items1])
        self.ids1 = [item[1] for item in items1]

        self.combo2 = QComboBox()
        self.combo2.addItems([f"{item[0]} ({item[1]})" for item in items2])
        self.ids2 = [item[1] for item in items2]

        self.layout.addRow(labels[0], self.combo1)
        self.layout.addRow(labels[1], self.combo2)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

    def get_selection(self):
        if not self.ids1 or not self.ids2:
            return None, None
        return self.ids1[self.combo1.currentIndex()], self.ids2[self.combo2.currentIndex()]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ums = UniversityManagementSystem()
        self.setWindowTitle("University Management System")
        self.setGeometry(100, 100, 1200, 600)

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # --- Left Panel: Actions ---
        action_panel = QVBoxLayout()
        action_panel.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Add buttons
        self.add_student_btn = QPushButton("Add Student")
        self.add_prof_btn = QPushButton("Add Professor")
        self.add_course_btn = QPushButton("Add Course")
        self.enroll_btn = QPushButton("Enroll Student")
        self.assign_btn = QPushButton("Assign Professor")
        
        action_panel.addWidget(QLabel("<h2>Actions</h2>"))
        action_panel.addWidget(self.add_student_btn)
        action_panel.addWidget(self.add_prof_btn)
        action_panel.addWidget(self.add_course_btn)
        action_panel.addWidget(self.enroll_btn)
        action_panel.addWidget(self.assign_btn)
        
        # --- Right Panel: Data Display ---
        self.tabs = QTabWidget()
        self.student_table = self.create_table(["Name", "Student ID", "Age", "Gender"])
        self.prof_table = self.create_table(["Name", "Faculty ID", "Department", "Age"])
        self.course_table = self.create_table(["Title", "Course Code", "Credits", "Capacity", "Professor"])

        self.tabs.addTab(self.student_table, "Students")
        self.tabs.addTab(self.prof_table, "Professors")
        self.tabs.addTab(self.course_table, "Courses")

        main_layout.addLayout(action_panel, 1) # 1/4 of the space
        main_layout.addWidget(self.tabs, 3)    # 3/4 of the space

        # Connect signals
        self.add_student_btn.clicked.connect(self.add_student)
        self.add_prof_btn.clicked.connect(self.add_professor)
        self.add_course_btn.clicked.connect(self.add_course)
        self.enroll_btn.clicked.connect(self.enroll_student)
        self.assign_btn.clicked.connect(self.assign_professor)

        self.student_table.itemDoubleClicked.connect(self.view_student_details)
        self.prof_table.itemDoubleClicked.connect(self.view_professor_details)
        self.course_table.itemDoubleClicked.connect(self.view_course_details)

        self.update_displays()

    def create_table(self, headers):
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        return table

    def update_displays(self):
        # Update student table
        self.student_table.setRowCount(len(self.ums.students))
        for row, student in enumerate(self.ums.students):
            self.student_table.setItem(row, 0, QTableWidgetItem(student.name))
            self.student_table.setItem(row, 1, QTableWidgetItem(student.student_id))
            self.student_table.setItem(row, 2, QTableWidgetItem(str(student.age)))
            self.student_table.setItem(row, 3, QTableWidgetItem(student.gender))

        # Update professor table
        self.prof_table.setRowCount(len(self.ums.professors))
        for row, prof in enumerate(self.ums.professors):
            self.prof_table.setItem(row, 0, QTableWidgetItem(prof.name))
            self.prof_table.setItem(row, 1, QTableWidgetItem(prof.faculty_id))
            self.prof_table.setItem(row, 2, QTableWidgetItem(prof.department))
            self.prof_table.setItem(row, 3, QTableWidgetItem(str(prof.age)))
        
        # Update course table
        self.course_table.setRowCount(len(self.ums.courses))
        for row, course in enumerate(self.ums.courses):
            capacity = f"{len(course.enrolled_students)}/{course.max_capacity}"
            prof_name = course.assigned_professor.name if course.assigned_professor else "N/A"
            self.course_table.setItem(row, 0, QTableWidgetItem(course.title))
            self.course_table.setItem(row, 1, QTableWidgetItem(course.course_code))
            self.course_table.setItem(row, 2, QTableWidgetItem(str(course.credits)))
            self.course_table.setItem(row, 3, QTableWidgetItem(capacity))
            self.course_table.setItem(row, 4, QTableWidgetItem(prof_name))

    def add_student(self):
        fields = [
            ('name', 'Name:', 'text'),
            ('age', 'Age:', 'spin'),
            ('gender', 'Gender:', 'text'),
            ('student_id', 'Student ID:', 'text')
        ]
        dialog = AddEntityDialog("Add New Student", fields, self)
        if dialog.exec():
            data = dialog.get_data()
            if not all(data.values()):
                 QMessageBox.warning(self, "Input Error", "All fields are required.")
                 return
            success, message = self.ums.add_student(**data)
            QMessageBox.information(self, "Result", message)
            if success:
                self.update_displays()

    def add_professor(self):
        fields = [
            ('name', 'Name:', 'text'),
            ('age', 'Age:', 'spin'),
            ('gender', 'Gender:', 'text'),
            ('faculty_id', 'Faculty ID:', 'text'),
            ('department', 'Department:', 'text')
        ]
        dialog = AddEntityDialog("Add New Professor", fields, self)
        if dialog.exec():
            data = dialog.get_data()
            if not all(data.values()):
                 QMessageBox.warning(self, "Input Error", "All fields are required.")
                 return
            success, message = self.ums.add_professor(**data)
            QMessageBox.information(self, "Result", message)
            if success:
                self.update_displays()

    def add_course(self):
        fields = [
            ('title', 'Title:', 'text'),
            ('course_code', 'Course Code:', 'text'),
            ('credits', 'Credits:', 'spin'),
            ('max_capacity', 'Max Capacity:', 'spin')
        ]
        dialog = AddEntityDialog("Add New Course", fields, self)
        if dialog.exec():
            data = dialog.get_data()
            if not all(data.values()):
                 QMessageBox.warning(self, "Input Error", "All fields are required.")
                 return
            data['course_code'] = data['course_code'].upper()
            success, message = self.ums.add_course(**data)
            QMessageBox.information(self, "Result", message)
            if success:
                self.update_displays()
    
    def enroll_student(self):
        students = [(s.name, s.student_id) for s in self.ums.students]
        courses = [(c.title, c.course_code) for c in self.ums.courses]
        if not students or not courses:
            QMessageBox.warning(self, "Error", "Please add students and courses before enrolling.")
            return

        dialog = AssignEnrollDialog("Enroll Student in Course", students, courses, ["Select Student:", "Select Course:"], self)
        if dialog.exec():
            student_id, course_code = dialog.get_selection()
            if student_id and course_code:
                success, message = self.ums.enroll_student_in_course(student_id, course_code)
                QMessageBox.information(self, "Enrollment Result", message)
                if success:
                    self.update_displays()

    def assign_professor(self):
        profs = [(p.name, p.faculty_id) for p in self.ums.professors]
        courses = [(c.title, c.course_code) for c in self.ums.courses]
        if not profs or not courses:
            QMessageBox.warning(self, "Error", "Please add professors and courses before assigning.")
            return

        dialog = AssignEnrollDialog("Assign Professor to Course", profs, courses, ["Select Professor:", "Select Course:"], self)
        if dialog.exec():
            faculty_id, course_code = dialog.get_selection()
            if faculty_id and course_code:
                success, message = self.ums.assign_professor_to_course(faculty_id, course_code)
                QMessageBox.information(self, "Assignment Result", message)
                if success:
                    self.update_displays()
    
    def view_student_details(self, item):
        student_id = self.student_table.item(item.row(), 1).text()
        student = self.ums.find_student_by_id(student_id)
        if student:
            QMessageBox.information(self, f"Details for {student.name}", student.display_info())

    def view_professor_details(self, item):
        faculty_id = self.prof_table.item(item.row(), 1).text()
        prof = self.ums.find_professor_by_id(faculty_id)
        if prof:
            QMessageBox.information(self, f"Details for {prof.name}", prof.display_info())

    def view_course_details(self, item):
        course_code = self.course_table.item(item.row(), 1).text()
        course = self.ums.find_course_by_code(course_code)
        if course:
            QMessageBox.information(self, f"Details for {course.title}", course.display_info())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```