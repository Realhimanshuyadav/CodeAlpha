import json
import os

class Person:
    """
    Represents a generic person in the university system.
    """
    def __init__(self, id: str, name: str):
        """
        Constructor. Initializes _id and _name.
        """
        self._id = id  # 
        self._name = name  # 

    @property
    def id(self) -> str:
        """
        Returns _id. 
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Returns _name. 
        """
        return self._name

    def __str__(self) -> str:
        """
        Returns a basic string representation: "ID: [ID], Name: [Name]". 
        """
        return f"ID: {self._id}, Name: {self._name}"

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the person's basic attributes, useful for saving to file. 
        Include a type key (e.g., 'student', 'faculty'). 
        """
        return {"id": self._id, "name": self._name}


class Student(Person):
    """
    Inherits from Person, representing a university student. 
    """
    def __init__(self, id: str, name: str, major: str):
        """
        Constructor. Calls parent __init__ and initializes _major. 
        _enrolled_course_codes starts as empty. 
        """
        super().__init__(id, name)
        self._major = major  # 
        self._enrolled_course_codes = []  # 

    @property
    def major(self) -> str:
        """
        Returns/sets _major. 
        """
        return self._major

    @major.setter
    def major(self, major: str) -> None:
        self._major = major

    @property
    def enrolled_course_codes(self) -> list[str]:
        """
        Returns a copy of _enrolled_course_codes. 
        """
        return self._enrolled_course_codes.copy()

    def enroll_course(self, course_code: str) -> None:
        """
        Adds course_code to _enrolled_course_codes if not already present. 
        """
        if course_code not in self._enrolled_course_codes:
            self._enrolled_course_codes.append(course_code)

    def drop_course(self, course_code: str) -> None:
        """
        Removes course_code from _enrolled_course_codes. 
        """
        if course_code in self._enrolled_course_codes:
            self._enrolled_course_codes.remove(course_code)

    def display_details(self) -> str:
        """
        Overrides parent. Returns a string including inherited details plus major and number of enrolled courses. 
        """
        return (f"{super().__str__()}, Major: {self._major}, "
                f"Enrolled Courses: {len(self._enrolled_course_codes)}")

    def to_dict(self) -> dict:
        """
        Overrides parent. Returns dictionary including _major, _enrolled_course_codes, and type: 'student'. 
        """
        data = super().to_dict()
        data.update({
            "type": "student",  # 
            "major": self._major,  # 
            "enrolled_course_codes": self._enrolled_course_codes  # 
        })
        return data


class Faculty(Person):
    """
    Inherits from Person, representing a university faculty member. 
    """
    def __init__(self, id: str, name: str, department: str):
        """
        Constructor. Calls parent __init__ and initializes _department. 
        _assigned_course_codes starts as empty. 
        """
        super().__init__(id, name)
        self._department = department  # 
        self._assigned_course_codes = []  # 

    @property
    def department(self) -> str:
        """
        Returns/sets _department. 
        """
        return self._department

    @department.setter
    def department(self, department: str) -> None:
        self._department = department

    @property
    def assigned_course_codes(self) -> list[str]:
        """
        Returns a copy of _assigned_course_codes. 
        """
        return self._assigned_course_codes.copy()

    def assign_course(self, course_code: str) -> None:
        """
        Adds course_code to _assigned_course_codes if not already present. 
        """
        if course_code not in self._assigned_course_codes:
            self._assigned_course_codes.append(course_code)

    def unassign_course(self, course_code: str) -> None:
        """
        Removes course_code from _assigned_course_codes. 
        """
        if course_code in self._assigned_course_codes:
            self._assigned_course_codes.remove(course_code)

    def display_details(self) -> str:
        """
        Overrides parent. Returns a string including inherited details plus department and number of assigned courses. 
        """
        return (f"{super().__str__()}, Department: {self._department}, "
                f"Assigned Courses: {len(self._assigned_course_codes)}")

    def to_dict(self) -> dict:
        """
        Overrides parent. Returns dictionary including _department, _assigned_course_codes, and type: 'faculty'. 
        """
        data = super().to_dict()
        data.update({
            "type": "faculty",  # 
            "department": self._department,  # 
            "assigned_course_codes": self._assigned_course_codes  # 
        })
        return data


class Course:
    """
    Represents a university course. 
    """
    def __init__(self, course_code: str, title: str, credits: int, prerequisites: list[str]) -> None:
        """
        Constructor. Initializes attributes. 
        _prerequisite_codes defaults to empty list. 
        _enrolled_student_ids starts empty. 
        _assigned_faculty_id starts as None. 
        """
        self._course_code = course_code  # 
        self._title = title  # 
        self._credits = credits  # 
        self._prerequisite_codes = prerequisites if prerequisites is not None else []  # 
        self._enrolled_student_ids = []  # 
        self._assigned_faculty_id = None  # 

    @property
    def course_code(self) -> str:
        """
        Returns _course_code. 
        """
        return self._course_code

    @property
    def title(self) -> str:
        """
        Returns _title. 
        """
        return self._title

    @property
    def credits(self) -> int:
        """
        Returns _credits. 
        """
        return self._credits

    @property
    def prerequisite_codes(self) -> list[str]:
        """
        Returns a copy of _prerequisite_codes. 
        """
        return self._prerequisite_codes.copy()

    @property
    def enrolled_student_ids(self) -> list[str]:
        """
        Returns a copy of _enrolled_student_ids. 
        """
        return self._enrolled_student_ids.copy()

    @property
    def assigned_faculty_id(self) -> None:
        """
        Returns/sets _assigned_faculty_id. 
        """
        return 

    @assigned_faculty_id.setter
    def assigned_faculty_id(self, faculty_id: str) -> None:
        self._assigned_faculty_id = faculty_id

    def add_prerequisite(self, prerequisite_code: str) -> None:
        """
        Adds prerequisite_code to _prerequisite_codes. 
        """
        if prerequisite_code not in self._prerequisite_codes:
            self._prerequisite_codes.append(prerequisite_code)

    def add_student_id(self, student_id: str) -> None:
        """
        Adds student_id to _enrolled_student_ids if not already present. 
        """
        if student_id not in self._enrolled_student_ids:
            self._enrolled_student_ids.append(student_id)

    def remove_student_id(self, student_id: str) -> None:
        """
        Removes student_id from _enrolled_student_ids. 
        """
        if student_id in self._enrolled_student_ids:
            self._enrolled_student_ids.remove(student_id)

    def assign_faculty_id(self, faculty_id: str) -> None:
        """
        Assigns faculty_id to the course. 
        """
        self._assigned_faculty_id = faculty_id

    def unassign_faculty_id(self) -> None:
        """
        Sets _assigned_faculty_id to None. 
        """
        self._assigned_faculty_id = None

    def display_details(self) -> str:
        """
        Returns a string including course details, prerequisites, number of enrolled students,
        and assigned faculty ID (if any). 
        """
        faculty_info = f", Assigned Faculty ID: {self._assigned_faculty_id}" if self._assigned_faculty_id else ""
        return (f"Course Code: {self._course_code}, Title: {self._title}, Credits: {self._credits}, "
                f"Prerequisites: {', '.join(self._prerequisite_codes) if self._prerequisite_codes else 'None'}, "
                f"Enrolled Students: {len(self._enrolled_student_ids)}{faculty_info}")

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the course's attributes, useful for saving to file. 
        """
        return {
            "course_code": self._course_code,  # 
            "title": self._title,  # 
            "credits": self._credits,  # 
            "prerequisite_codes": self._prerequisite_codes,  # 
            "enrolled_student_ids": self._enrolled_student_ids,  # 
            "assigned_faculty_id": self._assigned_faculty_id  # 
        }


class University:
    """
    The main orchestrator class, managing all Student, Faculty, and Course objects. 
    """
    def __init__(self, student_file='students.json', faculty_file='faculty.json', course_file='courses.json'):
        """
        Initializes empty dictionaries. Sets file names. 
        Calls _load_data() to load existing data from files. 
        """
        self._students: dict[str, Student] = {}  # 
        self._faculty: dict[str, Faculty] = {}  # 
        self._courses: dict[str, Course] = {}  # 
        self._student_file = student_file  # 
        self._faculty_file = faculty_file  # 
        self._course_file = course_file  # 
        self._load_data()  # 

    def _load_data(self) -> None:
        """
        Loads student, faculty, and course data from their respective files. 
        Handles FileNotFoundError. 
        Crucial for Relationships: After loading all entities, you must "re-link" them. 
        For example, iterate through loaded Student objects and verify their _enrolled_course_codes exist in _courses.
        Similarly for Faculty and Course assignments/prerequisites. 
        This ensures data consistency. 
        """
        # Load students
        try:
            with open(self._student_file, 'r') as f:
                students_data = json.load(f)
                for s_data in students_data:
                    student = Student(s_data['id'], s_data['name'], s_data['major'])
                    student._enrolled_course_codes = s_data['enrolled_course_codes']  # Direct assignment for loading
                    self._students[student.id] = student
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self._student_file}. Starting with empty student data.")

        # Load faculty
        try:
            with open(self._faculty_file, 'r') as f:
                faculty_data = json.load(f)
                for f_data in faculty_data:
                    faculty = Faculty(f_data['id'], f_data['name'], f_data['department'])
                    faculty._assigned_course_codes = f_data['assigned_course_codes']  # Direct assignment for loading
                    self._faculty[faculty.id] = faculty
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self._faculty_file}. Starting with empty faculty data.")

        # Load courses
        try:
            with open(self._course_file, 'r') as f:
                courses_data = json.load(f)
                for c_data in courses_data:
                    course = Course(c_data['course_code'], c_data['title'], c_data['credits'], c_data['prerequisite_codes'])
                    course._enrolled_student_ids = c_data['enrolled_student_ids']  # Direct assignment
                    course._assigned_faculty_id = c_data['assigned_faculty_id']  # Direct assignment
                    self._courses[course.course_code] = course
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self._course_file}. Starting with empty course data.")

        # Re-link relationships 
        # For students, verify enrolled courses exist
        for student_id, student in self._students.items():
            valid_courses = []
            for course_code in student._enrolled_course_codes:
                if course_code in self._courses:
                    valid_courses.append(course_code)
                else:
                    print(f"Warning: Course {course_code} not found for student {student_id}. Removing from enrollment.")
            student._enrolled_course_codes = valid_courses

        # For faculty, verify assigned courses exist
        for faculty_id, faculty in self._faculty.items():
            valid_courses = []
            for course_code in faculty._assigned_course_codes:
                if course_code in self._courses:
                    valid_courses.append(course_code)
                else:
                    print(f"Warning: Course {course_code} not found for faculty {faculty_id}. Removing from assignment.")
            faculty._assigned_course_codes = valid_courses

        # For courses, verify enrolled students and assigned faculty exist
        for course_code, course in self._courses.items():
            valid_students = []
            for student_id in course._enrolled_student_ids:
                if student_id in self._students:
                    valid_students.append(student_id)
                else:
                    print(f"Warning: Student {student_id} not found for course {course_code}. Removing from course enrollment.")
            course._enrolled_student_ids = valid_students

            if course._assigned_faculty_id and course._assigned_faculty_id not in self._faculty:
                print(f"Warning: Faculty {course._assigned_faculty_id} not found for course {course_code}. Unassigning faculty.")
                course._assigned_faculty_id = None

    def _save_data(self) -> None:
        """
        Saves current _students, _faculty, and _courses data to their respective JSON files. 
        Iterate through collections and call to_dict() on each object before saving. 
        """
        try:
            with open(self._student_file, 'w') as f:
                json.dump([s.to_dict() for s in self._students.values()], f, indent=4)
        except IOError as e:
            print(f"Error saving student data to {self._student_file}: {e}")

        try:
            with open(self._faculty_file, 'w') as f:
                json.dump([f.to_dict() for f in self._faculty.values()], f, indent=4)
        except IOError as e:
            print(f"Error saving faculty data to {self._faculty_file}: {e}")

        try:
            with open(self._course_file, 'w') as f:
                json.dump([c.to_dict() for c in self._courses.values()], f, indent=4)
        except IOError as e:
            print(f"Error saving course data to {self._course_file}: {e}")

    def add_student(self, student: Student) -> bool:
        """
        Adds a Student object. Returns True if added, False if ID exists. Calls _save_data(). 
        """
        if student.id in self._students:
            print(f"Student with ID {student.id} already exists.")
            return False
        self._students[student.id] = student
        self._save_data()  # 
        print(f"Student {student.name} added successfully.")
        return True

    def remove_student(self, student_id: str) -> bool:
        """
        Removes a student. Returns True if removed, False if not found or if student is enrolled in courses.
        Calls _save_data(). 
        """
        if student_id not in self._students:
            print(f"Student with ID {student_id} not found.")
            return False

        student = self._students[student_id]
        if student.enrolled_course_codes:
            print(f"Student {student.name} is enrolled in courses. Drop them from all courses first.")
            return False

        del self._students[student_id]
        self._save_data()  # 
        print(f"Student {student.name} removed successfully.")
        return True

    def add_faculty(self, faculty: Faculty) -> bool:
        """
        Adds a Faculty object. Returns True if added, False if ID exists. Calls _save_data(). 
        """
        if faculty.id in self._faculty:
            print(f"Faculty with ID {faculty.id} already exists.")
            return False
        self._faculty[faculty.id] = faculty
        self._save_data()  # 
        print(f"Faculty {faculty.name} added successfully.")
        return True

    def remove_faculty(self, faculty_id: str) -> bool:
        """
        Removes faculty. Returns True if removed, False if not found or if faculty is assigned to courses.
        Calls _save_data(). 
        """
        if faculty_id not in self._faculty:
            print(f"Faculty with ID {faculty_id} not found.")
            return False

        faculty = self._faculty[faculty_id]
        if faculty.assigned_course_codes:
            print(f"Faculty {faculty.name} is assigned to courses. Unassign them from all courses first.")
            return False

        del self._faculty[faculty_id]
        self._save_data()  # 
        print(f"Faculty {faculty.name} removed successfully.")
        return True

    def add_course(self, course: Course) -> bool:
        """
        Adds a Course object. Returns True if added, False if code exists. Calls _save_data(). 
        """
        if course.course_code in self._courses:
            print(f"Course with code {course.course_code} already exists.")
            return False
        self._courses[course.course_code] = course
        self._save_data()  # 
        print(f"Course {course.title} added successfully.")
        return True

    def remove_course(self, course_code: str) -> bool:
        """
        Removes a course. Returns True if removed, False if not found or if students are enrolled.
        Calls _save_data(). 
        """
        if course_code not in self._courses:
            print(f"Course with code {course_code} not found.")
            return False

        course = self._courses[course_code]
        if course.enrolled_student_ids:
            print(f"Course {course.title} has enrolled students. Drop all students from this course first.")
            return False
        if course.assigned_faculty_id:
            print(f"Course {course.title} has an assigned faculty. Unassign faculty first.")
            return False

        del self._courses[course_code]
        self._save_data()  # 
        print(f"Course {course.title} removed successfully.")
        return True

    def enroll_student_in_course(self, student_id: str, course_code: str) -> bool:
        """
        Checks if student and course exist and prerequisites are met. 
        Updates both Student and Course objects' respective lists. Returns True on success, False otherwise.
        Calls _save_data(). 
        """
        student = self._students.get(student_id)
        course = self._courses.get(course_code)

        if not student:
            print(f"Student with ID {student_id} not found.")
            return False
        if not course:
            print(f"Course with code {course_code} not found.")
            return False
        if course_code in student.enrolled_course_codes:
            print(f"Student {student.name} is already enrolled in {course.title}.")
            return False

        # Check prerequisites
        for prereq_code in course.prerequisite_codes:
            if prereq_code not in student.enrolled_course_codes:
                print(f"Student {student.name} has not met prerequisite: {prereq_code}.")
                return False

        student.enroll_course(course_code)
        course.add_student_id(student_id)
        self._save_data()  # 
        print(f"Student {student.name} enrolled in {course.title} successfully.")
        return True

    def drop_student_from_course(self, student_id: str, course_code: str) -> bool:
        """
        Checks if student and course exist and student is enrolled. 
        Updates both Student and Course objects. Returns True on success, False otherwise.
        Calls _save_data(). 
        """
        student = self._students.get(student_id)
        course = self._courses.get(course_code)

        if not student:
            print(f"Student with ID {student_id} not found.")
            return False
        if not course:
            print(f"Course with code {course_code} not found.")
            return False
        if course_code not in student.enrolled_course_codes:
            print(f"Student {student.name} is not enrolled in {course.title}.")
            return False

        student.drop_course(course_code)
        course.remove_student_id(student_id)
        self._save_data()  # 
        print(f"Student {student.name} dropped from {course.title} successfully.")
        return True

    def assign_faculty_to_course(self, faculty_id: str, course_code: str) -> bool:
        """
        Checks if faculty and course exist. 
        Updates both Faculty and Course objects. Returns True on success, False otherwise.
        Calls _save_data(). 
        """
        faculty = self._faculty.get(faculty_id)
        course = self._courses.get(course_code)

        if not faculty:
            print(f"Faculty with ID {faculty_id} not found.")
            return False
        if not course:
            print(f"Course with code {course_code} not found.")
            return False
        if course.assigned_faculty_id == faculty_id:
            print(f"Faculty {faculty.name} is already assigned to {course.title}.")
            return False
        if course.assigned_faculty_id is not None:
            print(f"Course {course.title} already has faculty {self._faculty[course.assigned_faculty_id].name} assigned. Unassign them first.")
            return False

        faculty.assign_course(course_code)
        course.assign_faculty_id(faculty_id)
        self._save_data()  # 
        print(f"Faculty {faculty.name} assigned to {course.title} successfully.")
        return True

    def unassign_faculty_from_course(self, faculty_id: str, course_code: str) -> bool:
        """
        Checks if faculty and course exist and are assigned. 
        Updates both Faculty and Course objects. Returns True on success, False otherwise.
        Calls _save_data(). 
        """
        faculty = self._faculty.get(faculty_id)
        course = self._courses.get(course_code)

        if not faculty:
            print(f"Faculty with ID {faculty_id} not found.")
            return False
        if not course:
            print(f"Course with code {course_code} not found.")
            return False
        if course.assigned_faculty_id != faculty_id:
            print(f"Faculty {faculty.name} is not assigned to {course.title}.")
            return False

        faculty.unassign_course(course_code)
        course.unassign_faculty_id()
        self._save_data()  # 
        print(f"Faculty {faculty.name} unassigned from {course.title} successfully.")
        return True

    def get_course_roster(self, course_code: str) -> list[Student]:
        """
        Returns a list of Student objects enrolled in the specified course. 
        Handles course not found. 
        """
        course = self._courses.get(course_code)
        if not course:
            print(f"Course with code {course_code} not found.")
            return []

        roster = []
        for student_id in course.enrolled_student_ids:
            student = self._students.get(student_id)
            if student:
                roster.append(student)
        return roster

    def display_all_students(self) -> None:
        """
        Prints details of all registered students. 
        """
        if not self._students:
            print("\nNo students registered.")
            return
        print("\n--- All Students ---")
        for student in self._students.values():
            print(student.display_details())

    def display_all_faculty(self) -> None:
        """
        Prints details of all registered faculty. 
        """
        if not self._faculty:
            print("\nNo faculty registered.")
            return
        print("\n--- All Faculty ---")
        for faculty in self._faculty.values():
            print(faculty.display_details())

    def display_all_courses(self) -> None:
        """
        Prints details of all registered courses. 
        """
        if not self._courses:
            print("\nNo courses registered.")
            return
        print("\n--- All Courses ---")
        for course in self._courses.values():
            print(course.display_details())

    def run(self):
        """
        Develops a main() function or a run() method in the University class. 
        Implements a main while loop that presents a menu to the administrator. 
        Uses input() to get administrator choices and data. 
        Calls the appropriate University methods based on input. 
        Includes clear print() statements for feedback and displaying results. 
        """
        while True:
            print("\nUniversity Management System Menu:")
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

            choice = input("Enter your choice: ")

            if choice == '1':
                s_id = input("Enter student ID: ")
                s_name = input("Enter student name: ")
                s_major = input("Enter student major: ")
                student = Student(s_id, s_name, s_major)
                self.add_student(student)
            elif choice == '2':
                s_id = input("Enter student ID to remove: ")
                self.remove_student(s_id)
            elif choice == '3':
                f_id = input("Enter faculty ID: ")
                f_name = input("Enter faculty name: ")
                f_dept = input("Enter faculty department: ")
                faculty = Faculty(f_id, f_name, f_dept)
                self.add_faculty(faculty)
            elif choice == '4':
                f_id = input("Enter faculty ID to remove: ")
                self.remove_faculty(f_id)
            elif choice == '5':
                c_code = input("Enter course code: ")
                c_title = input("Enter course title: ")
                try:
                    c_credits = int(input("Enter course credits: "))
                except ValueError:
                    print("Invalid credits. Please enter a number.")
                    continue
                prerequisites_str = input("Enter prerequisite course codes (comma-separated, leave empty if none): ")
                c_prerequisites = [p.strip() for p in prerequisites_str.split(',') if p.strip()]
                course = Course(c_code, c_title, c_credits, c_prerequisites)
                self.add_course(course)
            elif choice == '6':
                c_code = input("Enter course code to remove: ")
                self.remove_course(c_code)
            elif choice == '7':
                s_id = input("Enter student ID: ")
                c_code = input("Enter course code to enroll in: ")
                self.enroll_student_in_course(s_id, c_code)
            elif choice == '8':
                s_id = input("Enter student ID: ")
                c_code = input("Enter course code to drop from: ")
                self.drop_student_from_course(s_id, c_code)
            elif choice == '9':
                f_id = input("Enter faculty ID: ")
                c_code = input("Enter course code to assign to: ")
                self.assign_faculty_to_course(f_id, c_code)
            elif choice == '10':
                f_id = input("Enter faculty ID: ")
                c_code = input("Enter course code to unassign from: ")
                self.unassign_faculty_from_course(f_id, c_code)
            elif choice == '11':
                c_code = input("Enter course code to view roster: ")
                roster = self.get_course_roster(c_code)
                if roster:
                    print(f"\n--- Roster for {c_code} ---")
                    for student in roster:
                        print(student.display_details())
                else:
                    print(f"No students enrolled in {c_code} or course not found.")
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
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Clean up previous data files for a fresh start (optional, for testing)
    # for f in ['students.json', 'faculty.json', 'courses.json']:
    #     if os.path.exists(f):
    #         os.remove(f)

    university = University()
    university.run()