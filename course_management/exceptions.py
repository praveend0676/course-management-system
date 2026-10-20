class CourseManagementError(Exception):
    """Base application error."""


class ValidationError(CourseManagementError):
    """Invalid domain data or operation."""


class NotFoundError(CourseManagementError):
    """Requested entity does not exist."""


class EnrollmentError(CourseManagementError):
    """Enrollment operation is not permitted."""
