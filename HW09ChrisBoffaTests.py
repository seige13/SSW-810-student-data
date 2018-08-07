import unittest
from HW09ChrisBoffa import CollegeAdministration


class FileMethods(unittest.TestCase):
    school = 'stevens'
    college = CollegeAdministration(school)

    def test_process_students(self):
        filepath = '{0}/students.txt'.format(self.school)
        students = self.college.process_students(filepath)
        self.assertEqual(len(students), 10)
        self.assertEqual(students.get('10103').name, 'Baldwin, C')
        self.assertEqual(students.get('10172').cwid, '10172')

    def test_process_instructors(self):
        filepath = '{0}/instructors.txt'.format(self.school)
        instructors = self.college.process_instructors(filepath)
        self.assertEqual(len(instructors), 6)
        self.assertEqual(instructors.get('98765').name, 'Einstein, A')
        self.assertEqual(instructors.get('98761').cwid, '98761')


if __name__ == '__main__':
    unittest.main()
