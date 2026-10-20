# Course Management System (Python OOP)

A CLI application for managing students, mentors, courses, and enrollments. It demonstrates abstraction, inheritance, encapsulation, polymorphism, instance methods, `@staticmethod`, and `@classmethod`. Data is persisted locally in JSON.

## Architecture
- `models.py`: abstract `User`, concrete `Student` and `Mentor`, plus `Course` and `Enrollment`.
- `service.py`: business rules, registration, course creation, enrollment, and persistence coordination.
- `storage.py`: JSON file persistence.
- `app.py`: interactive command-line menu.
- `tests/`: automated unit tests.

## OOP concepts
- **Abstraction:** `User` is an abstract base class.
- **Inheritance:** `Student` and `Mentor` inherit from `User`.
- **Encapsulation:** state is stored in underscored attributes and exposed through properties/methods.
- **Polymorphism:** each user type implements `role_description()` differently.
- **Instance methods:** course enrollment and enrollment completion methods.
- **`@staticmethod`:** `User.is_valid_email()` validates an email without object state.
- **`@classmethod`:** `from_dict()` methods reconstruct objects from serialized data.

## Requirements
Python 3.10+; no third-party runtime dependencies.

## Install and run
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m course_management.app
```

Use the menu to add students and mentors, create courses, assign mentors, enroll students, list data, complete enrollments, and save/exit. Data is stored in `data/course_data.json`.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Git collaboration workflow
1. Developer A initializes `main`, commits the initial project, creates a public GitHub repository, adds `origin`, and pushes `main`.
2. Developer B clones the repo and creates a feature branch:
   ```bash
   git clone https://github.com/<username>/course-management-system.git
   cd course-management-system
   git switch -c feature/course-enrollment
   ```
3. Implement and commit a feature:
   ```bash
   git add .
   git commit -m "feat: validate course enrollment"
   git push -u origin feature/course-enrollment
   ```
4. Open a Pull Request from `feature/course-enrollment` to `main`; review the diff, run tests, provide feedback, and merge after approval.
5. For an individual assignment, use two branches to simulate the two developers. Submit the public repository URL and the PR URL.

Suggested commits:
- `chore: initialize course management project`
- `feat: add user and course domain models`
- `feat: add JSON persistence`
- `feat: implement course enrollment validation`
- `test: cover course and enrollment rules`

## YouTube video plan (6–9 minutes)
1. Problem statement and goals.
2. Architecture and class responsibilities.
3. Explain abstraction, inheritance, encapsulation, polymorphism, instance/static/class methods.
4. Demonstrate branch creation, meaningful commits, push, Pull Request, code review, and merge.
5. Run the application: add a student, mentor, course, enroll, and list records.
6. Run tests and show output; finish by showing repository and PR URLs.

## Production-readiness note
This is a learning project, not a deployed multi-user service. A real production deployment should add authentication/authorization, a transactional database, audit logs, migrations, concurrency controls, backups, CI, and deployment configuration.
