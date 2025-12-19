from db_mgr import *
def populate_sample_data():
    setup_database()

    add_class("Class A")
    add_class("Class B")

    add_subject("Math", 1)
    add_subject("Science", 1)
    add_subject("English", 2)
    add_subject("History", 2)

    add_teacher("Raj", "raj@example.com", 1)
    add_teacher("Anita", "anita@example.com", 2)
    add_teacher("Vikram", "vikram@example.com", 3)
    add_teacher("Priya", "priya@example.com", 4)

    add_teacher_class(1, 1)
    add_teacher_class(2, 1)
    add_teacher_class(3, 2)
    add_teacher_class(4, 2)

    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ClassSubjects (ClassID, SubjectID, TeacherID) VALUES (1, 1, 1)")
    cursor.execute("INSERT INTO ClassSubjects (ClassID, SubjectID, TeacherID) VALUES (1, 2, 2)")
    cursor.execute("INSERT INTO ClassSubjects (ClassID, SubjectID, TeacherID) VALUES (2, 3, 3)")
    cursor.execute("INSERT INTO ClassSubjects (ClassID, SubjectID, TeacherID) VALUES (2, 4, 4)")
    conn.commit()
    conn.close()

    students = [
        ("Aarav", 16, "aarav@example.com", 1),
        ("Isha", 15, "isha@example.com", 1),
        ("Kabir", 16, "kabir@example.com", 1),
        ("Meera", 17, "meera@example.com", 1),
        ("Rohan", 16, "rohan@example.com", 1),
        ("Tara", 17, "tara@example.com", 2),
        ("Aryan", 16, "aryan@example.com", 2),
        ("Diya", 16, "diya@example.com", 2),
        ("Neha", 17, "neha@example.com", 2),
        ("Yash", 15, "yash@example.com", 2)
    ]

    for student in students:
        add_student(*student)

    sample_marks = [
        (1, 1, 85.5, "2024-01-15"),
        (1, 2, 78.0, "2024-02-20"),
        (2, 1, 91.0, "2024-01-15"),
        (3, 1, 72.0, "2024-01-15"),
        (4, 2, 88.0, "2024-02-20"),
        (6, 3, 88.5, "2024-03-10"),
        (7, 4, 92.0, "2024-03-11"),
        (8, 3, 75.0, "2024-03-12"),
        (9, 4, 81.0, "2024-03-13"),
        (10, 4, 89.0, "2024-03-14")
    ]

    for mark in sample_marks:
        add_marks(*mark)

    sample_attendance = [
        (1, 1, "2024-01-10", "Present"),
        (1, 2, "2024-01-10", "Absent"),
        (2, 1, "2024-01-10", "Present"),
        (3, 1, "2024-01-11", "Present"),
        (4, 2, "2024-01-11", "Present"),
        (6, 3, "2024-01-10", "Present"),
        (7, 4, "2024-01-10", "Present"),
        (8, 3, "2024-01-11", "Absent"),
        (9, 4, "2024-01-11", "Present"),
        (10, 4, "2024-01-12", "Present")
    ]

    for attendance in sample_attendance:
        add_attendance(*attendance)

    print("Sample data populated successfully.")

populate_sample_data()