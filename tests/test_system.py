import tempfile
import unittest
from pathlib import Path
from course_management.exceptions import EnrollmentError, NotFoundError, ValidationError
from course_management.models import User, Student, Mentor, Course
from course_management.service import CourseManagementService
from course_management.storage import JsonStorage


class CourseSystemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.service = CourseManagementService(JsonStorage(Path(self.tmp.name) / "state.json"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_user_is_abstract(self):
        with self.assertRaises(TypeError): User("U1", "User", "u@example.com")

    def test_static_method_and_polymorphism(self):
        self.assertTrue(User.is_valid_email("a@example.com"))
        self.assertFalse(User.is_valid_email("bad-email"))
        self.assertTrue(Student("S1", "Asha", "a@example.com").role_description().startswith("Student:"))
        self.assertTrue(Mentor("M1", "Ravi", "r@example.com", "Python").role_description().startswith("Mentor:"))

    def test_enrollment_capacity_and_duplicate(self):
        self.service.add_student(Student("S1", "Asha", "a@example.com"))
        self.service.add_student(Student("S2", "Bala", "b@example.com"))
        self.service.add_course(Course("C1", "Python", "OOP course", capacity=1))
        self.service.enroll_student("S1", "C1")
        with self.assertRaises(EnrollmentError): self.service.enroll_student("S1", "C1")
        with self.assertRaises(EnrollmentError): self.service.enroll_student("S2", "C1")
        with self.assertRaises(NotFoundError): self.service.enroll_student("S3", "C2")
        with self.assertRaises(NotFoundError): self.service.enroll_student("S4", "C2")

    def test_json_round_trip(self):
        self.service.add_student(Student("S1", "Asha", "a@example.com"))
        self.service.add_course(Course("C1", "Python", "OOP course"))
        self.service.enroll_student("S1", "C1")
        self.service.save()
        restored = CourseManagementService(self.service.storage)
        self.assertIn("S1", restored.students)
        self.assertIn("C1", restored.courses)
        self.assertEqual(len(restored.enrollments), 1)

    def test_invalid_email(self):
        with self.assertRaises(ValidationError): Student("S1", "Asha", "invalid")


if __name__ == "__main__": unittest.main()
