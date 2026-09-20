import json
import os
import uuid

# --- 3.1. Person Class (Base Class) ---
class Person:
    """Represents a generic person in the university system."""
    def __init__(self, _id: str, _name: str):
        self._id = _id # Unique identifier for the person
        self._name = _name # The person's full name

    @property
    def id(self) -> str:
        """Returns the unique ID of the person (read-only)."""
        return self._id

    @property
    def name(self) -> str:
        """Returns the name of the person (read-only)."""
        return self._name

    def __str__(self) -> str:
        """Returns a basic string representation of the person."""
        return f"ID: {self._id}, Name: {self._name}"

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the person's basic attributes,
        useful for saving to file. Includes a 'type' key.
        """
        return {
            'id': self._id,
            'name': self._name,
            'type': 'person' # Default type, overridden by subclasses
        }

# --- 3.2. Student Class ---
class Student(Person):
    """Inherits from Person, representing a university student."""
    def __init__(self, _id: str, _name: str, _major: str):
        super().__init__(_id, _name)
        self._major = _major # The student's major
        self._enrolled_course_codes = [] # List of course_code strings

    @property
    def major(self) -> str:
        """Returns the student's major."""
        return self._major

    @major.setter
    def major(self, new_major: str):
        """Sets the student's major."""
        self._major = new_major

    @property
    def enrolled_course_codes(self) -> list:
        """Returns a copy of the list of enrolled course codes (read-only)."""
        return self._enrolled_course_codes.copy()

    def enroll_course(self, course_code: str) -> None:
        """Adds a course_code to the enrolled courses if not already present."""
        if course_code not in self._enrolled_course_codes:
            self._enrolled_course_codes.append(course_code)
            # print(f"DEBUG: Student {self.name} enrolled in {course_code}")

    def drop_course(self, course_code: str) -> None:
        """Removes a course_code from the enrolled courses."""
        if course_code in self._enrolled_course_codes:
            self._enrolled_course_codes.remove(course_code)
            # print(f"DEBUG: Student {self.name} dropped {course_code}")

    def display_details(self) -> str:
        """
        Overrides parent. Returns a string including inherited details plus major
        and number of enrolled courses.
        """
        return (f"Student: {self._name} (ID: {self._id})\n"
                f"  Major: {self._major}\n"
                f"  Enrolled Courses: {len(self._enrolled_course_codes)}")

    def to_dict(self) -> dict:
        """
        Overrides parent. Returns dictionary including _major,
        _enrolled_course_codes, and type: 'student'.
        """
        data = super().to_dict()
        data.update({
            'major': self._major,
            'enrolled_course_codes': self._enrolled_course_codes,
            'type': 'student'
        })
        return data

# --- 3.3. Faculty Class ---
class Faculty(Person):
    """Inherits from Person, representing a university faculty member."""
    def __init__(self, _id: str, _name: str, _department: str):
        super().__init__(_id, _name)
        self._department = _department # The faculty's department
        self._assigned_course_codes = [] # List of course_code strings

    @property
    def department(self) -> str:
        """Returns the faculty's department."""
        return self._department

    @department.setter
    def department(self, new_department: str):
        """Sets the faculty's department."""
        self._department = new_department

    @property
    def assigned_course_codes(self) -> list:
        """Returns a copy of the list of assigned course codes (read-only)."""
        return self._assigned_course_codes.copy()

    def assign_course(self, course_code: str) -> None:
        """Adds a course_code to the assigned courses if not already present."""
        if course_code not in self._assigned_course_codes:
            self._assigned_course_codes.append(course_code)
            # print(f"DEBUG: Faculty {self.name} assigned to {course_code}")

    def unassign_course(self, course_code: str) -> None:
        """Removes a course_code from the assigned courses."""
        if course_code in self._assigned_course_codes:
            self._assigned_course_codes.remove(course_code)
            # print(f"DEBUG: Faculty {self.name} unassigned from {course_code}")

    def display_details(self) -> str:
        """
        Overrides parent. Returns a string including inherited details plus
        department and number of assigned courses.
        """
        return (f"Faculty: {self._name} (ID: {self._id})\n"
                f"  Department: {self._department}\n"
                f"  Assigned Courses: {len(self._assigned_course_codes)}")

    def to_dict(self) -> dict:
        """
        Overrides parent. Returns dictionary including _department,
        _assigned_course_codes, and type: 'faculty'.
        """
        data = super().to_dict()
        data.update({
            'department': self._department,
            'assigned_course_codes': self._assigned_course_codes,
            'type': 'faculty'
        })
        return data

# --- 3.4. Course Class ---
class Course:
    """Represents a university course."""
    def __init__(self, _course_code: str, _title: str, _credits: int, _prerequisite_codes: list = None):
        self._course_code = _course_code.upper() # Unique identifier for the course
        self._title = _title # The course title
        self._credits = _credits # The number of credits for the course
        self._prerequisite_codes = _prerequisite_codes if _prerequisite_codes is not None else [] # List of course_code strings for prerequisites
        self._enrolled_student_ids = [] # List of student_id strings for enrolled students
        self._assigned_faculty_id = None # The id of the assigned faculty, None if no faculty is assigned.

    @property
    def course_code(self) -> str:
        """Returns the course code (read-only)."""
        return self._course_code

    @property
    def title(self) -> str:
        """Returns the course title (read-only)."""
        return self._title

    @property
    def credits(self) -> int:
        """Returns the number of credits for the course (read-only)."""
        return self._credits

    @property
    def prerequisite_codes(self) -> list:
        """Returns a copy of the list of prerequisite course codes (read-only)."""
        return self._prerequisite_codes.copy()

    @property
    def enrolled_student_ids(self) -> list:
        """Returns a copy of the list of enrolled student IDs (read-only)."""
        return self._enrolled_student_ids.copy()

    @property
    def assigned_faculty_id(self) -> str or None:
        """Returns the ID of the assigned faculty."""
        return self._assigned_faculty_id

    @assigned_faculty_id.setter
    def assigned_faculty_id(self, faculty_id: str or None):
        """Sets the ID of the assigned faculty."""
        self._assigned_faculty_id = faculty_id

    def add_prerequisite(self, prerequisite_code: str) -> None:
        """Adds a prerequisite_code to the list of prerequisites."""
        if prerequisite_code not in self._prerequisite_codes:
            self._prerequisite_codes.append(prerequisite_code)

    def add_student_id(self, student_id: str) -> None:
        """Adds a student_id to the enrolled students if not already present."""
        if student_id not in self._enrolled_student_ids:
            self._enrolled_student_ids.append(student_id)
            # print(f"DEBUG: Course {self.course_code} added student {student_id}")

    def remove_student_id(self, student_id: str) -> None:
        """Removes a student_id from the enrolled students."""
        if student_id in self._enrolled_student_ids:
            self._enrolled_student_ids.remove(student_id)
            # print(f"DEBUG: Course {self.course_code} removed student {student_id}")

    def assign_faculty_id(self, faculty_id: str) -> None:
        """Assigns faculty_id to the course."""
        self._assigned_faculty_id = faculty_id
        # print(f"DEBUG: Course {self.course_code} assigned to faculty {faculty_id}")


    def unassign_faculty_id(self) -> None:
        """Sets _assigned_faculty_id to None."""
        self._assigned_faculty_id = None
        # print(f"DEBUG: Course {self.course_code} unassigned faculty")

    def display_details(self) -> str:
        """
        Returns a string including course details, prerequisites, number of
        enrolled students, and assigned faculty ID (if any).
        """
        prereqs_str = ", ".join(self._prerequisite_codes) if self._prerequisite_codes else "None"
        faculty_str = self._assigned_faculty_id if self._assigned_faculty_id else "None"
        return (f"Course: {self._title} (Code: {self._course_code})\n"
                f"  Credits: {self._credits}\n"
                f"  Prerequisites: {prereqs_str}\n"
                f"  Enrolled Students: {len(self._enrolled_student_ids)}\n"
                f"  Assigned Faculty ID: {faculty_str}")

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the course's attributes, useful for
        saving to file.
        """
        return {
            'course_code': self._course_code,
            'title': self._title,
            'credits': self._credits,
            'prerequisite_codes': self._prerequisite_codes,
            'enrolled_student_ids': self._enrolled_student_ids,
            'assigned_faculty_id': self._assigned_faculty_id
        }

# --- 3.5. University Class ---
class University:
    """
    The main orchestrator class, managing all Student, Faculty, and Course objects.
    Handles data persistence to JSON files.
    """
    def __init__(self, student_file='students.json', faculty_file='faculty.json', course_file='courses.json'):
        self._students = {} # Dictionary: student_id -> Student object.
        self._faculty = {} # Dictionary: faculty_id -> Faculty object.
        self._courses = {} # Dictionary: course_code -> Course object.
        self._student_file = student_file
        self._faculty_file = faculty_file
        self._course_file = course_file
        self._load_data() # Load existing data from files on initialization

    def _load_data(self) -> None:
        """
        (Private Helper Method)
        Loads student, faculty, and course data from their respective files.
        Handles FileNotFoundError.
        Crucial for Relationships: After loading all entities, "re-link" them.
        """
        print("Loading data...")
        # Load Students
        if os.path.exists(self._student_file):
            try:
                with open(self._student_file, 'r') as f:
                    students_data = json.load(f)
                    for data in students_data:
                        student = Student(data['id'], data['name'], data['major'])
                        student._enrolled_course_codes = data.get('enrolled_course_codes', [])
                        self._students[student.id] = student
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading students data: {e}")
        else:
            print(f"'{self._student_file}' not found. Starting with no students.")

        # Load Faculty
        if os.path.exists(self._faculty_file):
            try:
                with open(self._faculty_file, 'r') as f:
                    faculty_data = json.load(f)
                    for data in faculty_data:
                        faculty = Faculty(data['id'], data['name'], data['department'])
                        faculty._assigned_course_codes = data.get('assigned_course_codes', [])
                        self._faculty[faculty.id] = faculty
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading faculty data: {e}")
        else:
            print(f"'{self._faculty_file}' not found. Starting with no faculty.")

        # Load Courses
        if os.path.exists(self._course_file):
            try:
                with open(self._course_file, 'r') as f:
                    courses_data = json.load(f)
                    for data in courses_data:
                        course = Course(data['course_code'], data['title'], data['credits'],
                                        data.get('prerequisite_codes', []))
                        course._enrolled_student_ids = data.get('enrolled_student_ids', [])
                        course._assigned_faculty_id = data.get('assigned_faculty_id')
                        self._courses[course.course_code] = course
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading courses data: {e}")
        else:
            print(f"'{self._course_file}' not found. Starting with no courses.")

        # Re-link relationships after loading all objects
        self._relink_data()
        print("Data loaded and relationships re-linked.")

    def _relink_data(self) -> None:
        """
        Re-establishes relationships between loaded objects.
        This is crucial because JSON serialization breaks object references.
        """
        # Re-link students to courses (for enrolled_course_codes)
        for student_id, student in self._students.items():
            valid_courses = []
            for course_code in student._enrolled_course_codes:
                if course_code in self._courses:
                    # Enroll student in course (adds student ID to course's list)
                    self._courses[course_code].add_student_id(student_id)
                    valid_courses.append(course_code)
                else:
                    print(f"Warning: Course '{course_code}' for student '{student.name}' not found. Skipping enrollment.")
            student._enrolled_course_codes = valid_courses # Clean up invalid course codes

        # Re-link faculty to courses (for assigned_course_codes)
        for faculty_id, faculty in self._faculty.items():
            valid_courses = []
            for course_code in faculty._assigned_course_codes:
                if course_code in self._courses:
                    # Assign faculty to course (sets faculty ID in course)
                    self._courses[course_code].assign_faculty_id(faculty_id)
                    valid_courses.append(course_code)
                else:
                    print(f"Warning: Course '{course_code}' for faculty '{faculty.name}' not found. Skipping assignment.")
            faculty._assigned_course_codes = valid_courses # Clean up invalid course codes

        # Validate Course assigned_faculty_id and enrolled_student_ids
        for course_code, course in self._courses.items():
            if course.assigned_faculty_id and course.assigned_faculty_id not in self._faculty:
                print(f"Warning: Assigned faculty ID '{course.assigned_faculty_id}' for course '{course.title}' not found. Unassigning.")
                course.unassign_faculty_id()
            
            valid_enrolled_students = []
            for student_id in course._enrolled_student_ids:
                if student_id in self._students:
                    valid_enrolled_students.append(student_id)
                else:
                    print(f"Warning: Enrolled student ID '{student_id}' in course '{course.title}' not found. Removing from roster.")
            course._enrolled_student_ids = valid_enrolled_students


    def _save_data(self) -> None:
        """
        (Private Helper Method)
        Saves current _students, _faculty, and _courses data to their
        respective JSON files. Iterates through collections and calls to_dict()
        on each object before saving.
        """
        try:
            # Save Students
            with open(self._student_file, 'w') as f:
                json.dump([s.to_dict() for s in self._students.values()], f, indent=4)
            # Save Faculty
            with open(self._faculty_file, 'w') as f:
                json.dump([fa.to_dict() for fa in self._faculty.values()], f, indent=4)
            # Save Courses
            with open(self._course_file, 'w') as f:
                json.dump([c.to_dict() for c in self._courses.values()], f, indent=4)
            print("Data saved successfully.")
        except IOError as e:
            print(f"Error saving data: {e}")

    def add_student(self, student: Student) -> bool:
        """Adds a Student object. Returns True if added, False if ID exists. Calls _save_data()."""
        if student.id in self._students:
            print(f"Error: Student with ID {student.id} already exists.")
            return False
        self._students[student.id] = student
        self._save_data()
        return True

    def remove_student(self, student_id: str) -> bool:
        """
        Removes a student. Returns True if removed, False if not found or if
        student is enrolled in courses. Calls _save_data().
        """
        if student_id not in self._students:
            print(f"Error: Student with ID {student_id} not found.")
            return False

        student = self._students[student_id]
        if student.enrolled_course_codes:
            print(f"Error: Student {student.name} is enrolled in courses. Drop them first.")
            return False

        del self._students[student_id]
        self._save_data()
        print(f"Student {student.name} removed successfully.")
        return True

    def add_faculty(self, faculty: Faculty) -> bool:
        """Adds a Faculty object. Returns True if added, False if ID exists. Calls _save_data()."""
        if faculty.id in self._faculty:
            print(f"Error: Faculty with ID {faculty.id} already exists.")
            return False
        self._faculty[faculty.id] = faculty
        self._save_data()
        return True

    def remove_faculty(self, faculty_id: str) -> bool:
        """
        Removes faculty. Returns True if removed, False if not found or if
        faculty is assigned to courses. Calls _save_data().
        """
        if faculty_id not in self._faculty:
            print(f"Error: Faculty with ID {faculty_id} not found.")
            return False

        faculty = self._faculty[faculty_id]
        if faculty.assigned_course_codes:
            print(f"Error: Faculty {faculty.name} is assigned to courses. Unassign them first.")
            return False

        del self._faculty[faculty_id]
        self._save_data()
        print(f"Faculty {faculty.name} removed successfully.")
        return True

    def add_course(self, course: Course) -> bool:
        """Adds a Course object. Returns True if added, False if code exists. Calls _save_data()."""
        if course.course_code in self._courses:
            print(f"Error: Course with code {course.course_code} already exists.")
            return False
        self._courses[course.course_code] = course
        self._save_data()
        return True

    def remove_course(self, course_code: str) -> bool:
        """
        Removes a course. Returns True if removed, False if not found or if
        students are enrolled. Calls _save_data().
        """
        if course_code not in self._courses:
            print(f"Error: Course with code {course_code} not found.")
            return False

        course = self._courses[course_code]
        if course.enrolled_student_ids:
            print(f"Error: Course {course.title} has enrolled students. Drop them first.")
            return False

        if course.assigned_faculty_id:
            # Also unassign faculty from their list if the course is removed
            faculty = self._faculty.get(course.assigned_faculty_id)
            if faculty and course_code in faculty.assigned_course_codes:
                faculty.unassign_course(course_code)

        del self._courses[course_code]
        self._save_data()
        print(f"Course {course.title} removed successfully.")
        return True

    def enroll_student_in_course(self, student_id: str, course_code: str) -> bool:
        """
        Checks if student and course exist and prerequisites are met.
        Updates both Student and Course objects' respective lists. Returns
        True on success, False otherwise. Calls _save_data().
        """
        student = self._students.get(student_id)
        course = self._courses.get(course_code)

        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return False

        if course_code in student.enrolled_course_codes:
            print(f"Student {student.name} is already enrolled in {course.title}.")
            return False
        
        # Check prerequisites
        for prereq_code in course.prerequisite_codes:
            if prereq_code not in student.enrolled_course_codes:
                print(f"Error: Student {student.name} has not met prerequisite '{prereq_code}' for '{course.title}'.")
                return False

        student.enroll_course(course_code)
        course.add_student_id(student_id)
        self._save_data()
        print(f"Student {student.name} successfully enrolled in {course.title}.")
        return True

    def drop_student_from_course(self, student_id: str, course_code: str) -> bool:
        """
        Checks if student and course exist and student is enrolled.
        Updates both Student and Course objects. Returns True on success,
        False otherwise. Calls _save_data().
        """
        student = self._students.get(student_id)
        course = self._courses.get(course_code)

        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return False

        if course_code not in student.enrolled_course_codes:
            print(f"Student {student.name} is not enrolled in {course.title}.")
            return False

        student.drop_course(course_code)
        course.remove_student_id(student_id)
        self._save_data()
        print(f"Student {student.name} successfully dropped from {course.title}.")
        return True

    def assign_faculty_to_course(self, faculty_id: str, course_code: str) -> bool:
        """
        Checks if faculty and course exist.
        Updates both Faculty and Course objects. Returns True on success,
        False otherwise. Calls _save_data().
        """
        faculty = self._faculty.get(faculty_id)
        course = self._courses.get(course_code)

        if not faculty:
            print(f"Error: Faculty with ID {faculty_id} not found.")
            return False
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return False

        if course.assigned_faculty_id == faculty_id:
            print(f"Faculty {faculty.name} is already assigned to {course.title}.")
            return False
        
        # If another faculty is already assigned, unassign them first
        if course.assigned_faculty_id:
            old_faculty = self._faculty.get(course.assigned_faculty_id)
            if old_faculty:
                old_faculty.unassign_course(course_code)

        faculty.assign_course(course_code)
        course.assign_faculty_id(faculty_id)
        self._save_data()
        print(f"Faculty {faculty.name} successfully assigned to {course.title}.")
        return True

    def unassign_faculty_from_course(self, faculty_id: str, course_code: str) -> bool:
        """
        Checks if faculty and course exist and are assigned.
        Updates both Faculty and Course objects. Returns True on success,
        False otherwise. Calls _save_data().
        """
        faculty = self._faculty.get(faculty_id)
        course = self._courses.get(course_code)

        if not faculty:
            print(f"Error: Faculty with ID {faculty_id} not found.")
            return False
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return False

        if course.assigned_faculty_id != faculty_id:
            print(f"Faculty {faculty.name} is not assigned to {course.title}.")
            return False

        faculty.unassign_course(course_code)
        course.unassign_faculty_id()
        self._save_data()
        print(f"Faculty {faculty.name} successfully unassigned from {course.title}.")
        return True

    def get_course_roster(self, course_code: str) -> list:
        """
        Returns a list of Student objects enrolled in the specified course.
        Handles course not found.
        """
        course = self._courses.get(course_code)
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return []

        roster = []
        for student_id in course.enrolled_student_ids:
            student = self._students.get(student_id)
            if student:
                roster.append(student)
        return roster

    def display_all_students(self) -> None:
        """Prints details of all registered students."""
        print("\n--- All Registered Students ---")
        if not self._students:
            print("No students registered.")
            return
        for student in self._students.values():
            print(student.display_details())
            print("-" * 30) # Separator
        print("-------------------------------")

    def display_all_faculty(self) -> None:
        """Prints details of all registered faculty."""
        print("\n--- All Registered Faculty ---")
        if not self._faculty:
            print("No faculty registered.")
            return
        for faculty in self._faculty.values():
            print(faculty.display_details())
            print("-" * 30) # Separator
        print("------------------------------")

    def display_all_courses(self) -> None:
        """Prints details of all registered courses."""
        print("\n--- All Registered Courses ---")
        if not self._courses:
            print("No courses available.")
            return
        for course in self._courses.values():
            print(course.display_details())
            print("-" * 30) # Separator
        print("------------------------------")

    def run(self):
        """Main loop for the console application, presenting a menu to the administrator."""
        while True:
            print("\n===== University Management System =====")
            print("1. Add Student")
            print("2. Remove Student")
            print("3. Add Faculty")
            print("4. Remove Faculty")
            print("5. Add Course")
            print("6. Remove Course")
            print("7. Enroll Student in Course")
            print("8. Drop Student from Course")
            print("9. Assign Faculty to Course")
            print("10. Unassign Faculty from Course")
            print("11. View Course Roster")
            print("12. Display All Students")
            print("13. Display All Faculty")
            print("14. Display All Courses")
            print("15. Exit")
            print("========================================")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                name = input("Enter student name: ")
                major = input("Enter student major: ")
                # Generate a unique ID for new students
                student_id = str(uuid.uuid4())
                student = Student(student_id, name, major)
                self.add_student(student)
            elif choice == '2':
                student_id = input("Enter student ID to remove: ")
                self.remove_student(student_id)
            elif choice == '3':
                name = input("Enter faculty name: ")
                department = input("Enter faculty department: ")
                # Generate a unique ID for new faculty
                faculty_id = str(uuid.uuid4())
                faculty = Faculty(faculty_id, name, department)
                self.add_faculty(faculty)
            elif choice == '4':
                faculty_id = input("Enter faculty ID to remove: ")
                self.remove_faculty(faculty_id)
            elif choice == '5':
                course_code = input("Enter course code (e.g., CS101): ").upper()
                title = input("Enter course title: ")
                try:
                    credits = int(input("Enter number of credits: "))
                    prereqs_input = input("Enter prerequisite course codes (comma-separated, leave blank if none): ")
                    prerequisites = [p.strip().upper() for p in prereqs_input.split(',') if p.strip()]
                    course = Course(course_code, title, credits, prerequisites)
                    self.add_course(course)
                except ValueError:
                    print("Invalid input for credits. Please enter a number.")
            elif choice == '6':
                course_code = input("Enter course code to remove: ").upper()
                self.remove_course(course_code)
            elif choice == '7':
                student_id = input("Enter student ID to enroll: ")
                course_code = input("Enter course code to enroll in: ").upper()
                self.enroll_student_in_course(student_id, course_code)
            elif choice == '8':
                student_id = input("Enter student ID to drop: ")
                course_code = input("Enter course code to drop from: ").upper()
                self.drop_student_from_course(student_id, course_code)
            elif choice == '9':
                faculty_id = input("Enter faculty ID to assign: ")
                course_code = input("Enter course code to assign to: ").upper()
                self.assign_faculty_to_course(faculty_id, course_code)
            elif choice == '10':
                faculty_id = input("Enter faculty ID to unassign: ")
                course_code = input("Enter course code to unassign from: ").upper()
                self.unassign_faculty_from_course(faculty_id, course_code)
            elif choice == '11':
                course_code = input("Enter course code to view roster: ").upper()
                roster = self.get_course_roster(course_code)
                if roster:
                    print(f"\n--- Roster for {course_code} ---")
                    for student in roster:
                        print(f"- {student.name} (ID: {student.id}, Major: {student.major})")
                    print("----------------------------")
                elif course_code in self._courses:
                    print(f"No students enrolled in {self._courses[course_code].title}.")
            elif choice == '12':
                self.display_all_students()
            elif choice == '13':
                self.display_all_faculty()
            elif choice == '14':
                self.display_all_courses()
            elif choice == '15':
                print("Exiting University Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    # Ensure current working directory exists for saving files
    if not os.path.exists(os.getcwd()):
        os.makedirs(os.getcwd())

    ums = University()
    ums.run()
