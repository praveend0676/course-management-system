from .exceptions import ValidationError, NotFoundError, EnrollmentError
from .models import Student, Mentor, Course, Enrollment
from .storage import JsonStorage


class CourseManagementService:
    def __init__(self, storage=None):
        self.storage = storage or JsonStorage()
        self.students, self.mentors, self.courses, self.enrollments = {}, {}, {}, {}
        self.load()

    @staticmethod
    def _unique(key, collection, label):
        if key in collection:
            raise ValidationError(f"{label} ID {key!r} already exists")

    @staticmethod
    def _get(collection, key, label):
        try: return collection[key]
        except KeyError as exc: raise NotFoundError(f"{label} {key!r} not found") from exc

    def add_student(self, student):
        self._unique(student.user_id, self.students, "Student")
        if student.user_id in self.mentors: raise ValidationError("User ID already exists")
        self.students[student.user_id] = student

    def add_mentor(self, mentor):
        self._unique(mentor.user_id, self.mentors, "Mentor")
        if mentor.user_id in self.students: raise ValidationError("User ID already exists")
        self.mentors[mentor.user_id] = mentor

    def add_course(self, course):
        self._unique(course.course_id, self.courses, "Course")
        self.courses[course.course_id] = course

    def assign_mentor(self, course_id, mentor_id):
        self._get(self.courses, course_id, "Course").assign_mentor(self._get(self.mentors, mentor_id, "Mentor"))

    def enroll_student(self, student_id, course_id):
        student = self._get(self.students, student_id, "Student")
        course = self._get(self.courses, course_id, "Course")
        if student_id in course.enrolled_student_ids:
            raise EnrollmentError("Student is already enrolled")
        if course.seats_available <= 0:
            raise EnrollmentError("Course is full")
        eid = f"ENR-{student_id}-{course_id}"
        self._unique(eid, self.enrollments, "Enrollment")
        enrollment = Enrollment.create(student, course, eid)
        self.enrollments[eid] = enrollment
        return enrollment

    def complete_enrollment(self, enrollment_id):
        self._get(self.enrollments, enrollment_id, "Enrollment").complete()

    def save(self):
        self.storage.save({
            "students": [{**s.to_dict(), "type": "Student"} for s in self.students.values()],
            "mentors": [{**m.to_dict(), "type": "Mentor"} for m in self.mentors.values()],
            "courses": [c.to_dict() for c in self.courses.values()],
            "enrollments": [e.to_dict() for e in self.enrollments.values()],
        })

    def load(self):
        data = self.storage.load()
        self.students = {x.user_id: x for x in (Student.from_dict(d) for d in data["students"])}
        self.mentors = {x.user_id: x for x in (Mentor.from_dict(d) for d in data["mentors"])}
        self.courses = {x.course_id: x for x in (Course.from_dict(d) for d in data["courses"])}
        self.enrollments = {x.enrollment_id: x for x in (Enrollment.from_dict(d) for d in data["enrollments"])}
