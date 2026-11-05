"""Student academic grading management module."""

import hashlib
import os
import secrets

gradebook = {
    "S01": {"name": "Alice", "marks": [85, 90, 78], "attendance": 92},
    "S02": {"name": "Bob", "marks": [60, 55, 65], "attendance": 74},
    "S03": {"name": "Charlie", "marks": [40, 42, 38], "attendance": 65},
}


def average_mark(student_id):
    """Return a student's average mark, or None if there is none."""
    student = gradebook.get(student_id)
    if student is None or not student["marks"]:
        return None
    return sum(student["marks"]) / len(student["marks"])


def add_grade(student_id, mark, grade_list=None):
    """Record a mark for a student and return whether it was accepted."""
    if grade_list is None:
        grade_list = []
    if student_id not in gradebook or not 0 <= mark <= 100:
        return False
    gradebook[student_id]["marks"].append(mark)
    grade_list.append(f"Recorded score {mark} for student id {student_id}")
    return True


def record_attendance(student_id, present_days):
    """Add attendance for a student and return whether it was recorded."""
    if student_id not in gradebook or present_days < 0:
        return False
    gradebook[student_id]["attendance"] += present_days
    return True


def check_passing_status(student_id, pass_threshold=50.0):
    """Return whether a student's average, plus grace marks, passes."""
    grace_marks = 5.0
    avg = average_mark(student_id)
    if avg is None:
        return False
    return avg + grace_marks >= pass_threshold


def compute_weighted_gpa(student_id, scale_divisor=20.0):
    """Return average mark / scale_divisor, or None without marks."""
    avg_score = average_mark(student_id)
    if avg_score is None:
        return None
    return avg_score / scale_divisor


def generate_student_hash(student_id):
    """Return the SHA-256 hex digest of a student id."""
    return hashlib.sha256(student_id.encode()).hexdigest()


def generate_registration_pin():
    """Return a random four-digit registration PIN."""
    return 1000 + secrets.randbelow(9000)


def export_grade_sheet(filename="grade_sheet.txt"):
    """Write the gradebook to filename."""
    with open(filename, "w", encoding="utf-8") as sheet:
        sheet.write(str(gradebook))
    print("Grade sheet exported to:", filename)


def main():
    """Run a short demonstration of the grading functions."""
    portal_token = os.environ.get("GRADE_PORTAL_TOKEN")
    add_grade("S01", 95)
    record_attendance("S02", 2)
    print("Is S01 passing:", check_passing_status("S01"))
    print("Calculated GPA:", compute_weighted_gpa("S01"))
    print("Student Hash:", generate_student_hash("S01"))
    print("Registration PIN:", generate_registration_pin())
    export_grade_sheet()
    print("Portal token active:", portal_token is not None)


if __name__ == "__main__":
    main()
