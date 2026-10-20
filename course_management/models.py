from abc import ABC, abstractmethod
from datetime import datetime, timezone
import re
from .exceptions import EnrollmentError, ValidationError


class User(ABC):
    def __init__(self, user_id, name, email):
        self._user_id = self._required(user_id, "user_id")
        self._name = self._required(name, "name")
        if not self.is_valid_email(email):
            raise ValidationError(f"Invalid email: {email!r}")
        self._email = email.strip().lower()

    @staticmethod
    def is_valid_email(email):
        return isinstance(email, str) and bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()))

    @staticmethod
    def _required(value, field):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"{field} must be non-empty")
        return value.strip()

    @property
    def user_id(self): return self._user_id
    @property
    def name(self): return self._name
    @property
    def email(self): return self._email

    @abstractmethod
    def role_description(self): ...

    def to_dict(self):
        return {"user_id": self.user_id, "name": self.name, "email": self.email}


class Student(User):
    def __init__(self, user_id, name, email, program="General"):
        super().__init__(user_id, name, email)
        self._program = self._required(program, "program")

    @property
    def program(self): return self._program
    def role_description(self): return f"Student: {self.name} ({self.program})"

    @classmethod
    def from_dict(cls, data):
        return cls(data["user_id"], data["name"], data["email"], data.get("program", "General"))

    def to_dict(self):
        return {**super().to_dict(), "program": self.program}


class Mentor(User):
    def __init__(self, user_id, name, email, expertise):
        super().__init__(user_id, name, email)
        self._expertise = self._required(expertise, "expertise")

    @property
    def expertise(self): return self._expertise
    def role_description(self): return f"Mentor: {self.name} ({self.expertise})"

    @classmethod
    def from_dict(cls, data):
        return cls(data["user_id"], data["name"], data["email"], data["expertise"])

    def to_dict(self):
        return {**super().to_dict(), "expertise": self.expertise}


class Course:
    def __init__(self, course_id, title, description, capacity=30, mentor_id=None, enrolled_student_ids=None):
        self._course_id = User._required(course_id, "course_id")
        self._title = User._required(title, "title")
        self._description = User._required(description, "description")
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise ValidationError("capacity must be a positive integer")
        self._capacity = capacity
        self._mentor_id = mentor_id
        self._enrolled_student_ids = set(enrolled_student_ids or [])

    @property
    def course_id(self): return self._course_id
    @property
    def title(self): return self._title
    @property
    def description(self): return self._description
    @property
    def capacity(self): return self._capacity
    @property
    def mentor_id(self): return self._mentor_id
    @property
    def enrolled_student_ids(self): return tuple(sorted(self._enrolled_student_ids))
    @property
    def seats_available(self): return self.capacity - len(self._enrolled_student_ids)

    def assign_mentor(self, mentor):
        if not isinstance(mentor, Mentor):
            raise ValidationError("A course can only be assigned to a Mentor")
        self._mentor_id = mentor.user_id

    def add_student(self, student):
        if not isinstance(student, Student):
            raise ValidationError("Only a Student can enroll")
        if student.user_id in self._enrolled_student_ids:
            raise EnrollmentError("Student is already enrolled")
        if self.seats_available <= 0:
            raise EnrollmentError("Course is full")
        self._enrolled_student_ids.add(student.user_id)

    def to_dict(self):
        return {"course_id": self.course_id, "title": self.title, "description": self.description,
                "capacity": self.capacity, "mentor_id": self.mentor_id,
                "enrolled_student_ids": list(self.enrolled_student_ids)}

    @classmethod
    def from_dict(cls, data):
        return cls(data["course_id"], data["title"], data["description"], data.get("capacity", 30),
                   data.get("mentor_id"), data.get("enrolled_student_ids", []))


class Enrollment:
    STATUSES = {"active", "completed", "cancelled"}

    def __init__(self, enrollment_id, student_id, course_id, status="active", enrolled_at=None):
        self._enrollment_id = User._required(enrollment_id, "enrollment_id")
        self._student_id = User._required(student_id, "student_id")
        self._course_id = User._required(course_id, "course_id")
        if status not in self.STATUSES:
            raise ValidationError(f"Unsupported status: {status}")
        self._status = status
        self._enrolled_at = enrolled_at or datetime.now(timezone.utc).isoformat()

    @property
    def enrollment_id(self): return self._enrollment_id
    @property
    def student_id(self): return self._student_id
    @property
    def course_id(self): return self._course_id
    @property
    def status(self): return self._status
    @property
    def enrolled_at(self): return self._enrolled_at

    def complete(self):
        if self._status != "active":
            raise EnrollmentError("Only active enrollments can be completed")
        self._status = "completed"

    def cancel(self):
        if self._status != "active":
            raise EnrollmentError("Only active enrollments can be cancelled")
        self._status = "cancelled"

    @classmethod
    def create(cls, student, course, enrollment_id=None):
        course.add_student(student)
        return cls(enrollment_id or f"ENR-{student.user_id}-{course.course_id}", student.user_id, course.course_id)

    @classmethod
    def from_dict(cls, data):
        return cls(data["enrollment_id"], data["student_id"], data["course_id"],
                   data.get("status", "active"), data.get("enrolled_at"))

    def to_dict(self):
        return {"enrollment_id": self.enrollment_id, "student_id": self.student_id,
                "course_id": self.course_id, "status": self.status, "enrolled_at": self.enrolled_at}
