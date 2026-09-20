import json
import os

# --- 1. Person Class (Base Class) ---
class Person:
    def __init__(self, id: str, name: str):
        self._id = id  # This is like a private variable
        self._name = name  # This is also a private-like variable

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"ID: {self._id}, Name: {self._name}"

    def to_dict(self) -> dict:
        # This helps us save the person's basic info to a file
        return {"id": self._id, "name": self._name}

# --- 2. Student Class ---
class Student(Person): # Student is a type of Person, so it inherits from Person
    def __init__(self, id: str, name: str, major: str):
        super().__init__(id, name) # Call the Person's constructor first
        self._major = major
        self._enrolled_course_codes = [] # Students start with no courses

    @property
    def major(self) -> str:
        return self._major

    @major.setter
    def major(self, new_major: str):
        self._major = new_major

    @property
    def enrolled_course_codes(self) -> list[str]:
        return self._enrolled_course_codes.copy() # Return a copy so the original list isn't changed directly

    def enroll_course(self, course_code: str) -> None:
        if course_code not in self._enrolled_course_codes:
            self._enrolled_course_codes.append(course_code)
            print(f"Student {self.name} enrolled in {course_code}")
        else:
            print(f"Student {self.name} is already enrolled in {course_code}")

    def drop_course(self, course_code: str) -> None:
        if course_code in self._enrolled_course_codes:
            self._enrolled_course_codes.remove(course_code)
            print(f"Student {self.name} dropped {course_code}")
        else:
            print(f"Student {self.name} was not enrolled in {course_code}")

    def display_details(self) -> str:
        # Show inherited details plus student-specific info
        return (f"{super().__str__()}, Major: {self._major}, "
                f"Enrolled Courses: {len(self._enrolled_course_codes)}")

    def to_dict(self) -> dict:
        # Add student specific attributes to the dictionary for saving
        data = super().to_dict()
        data['type'] = 'student' # This helps us know it's a student when loading
        data['major'] = self._major
        data['enrolled_course_codes'] = self._enrolled_course_codes
        return data

# --- 3. Faculty Class ---
class Faculty(Person): # Faculty also inherits from Person
    def __init__(self, id: str, name: str, department: str):
        super().__init__(id, name) # Call the Person's constructor
        self._department = department
        self._assigned_course_codes = [] # Faculty start with no assigned courses

    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, new_department: str):
        self._department = new_department

    @property
    def assigned_course_codes(self) -> list[str]:
        return self._assigned_course_codes.copy() # Return a copy

    def assign_course(self, course_code: str) -> None:
        if course_code not in self._assigned_course_codes:
            self._assigned_course_codes.append(course_code)
            print(f"Faculty {self.name} assigned to {course_code}")
        else:
            print(f"Faculty {self.name} is already assigned to {course_code}")

    def unassign_course(self, course_code: str) -> None:
        if course_code in self._assigned_course_codes:
            self._assigned_course_codes.remove(course_code)
            print(f"Faculty {self.name} unassigned from {course_code}")
        else:
            print(f"Faculty {self.name} was not assigned to {course_code}")

    def display_details(self) -> str:
        # Show inherited details plus faculty-specific info
        return (f"{super().__str__()}, Department: {self._department}, "
                f"Assigned Courses: {len(self._assigned_course_codes)}")

    def to_dict(self) -> dict:
        # Add faculty specific attributes for saving
        data = super().to_dict()
        data['type'] = 'faculty' # Helps identify as faculty when loading
        data['department'] = self._department
        data['assigned_course_codes'] = self._assigned_course_codes
        return data

# --- 4. Course Class ---
class Course:
    def __init__(self, course_code: str, title: str, credits: int, prerequisites: list[str]):
        self._course_code = course_code
        self._title = title
        self._credits = credits
        self._prerequisite_codes = prerequisites if prerequisites is not None else []
        self._enrolled_student_ids = []
        self._assigned_faculty_id = None # No faculty assigned at the start

    @property
    def course_code(self) -> str:
        return self._course_code

    @property
    def title(self) -> str:
        return self._title

    @property
    def credits(self) -> int:
        return self._credits

    @property
    def prerequisite_codes(self) -> list[str]:
        return self._prerequisite_codes.copy()

    @property
    def enrolled_student_ids(self) -> list[str]:
        return self._enrolled_student_ids.copy()

    @property
    def assigned_faculty_id(self) -> str | None:
        return self._assigned_faculty_id

    @assigned_faculty_id.setter
    def assigned_faculty_id(self, faculty_id: str | None):
        self._assigned_faculty_id = faculty_id

    def add_prerequisite(self, prerequisite_code: str) -> None:
        if prerequisite_code not in self._prerequisite_codes:
            self._prerequisite_codes.append(prerequisite_code)
            print(f"Prerequisite {prerequisite_code} added to {self.title}")
        else:
            print(f"{prerequisite_code} is already a prerequisite for {self.title}")

    def add_student_id(self, student_id: str) -> None:
        if student_id not in self._enrolled_student_ids:
            self._enrolled_student_ids.append(student_id)
            print(f"Student ID {student_id} added to {self.title}")
        else:
            print(f"Student ID {student_id} is already enrolled in {self.title}")

    def remove_student_id(self, student_id: str) -> None:
        if student_id in self._enrolled_student_ids:
            self._enrolled_student_ids.remove(student_id)
            print(f"Student ID {student_id} removed from {self.title}")
        else:
            print(f"Student ID {student_id} not found in {self.title} enrollments.")

    def assign_faculty_id(self, faculty_id: str) -> None:
        self._assigned_faculty_id = faculty_id
        print(f"Faculty ID {faculty_id} assigned to {self.title}")

    def unassign_faculty_id(self) -> None:
        self._assigned_faculty_id = None
        print(f"Faculty unassigned from {self.title}")

    def display_details(self) -> str:
        prereqs = ", ".join(self._prerequisite_codes) if self._prerequisite_codes else "None"
        faculty_info = self._assigned_faculty_id if self._assigned_faculty_id else "Not Assigned"
        return (f"Course Code: {self._course_code}, Title: {self._title}, Credits: {self._credits}\n"
                f"  Prerequisites: {prereqs}\n"
                f"  Enrolled Students: {len(self._enrolled_student_ids)}\n"
                f"  Assigned Faculty ID: {faculty_info}")

    def to_dict(self) -> dict:
        # All course attributes go into the dictionary for saving
        return {
            "course_code": self._course_code,
            "title": self._title,
            "credits": self._credits,
            "prerequisite_codes": self._prerequisite_codes,
            "enrolled_student_ids": self._enrolled_student_ids,
            "assigned_faculty_id": self._assigned_faculty_id
        }

# --- 5. University Class (The Main Brain) ---
class University:
    def __init__(self, student_file='students.json', faculty_file='faculty.json', course_file='courses.json'):
        self._students = {} # Stores Student objects, like a database
        self._faculty = {} # Stores Faculty objects
        self._courses = {} # Stores Course objects
        self._student_file = student_file
        self._faculty_file = faculty_file
        self._course_file = course_file
        self._load_data() # Try to load any existing data when the university system starts

    def _load_data(self) -> None:
        # Load students
        try:
            with open(self._student_file, 'r') as f:
                student_data = json.load(f)
                for data in student_data:
                    # We need to create a Student object from the loaded data
                    student = Student(data['id'], data['name'], data['major'])
                    student._enrolled_course_codes = data['enrolled_course_codes'] # Directly set for loading
                    self._students[student.id] = student
            print(f"Loaded {len(self._students)} students.")
        except FileNotFoundError:
            print(f"No student data file found: {self._student_file}. Starting fresh.")
        except Exception as e:
            print(f"Error loading student data: {e}")

        # Load faculty
        try:
            with open(self._faculty_file, 'r') as f:
                faculty_data = json.load(f)
                for data in faculty_data:
                    # Create Faculty object from loaded data
                    faculty = Faculty(data['id'], data['name'], data['department'])
                    faculty._assigned_course_codes = data['assigned_course_codes'] # Directly set for loading
                    self._faculty[faculty.id] = faculty
            print(f"Loaded {len(self._faculty)} faculty members.")
        except FileNotFoundError:
            print(f"No faculty data file found: {self._faculty_file}. Starting fresh.")
        except Exception as e:
            print(f"Error loading faculty data: {e}")

        # Load courses
        try:
            with open(self._course_file, 'r') as f:
                course_data = json.load(f)
                for data in course_data:
                    # Create Course object from loaded data
                    course = Course(data['course_code'], data['title'], data['credits'], data['prerequisite_codes'])
                    course._enrolled_student_ids = data['enrolled_student_ids'] # Directly set for loading
                    course._assigned_faculty_id = data['assigned_faculty_id'] # Directly set for loading
                    self._courses[course.course_code] = course
            print(f"Loaded {len(self._courses)} courses.")
        except FileNotFoundError:
            print(f"No course data file found: {self._course_file}. Starting fresh.")
        except Exception as e:
            print(f"Error loading course data: {e}")

        # --- IMPORTANT: Re-link relationships after loading! ---
        # This part makes sure our objects are consistent with each other.
        print("Re-linking relationships...")
        for student in self._students.values():
            # Check if enrolled courses actually exist in our _courses dictionary
            valid_courses = []
            for course_code in student._enrolled_course_codes:
                if course_code in self._courses:
                    valid_courses.append(course_code)
                else:
                    print(f"Warning: Course {course_code} for student {student.id} not found. Removing from enrollment.")
            student._enrolled_course_codes = valid_courses # Update the student's list

        for faculty_member in self._faculty.values():
            # Check if assigned courses actually exist
            valid_courses = []
            for course_code in faculty_member._assigned_course_codes:
                if course_code in self._courses:
                    valid_courses.append(course_code)
                else:
                    print(f"Warning: Course {course_code} for faculty {faculty_member.id} not found. Removing from assignment.")
            faculty_member._assigned_course_codes = valid_courses # Update the faculty's list

        for course in self._courses.values():
            # Check if enrolled students actually exist
            valid_students = []
            for student_id in course._enrolled_student_ids:
                if student_id in self._students:
                    valid_students.append(student_id)
                else:
                    print(f"Warning: Student {student_id} in course {course.course_code} not found. Removing from roster.")
            course._enrolled_student_ids = valid_students # Update the course's enrolled students

            # Check if assigned faculty actually exists
            if course._assigned_faculty_id and course._assigned_faculty_id not in self._faculty:
                print(f"Warning: Faculty {course._assigned_faculty_id} for course {course.course_code} not found. Unassigning.")
                course._assigned_faculty_id = None

    def _save_data(self) -> None:
        # Save students
        student_data = [s.to_dict() for s in self._students.values()]
        with open(self._student_file, 'w') as f:
            json.dump(student_data, f, indent=4)

        # Save faculty
        faculty_data = [f.to_dict() for f in self._faculty.values()]
        with open(self._faculty_file, 'w') as f:
            json.dump(faculty_data, f, indent=4)

        # Save courses
        course_data = [c.to_dict() for c in self._courses.values()]
        with open(self._course_file, 'w') as f:
            json.dump(course_data, f, indent=4)
        print("All data saved!")

    def add_student(self, student: Student) -> bool:
        if student.id in self._students:
            print(f"Student with ID {student.id} already exists.")
            return False
        self._students[student.id] = student
        self._save_data()
        print(f"Student {student.name} added successfully.")
        return True

    def remove_student(self, student_id: str) -> bool:
        if student_id not in self._students:
            print(f"Student with ID {student_id} not found.")
            return False
        
        student_to_remove = self._students[student_id]
        if student_to_remove.enrolled_course_codes: # Check if student is in any courses
            print(f"Cannot remove student {student_id}. They are enrolled in courses.")
            return False
            
        del self._students[student_id]
        self._save_data()
        print(f"Student with ID {student_id} removed successfully.")
        return True

    def add_faculty(self, faculty: Faculty) -> bool:
        if faculty.id in self._faculty:
            print(f"Faculty with ID {faculty.id} already exists.")
            return False
        self._faculty[faculty.id] = faculty
        self._save_data()
        print(f"Faculty {faculty.name} added successfully.")
        return True

    def remove_faculty(self, faculty_id: str) -> bool:
        if faculty_id not in self._faculty:
            print(f"Faculty with ID {faculty_id} not found.")
            return False

        faculty_to_remove = self._faculty[faculty_id]
        if faculty_to_remove.assigned_course_codes: # Check if faculty is assigned to any courses
            print(f"Cannot remove faculty {faculty_id}. They are assigned to courses.")
            return False
            
        del self._faculty[faculty_id]
        self._save_data()
        print(f"Faculty with ID {faculty_id} removed successfully.")
        return True

    def add_course(self, course: Course) -> bool:
        if course.course_code in self._courses:
            print(f"Course with code {course.course_code} already exists.")
            return False
        self._courses[course.course_code] = course
        self._save_data()
        print(f"Course {course.title} added successfully.")
        return True

    def remove_course(self, course_code: str) -> bool:
        if course_code not in self._courses:
            print(f"Course with code {course_code} not found.")
            return False
        
        course_to_remove = self._courses[course_code]
        if course_to_remove.enrolled_student_ids: # Check if students are enrolled
            print(f"Cannot remove course {course_code}. Students are enrolled in it.")
            return False

        del self._courses[course_code]
        self._save_data()
        print(f"Course {course_code} removed successfully.")
        return True

    def enroll_student_in_course(self, student_id: str, course_code: str) -> bool:
        student = self._students.get(student_id)
        course = self._courses.get(course_code)

        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return False
        
        # Check prerequisites
        for prereq_code in course.prerequisite_codes:
            if prereq_code not in student.enrolled_course_codes:
                print(f"Error: Student {student.name} has not met prerequisite {prereq_code} for {course.title}.")
                return False

        # Update both student and course
        if course_code not in student.enrolled_course_codes:
            student.enroll_course(course_code)
        if student_id not in course.enrolled_student_ids:
            course.add_student_id(student_id)
        
        self._save_data()
        print(f"Student {student.name} successfully enrolled in {course.title}.")
        return True

    def drop_student_from_course(self, student_id: str, course_code: str) -> bool:
        student = self._students.get(student_id)
        course = self._courses.get(course_code)

        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return False
        if course_code not in student.enrolled_course_codes:
            print(f"Error: Student {student.name} is not enrolled in {course.title}.")
            return False

        # Update both student and course
        student.drop_course(course_code)
        course.remove_student_id(student_id)
        
        self._save_data()
        print(f"Student {student.name} successfully dropped from {course.title}.")
        return True

    def assign_faculty_to_course(self, faculty_id: str, course_code: str) -> bool:
        faculty = self._faculty.get(faculty_id)
        course = self._courses.get(course_code)

        if not faculty:
            print(f"Error: Faculty with ID {faculty_id} not found.")
            return False
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return False
        
        # Check if course already has a faculty
        if course.assigned_faculty_id and course.assigned_faculty_id != faculty_id:
            print(f"Course {course.title} already has faculty {course.assigned_faculty_id} assigned. Unassign them first.")
            return False

        # Update both faculty and course
        faculty.assign_course(course_code)
        course.assign_faculty_id(faculty_id)
        
        self._save_data()
        print(f"Faculty {faculty.name} successfully assigned to {course.title}.")
        return True

    def unassign_faculty_from_course(self, faculty_id: str, course_code: str) -> bool:
        faculty = self._faculty.get(faculty_id)
        course = self._courses.get(course_code)

        if not faculty:
            print(f"Error: Faculty with ID {faculty_id} not found.")
            return False
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return False
        if course.assigned_faculty_id != faculty_id:
            print(f"Error: Faculty {faculty.name} is not assigned to {course.title}.")
            return False

        # Update both faculty and course
        faculty.unassign_course(course_code)
        course.unassign_faculty_id()
        
        self._save_data()
        print(f"Faculty {faculty.name} successfully unassigned from {course.title}.")
        return True

    def get_course_roster(self, course_code: str) -> list[Student]:
        course = self._courses.get(course_code)
        if not course:
            print(f"Error: Course with code {course_code} not found.")
            return []

        roster_students = []
        for student_id in course.enrolled_student_ids:
            student = self._students.get(student_id)
            if student: # Make sure the student actually exists
                roster_students.append(student)
        return roster_students

    def display_all_students(self) -> None:
        if not self._students:
            print("No students registered yet.")
            return
        print("\n--- All Registered Students ---")
        for student in self._students.values():
            print(student.display_details())
        print("-------------------------------")

    def display_all_faculty(self) -> None:
        if not self._faculty:
            print("No faculty members registered yet.")
            return
        print("\n--- All Registered Faculty ---")
        for faculty in self._faculty.values():
            print(faculty.display_details())
        print("------------------------------")

    def display_all_courses(self) -> None:
        if not self._courses:
            print("No courses registered yet.")
            return
        print("\n--- All Registered Courses ---")
        for course in self._courses.values():
            print(course.display_details())
        print("------------------------------")

# --- Console Interface (How the user interacts with the system) ---
def main():
    university = University() # This loads existing data or starts fresh

    while True: # Keep running until the user decides to exit
        print("\n===== University Management System Menu =====")
        print("1. Add Student")
        print("2. Add Faculty")
        print("3. Add Course")
        print("4. Enroll Student in Course")
        print("5. Drop Student from Course")
        print("6. Assign Faculty to Course")
        print("7. Unassign Faculty from Course")
        print("8. View Course Roster")
        print("9. Display All Students")
        print("10. Display All Faculty")
        print("11. Display All Courses")
        print("12. Remove Student")
        print("13. Remove Faculty")
        print("14. Remove Course")
        print("15. Exit")
        print("==============================================")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n--- Add New Student ---")
            student_id = input("Enter student ID: ")
            student_name = input("Enter student name: ")
            student_major = input("Enter student major: ")
            new_student = Student(student_id, student_name, student_major)
            university.add_student(new_student)
        elif choice == '2':
            print("\n--- Add New Faculty ---")
            faculty_id = input("Enter faculty ID: ")
            faculty_name = input("Enter faculty name: ")
            faculty_department = input("Enter faculty department: ")
            new_faculty = Faculty(faculty_id, faculty_name, faculty_department)
            university.add_faculty(new_faculty)
        elif choice == '3':
            print("\n--- Add New Course ---")
            course_code = input("Enter course code (e.g., CS101): ")
            course_title = input("Enter course title: ")
            try:
                course_credits = int(input("Enter course credits: "))
            except ValueError:
                print("Invalid credits. Please enter a number.")
                continue
            prereq_input = input("Enter prerequisite course codes (comma-separated, leave blank if none): ")
            prerequisites = [p.strip() for p in prereq_input.split(',') if p.strip()]
            new_course = Course(course_code, course_title, course_credits, prerequisites)
            university.add_course(new_course)
        elif choice == '4':
            print("\n--- Enroll Student in Course ---")
            student_id = input("Enter student ID: ")
            course_code = input("Enter course code: ")
            university.enroll_student_in_course(student_id, course_code)
        elif choice == '5':
            print("\n--- Drop Student from Course ---")
            student_id = input("Enter student ID: ")
            course_code = input("Enter course code: ")
            university.drop_student_from_course(student_id, course_code)
        elif choice == '6':
            print("\n--- Assign Faculty to Course ---")
            faculty_id = input("Enter faculty ID: ")
            course_code = input("Enter course code: ")
            university.assign_faculty_to_course(faculty_id, course_code)
        elif choice == '7':
            print("\n--- Unassign Faculty from Course ---")
            faculty_id = input("Enter faculty ID: ")
            course_code = input("Enter course code: ")
            university.unassign_faculty_from_course(faculty_id, course_code)
        elif choice == '8':
            print("\n--- View Course Roster ---")
            course_code = input("Enter course code: ")
            roster = university.get_course_roster(course_code)
            if roster:
                print(f"\nStudents enrolled in {course_code}:")
                for student in roster:
                    print(f"  - {student.name} (ID: {student.id})")
            elif course_code in university._courses: # Check if course exists but has no students
                 print(f"No students enrolled in {course_code} yet.")
        elif choice == '9':
            university.display_all_students()
        elif choice == '10':
            university.display_all_faculty()
        elif choice == '11':
            university.display_all_courses()
        elif choice == '12':
            print("\n--- Remove Student ---")
            student_id = input("Enter student ID to remove: ")
            university.remove_student(student_id)
        elif choice == '13':
            print("\n--- Remove Faculty ---")
            faculty_id = input("Enter faculty ID to remove: ")
            university.remove_faculty(faculty_id)
        elif choice == '14':
            print("\n--- Remove Course ---")
            course_code = input("Enter course code to remove: ")
            university.remove_course(course_code)
        elif choice == '15':
            print("Exiting University Management System. Goodbye!")
            break # Exit the loop
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

