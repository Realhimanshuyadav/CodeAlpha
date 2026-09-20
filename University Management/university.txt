import uuid # For generating unique IDs

class Person:
    """Base class for all people in the university system."""
    def __init__(self, name, age, gender):
        self.id = str(uuid.uuid4()) # Generate a unique ID for each person
        self.name = name
        self.age = age
        self.gender = gender

    def display_info(self):
        """Prints basic information about the person."""
        print(f"ID: {self.id[:8]}...") # Display first 8 chars of ID
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")

class Student(Person):
    """Represents a student in the university."""
    def __init__(self, name, age, gender, student_id):
        super().__init__(name, age, gender)
        self.student_id = student_id
        self.enrolled_courses = [] # List of Course objects

    def display_info(self):
        """Prints detailed information about the student, including enrolled courses."""
        print("\n--- Student Details ---")
        super().display_info()
        print(f"Student ID: {self.student_id}")
        if self.enrolled_courses:
            print("Enrolled Courses:")
            for course in self.enrolled_courses:
                print(f"  - {course.course_code}: {course.title}")
        else:
            print("Not enrolled in any courses.")
        print("-----------------------")

class Professor(Person):
    """Represents a professor in the university."""
    def __init__(self, name, age, gender, faculty_id, department):
        super().__init__(name, age, gender)
        self.faculty_id = faculty_id
        self.department = department
        self.assigned_courses = [] # List of Course objects

    def display_info(self):
        """Prints detailed information about the professor, including assigned courses."""
        print("\n--- Professor Details ---")
        super().display_info()
        print(f"Faculty ID: {self.faculty_id}")
        print(f"Department: {self.department}")
        if self.assigned_courses:
            print("Assigned Courses:")
            for course in self.assigned_courses:
                print(f"  - {course.course_code}: {course.title}")
        else:
            print("Not assigned to any courses.")
        print("-----------------------")

class Course:
    """Represents a course offered by the university."""
    def __init__(self, title, course_code, credits, max_capacity):
        self.id = str(uuid.uuid4()) # Unique ID for the course
        self.title = title
        self.course_code = course_code
        self.credits = credits
        self.max_capacity = max_capacity
        self.enrolled_students = [] # List of Student objects
        self.assigned_professor = None # Professor object

    def display_info(self):
        """Prints detailed information about the course."""
        print("\n--- Course Details ---")
        print(f"Course ID: {self.id[:8]}...")
        print(f"Title: {self.title}")
        print(f"Course Code: {self.course_code}")
        print(f"Credits: {self.credits}")
        print(f"Max Capacity: {self.max_capacity}")
        print(f"Current Enrollment: {len(self.enrolled_students)}")
        if self.assigned_professor:
            print(f"Assigned Professor: {self.assigned_professor.name} ({self.assigned_professor.faculty_id})")
        else:
            print("No professor assigned.")
        if self.enrolled_students:
            print("Enrolled Students:")
            for student in self.enrolled_students:
                print(f"  - {student.name} ({student.student_id})")
        else:
            print("No students enrolled.")
        print("--------------------")

class UniversityManagementSystem:
    """Manages all entities (students, professors, courses) in the university."""
    def __init__(self):
        self.students = []
        self.professors = []
        self.courses = []

    def add_student(self):
        """Prompts for student details and adds a new student."""
        print("\n--- Add New Student ---")
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        gender = input("Enter student gender (Male/Female/Other): ")
        student_id = input("Enter student ID: ")

        # Check for duplicate student ID
        if any(s.student_id == student_id for s in self.students):
            print("Error: Student with this ID already exists.")
            return

        student = Student(name, age, gender, student_id)
        self.students.append(student)
        print(f"Student '{name}' added successfully with ID: {student.student_id}")

    def add_professor(self):
        """Prompts for professor details and adds a new professor."""
        print("\n--- Add New Professor ---")
        name = input("Enter professor name: ")
        age = int(input("Enter professor age: "))
        gender = input("Enter professor gender (Male/Female/Other): ")
        faculty_id = input("Enter faculty ID: ")
        department = input("Enter department: ")

        # Check for duplicate faculty ID
        if any(p.faculty_id == faculty_id for p in self.professors):
            print("Error: Professor with this ID already exists.")
            return

        professor = Professor(name, age, gender, faculty_id, department)
        self.professors.append(professor)
        print(f"Professor '{name}' added successfully with ID: {professor.faculty_id}")

    def add_course(self):
        """Prompts for course details and adds a new course."""
        print("\n--- Add New Course ---")
        title = input("Enter course title: ")
        course_code = input("Enter course code (e.g., CS101): ").upper()
        credits = int(input("Enter number of credits: "))
        max_capacity = int(input("Enter maximum capacity: "))

        # Check for duplicate course code
        if any(c.course_code == course_code for c in self.courses):
            print("Error: Course with this code already exists.")
            return

        course = Course(title, course_code, credits, max_capacity)
        self.courses.append(course)
        print(f"Course '{title}' ({course_code}) added successfully.")

    def enroll_student_in_course(self):
        """Enrolls a student in a course."""
        print("\n--- Enroll Student in Course ---")
        if not self.students:
            print("No students registered yet. Please add students first.")
            return
        if not self.courses:
            print("No courses available yet. Please add courses first.")
            return

        self.list_all_students()
        student_id = input("Enter student ID to enroll: ")
        student = next((s for s in self.students if s.student_id == student_id), None)

        if not student:
            print("Student not found.")
            return

        self.list_all_courses()
        course_code = input("Enter course code to enroll in: ").upper()
        course = next((c for c in self.courses if c.course_code == course_code), None)

        if not course:
            print("Course not found.")
            return

        if student in course.enrolled_students:
            print(f"Student '{student.name}' is already enrolled in '{course.title}'.")
        elif len(course.enrolled_students) >= course.max_capacity:
            print(f"Course '{course.title}' is full. Cannot enroll more students.")
        else:
            course.enrolled_students.append(student)
            student.enrolled_courses.append(course)
            print(f"Student '{student.name}' successfully enrolled in '{course.title}'.")

    def assign_professor_to_course(self):
        """Assigns a professor to a course."""
        print("\n--- Assign Professor to Course ---")
        if not self.professors:
            print("No professors registered yet. Please add professors first.")
            return
        if not self.courses:
            print("No courses available yet. Please add courses first.")
            return

        self.list_all_professors()
        faculty_id = input("Enter professor's faculty ID to assign: ")
        professor = next((p for p in self.professors if p.faculty_id == faculty_id), None)

        if not professor:
            print("Professor not found.")
            return

        self.list_all_courses()
        course_code = input("Enter course code to assign professor to: ").upper()
        course = next((c for c in self.courses if c.course_code == course_code), None)

        if not course:
            print("Course not found.")
            return

        if course.assigned_professor:
            print(f"Course '{course.title}' already has a professor assigned: {course.assigned_professor.name}.")
            overwrite = input("Do you want to reassign? (yes/no): ").lower()
            if overwrite != 'yes':
                print("Assignment cancelled.")
                return
            # Remove course from old professor's assigned list
            old_professor = course.assigned_professor
            if course in old_professor.assigned_courses:
                old_professor.assigned_courses.remove(course)

        course.assigned_professor = professor
        professor.assigned_courses.append(course)
        print(f"Professor '{professor.name}' successfully assigned to '{course.title}'.")

    def list_all_students(self):
        """Lists all registered students."""
        print("\n--- All Students ---")
        if not self.students:
            print("No students registered.")
            return
        for student in self.students:
            print(f"- {student.name} (ID: {student.student_id})")
        print("--------------------")

    def list_all_professors(self):
        """Lists all registered professors."""
        print("\n--- All Professors ---")
        if not self.professors:
            print("No professors registered.")
            return
        for professor in self.professors:
            print(f"- {professor.name} (ID: {professor.faculty_id}, Dept: {professor.department})")
        print("--------------------")

    def list_all_courses(self):
        """Lists all registered courses."""
        print("\n--- All Courses ---")
        if not self.courses:
            print("No courses available.")
            return
        for course in self.courses:
            print(f"- {course.title} (Code: {course.course_code}, Credits: {course.credits}, Enrolled: {len(course.enrolled_students)}/{course.max_capacity})")
        print("--------------------")

    def view_student_details(self):
        """Views details of a specific student."""
        print("\n--- View Student Details ---")
        if not self.students:
            print("No students registered yet.")
            return
        self.list_all_students()
        student_id = input("Enter student ID to view details: ")
        student = next((s for s in self.students if s.student_id == student_id), None)
        if student:
            student.display_info()
        else:
            print("Student not found.")

    def view_professor_details(self):
        """Views details of a specific professor."""
        print("\n--- View Professor Details ---")
        if not self.professors:
            print("No professors registered yet.")
            return
        self.list_all_professors()
        faculty_id = input("Enter professor's faculty ID to view details: ")
        professor = next((p for p in self.professors if p.faculty_id == faculty_id), None)
        if professor:
            professor.display_info()
        else:
            print("Professor not found.")

    def view_course_details(self):
        """Views details of a specific course."""
        print("\n--- View Course Details ---")
        if not self.courses:
            print("No courses available yet.")
            return
        self.list_all_courses()
        course_code = input("Enter course code to view details: ").upper()
        course = next((c for c in self.courses if c.course_code == course_code), None)
        if course:
            course.display_info()
        else:
            print("Course not found.")

    def run(self):
        """Main loop for the console application."""
        while True:
            print("\n===== University Management System =====")
            print("1. Add New Student")
            print("2. Add New Professor")
            print("3. Add New Course")
            print("4. Enroll Student in Course")
            print("5. Assign Professor to Course")
            print("6. List All Students")
            print("7. List All Professors")
            print("8. List All Courses")
            print("9. View Student Details")
            print("10. View Professor Details")
            print("11. View Course Details")
            print("12. Exit")
            print("========================================")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.add_professor()
            elif choice == '3':
                self.add_course()
            elif choice == '4':
                self.enroll_student_in_course()
            elif choice == '5':
                self.assign_professor_to_course()
            elif choice == '6':
                self.list_all_students()
            elif choice == '7':
                self.list_all_professors()
            elif choice == '8':
                self.list_all_courses()
            elif choice == '9':
                self.view_student_details()
            elif choice == '10':
                self.view_professor_details()
            elif choice == '11':
                self.view_course_details()
            elif choice == '12':
                print("Exiting University Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    ums = UniversityManagementSystem()
    ums.run()
