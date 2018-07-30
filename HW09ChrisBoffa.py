from StudentClasses import Student, Instructor
from prettytable import PrettyTable

students = {}
instructors = {}
courses = {}


def read_large_file(file_object):
    """
    Uses a generator to read a large file lazily
    """
    while True:
        data = file_object.readline().strip()
        if not data:
            break
        yield data.strip().split('\t')


def process_students(path):
    """Processes student from students.txt"""
    try:
        with open(path) as file_handler:
            for line in read_large_file(file_handler):
                students[line[0]] = Student(line[0], line[1])
        return students
    except (IOError, OSError):
        print("Error opening or processing file: {0}".format(path))
        exit()


def process_instructors(path):
    """Processes instructors from instructors.txt"""
    try:
        with open(path) as file_handler:
            for line in read_large_file(file_handler):
                instructors[line[0]] = Instructor(line[0], line[1], line[2])
        return instructors
    except (IOError, OSError):
        print("Error opening or processing file: {0}".format(path))
        exit()


def process_grades(path):
    """ Assign grades to each course and process grades.txt """
    try:
        with open(path) as file_handler:
            for line in read_large_file(file_handler):
                if students.get(line[0]):
                    student = students.get(line[0])  # type: Student
                    student.completed_courses.append(line[1])
                if instructors.get(line[3]):
                    instructor = instructors.get(line[3])
                    instructor.course.append(line[1])
                    instructor.students += 1
    except (IOError, OSError):
        print("Error opening or processing file: {0}".format(path))
        exit()


def convert_instructor_to_courses():
    """ Utility function to convert instructor list to a new list identified by courses"""
    for key, instructor in instructors.items():
        for course in set(instructor.course):
            courses[course] = [instructor.cwid, instructor.name, instructor.department, course,
                               instructor.course.count(course)]


def read_and_process_school(folder):
    """ Read and process files by school folder """
    process_students('{0}/students.txt'.format(folder))
    process_instructors('{0}/instructors.txt'.format(folder))
    process_grades('{0}/grades.txt'.format(folder))
    print_student_summary()
    print_instructor_summary()


def print_student_summary():
    """ Print student summary table"""
    table = PrettyTable(['CWID', 'Name', 'Completed Courses'])
    for key, student in students.items():
        table.add_row([key, student.name, sorted(student.completed_courses)])
    print('Student Summary')
    print(table)


def print_instructor_summary():
    """Print instructor summary table"""
    convert_instructor_to_courses()
    table = PrettyTable(['CWID', 'Name', 'Dept', 'Course', 'Students'])
    for key, course in courses.items():
        table.add_row([course[0], course[1], course[2], course[3], course[4]])
    print('Instructor Summary')
    print(table)


if __name__ == '__main__':
    read_and_process_school('stevens')
