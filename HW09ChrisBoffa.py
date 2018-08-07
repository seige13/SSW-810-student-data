from StudentClasses import Student, Instructor, Major
from prettytable import PrettyTable
import sqlite3

DB_FILE = './810_startup.db'

db = sqlite3.connect(DB_FILE)


class CollegeAdministration(object):
    passing_grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']

    def __init__(self, administration_name):
        self.folder = administration_name
        self.administration = administration_name.title()
        self.students = {}
        self.majors = {}
        self.instructors = {}
        self.grades = {}
        self.courses = {}
        self.read_and_process_school()

    def read_large_file(self, file_object):
        """
        Uses a generator to read a large file lazily
        """
        while True:
            data = file_object.readline().strip()
            if not data:
                break
            yield data.strip().split('\t')

    def process_students(self, path):
        """Processes student from students.txt"""
        try:
            with open(path) as file_handler:
                next(file_handler)
                for line in self.read_large_file(file_handler):
                    self.students[line[0]] = Student(line[0], line[1], line[2])
            return self.students
        except (IOError, OSError):
            print("Error opening or processing file: {0}".format(path))
            exit()

    def process_majors(self, path):
        """Processes student from majors.txt"""
        try:
            with open(path) as file_handler:
                next(file_handler)
                for line in self.read_large_file(file_handler):
                    if not self.majors.get(line[0]):
                        self.majors[line[0]] = Major(line[0])

                    if line[1].upper() == 'R':
                        self.majors[line[0]].required.append(line[2])
                    else:
                        self.majors[line[0]].electives.append(line[1])

            return self.majors
        except (IOError, OSError):
            print("Error opening or processing file: {0}".format(path))
            exit()

    def process_instructors(self, path):
        """Processes instructors from instructors.txt"""
        try:
            with open(path) as file_handler:
                next(file_handler)
                for line in self.read_large_file(file_handler):
                    self.instructors[line[0]] = Instructor(line[0], line[1], line[2])
            return self.instructors
        except (IOError, OSError):
            print("Error opening or processing file: {0}".format(path))
            exit()

    def process_grades(self, path):
        """ Assign grades to each course and process grades.txt """
        try:
            with open(path) as file_handler:
                next(file_handler)
                for line in self.read_large_file(file_handler):
                    if self.students.get(line[0]):
                        student = self.students.get(line[0])  # type: Student
                        if line[2] in self.passing_grades:
                            student.completed_courses.append(line[1])
                    if self.instructors.get(line[3]):
                        instructor = self.instructors.get(line[3])
                        instructor.course.append(line[1])
                        instructor.students += 1
        except (IOError, OSError):
            print("Error opening or processing file: {0}".format(path))
            exit()

    def convert_instructor_to_courses(self):
        """ Utility function to convert instructor list to a new list identified by courses"""
        for key, instructor in self.instructors.items():
            for course in set(instructor.course):
                self.courses[course] = [instructor.cwid, instructor.name, instructor.department, course,
                                        instructor.course.count(course)]

    def assign_classes(self):
        for key, student in self.students.items():
            if self.majors.get(student.major):
                major = self.majors.get(student.major)  # type: Major
                student.remaining_required = set(major.required) - set(student.completed_courses)
                if not set(student.completed_courses).intersection(major.electives):
                    student.remaining_electives = set(major.electives) - set(student.completed_courses)
                else:
                    student.remaining_electives = None

    def read_and_process_school(self):
        """ Read and process files by school self.path """
        self.process_students('{0}/students.txt'.format(self.folder))
        self.process_instructors('{0}/instructors.txt'.format(self.folder))
        self.process_grades('{0}/grades.txt'.format(self.folder))
        self.process_majors('{0}/majors.txt'.format(self.folder))
        self.assign_classes()

    def print_student_summary(self):
        """ Print student summary table"""
        table = PrettyTable(['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for key, student in self.students.items():
            table.add_row(
                [key, student.name, student.major, sorted(student.completed_courses), student.remaining_required,
                 student.remaining_electives])
        print('Student Summary')
        print(table)

    def print_major_summary(self):
        """ Print major summary table"""
        table = PrettyTable(['Dept', 'Required', 'Electives'])
        for key, major in self.majors.items():
            table.add_row([key, sorted(major.required), sorted(major.electives)])
        print('Majors Summary')
        print(table)

    def print_instructor_summary(self, database):
        """Print instructor summary table"""
        cur = database.cursor()

        cur.execute(
            "select instructors.cwid, instructors.name, instructors.dept, grades.course, count(grades.student_cwid) as `students` from instructors inner join grades on instructors.cwid=grades.instructor_cwid group by grades.course order by instructors.cwid;")
        rows = cur.fetchall()

        # convert_instructor_to_courses()
        table = PrettyTable(['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for course in rows:
            table.add_row([course[0], course[1], course[2], course[3], course[4]])
        print('Instructor Summary')
        print(table)


if __name__ == '__main__':
    stevens = CollegeAdministration('stevens')
    # print_major_summary()
    # print_student_summary()
    stevens.print_instructor_summary(db)
