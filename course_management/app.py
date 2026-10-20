from .exceptions import CourseManagementError
from .models import Student, Mentor, Course
from .service import CourseManagementService


def ask(label):
    return input(label).strip()


def run():
    app = CourseManagementService()
    while True:
        print("\n=== Course Management System ===")
        print("1 Add student | 2 Add mentor | 3 Create course | 4 Assign mentor")
        print("5 Enroll student | 6 List records | 7 Complete enrollment | 8 Save and exit")
        try:
            choice = ask("Choose: ")
            if choice == "1":
                obj = Student(ask("Student ID: "), ask("Name: "), ask("Email: "), ask("Program [General]: ") or "General")
                app.add_student(obj); print(obj.role_description())
            elif choice == "2":
                obj = Mentor(ask("Mentor ID: "), ask("Name: "), ask("Email: "), ask("Expertise: "))
                app.add_mentor(obj); print(obj.role_description())
            elif choice == "3":
                obj = Course(ask("Course ID: "), ask("Title: "), ask("Description: "), int(ask("Capacity [30]: ") or "30"))
                app.add_course(obj); print(f"Created {obj.course_id}: {obj.title}")
            elif choice == "4":
                app.assign_mentor(ask("Course ID: "), ask("Mentor ID: ")); print("Mentor assigned.")
            elif choice == "5":
                e = app.enroll_student(ask("Student ID: "), ask("Course ID: "))
                print(f"Created {e.enrollment_id}: {e.status}")
            elif choice == "6":
                print("\nStudents:")
                for x in app.students.values(): print(f"  {x.user_id}: {x.role_description()} | {x.email}")
                print("\nMentors:")
                for x in app.mentors.values(): print(f"  {x.user_id}: {x.role_description()} | {x.email}")
                print("\nCourses:")
                for x in app.courses.values(): print(f"  {x.course_id}: {x.title} | seats {x.seats_available}/{x.capacity} | mentor {x.mentor_id or 'unassigned'}")
                print("\nEnrollments:")
                for x in app.enrollments.values(): print(f"  {x.enrollment_id}: {x.student_id} -> {x.course_id} [{x.status}]")
            elif choice == "7":
                app.complete_enrollment(ask("Enrollment ID: ")); print("Enrollment completed.")
            elif choice == "8":
                app.save(); print("Saved. Goodbye."); return
            else: print("Choose an option from 1 to 8.")
        except (CourseManagementError, ValueError) as exc:
            print(f"Error: {exc}")
        except (EOFError, KeyboardInterrupt):
            app.save(); print("\nSaved. Goodbye."); return


if __name__ == "__main__":
    run()
