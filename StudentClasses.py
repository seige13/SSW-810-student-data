class Student(object):
    def __init__(self, cwid, name):
        self.cwid = cwid
        self.name = name
        self.completed_courses = []
        self.major = ''


class Repository(object):
    def __init__(self, cwid, course, instructor):
        self.cwid = cwid
        self.course = course
        self.instructor = instructor


class Instructor(object):
    def __init__(self, cwid, name, department):
        self.name = name
        self.cwid = cwid
        self.department = department
        self.course = []
        self.students = 0
