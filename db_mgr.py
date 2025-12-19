import pyodbc
import numpy
import pandas as pd

db_path = # INCLUDE PATH HERE TO YOUR DATABASE FILE

def conn_db():
    conn_str = (r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
                fr'DBQ={db_path};')
    return pyodbc.connect(conn_str)

def table_exists(name: str) -> bool:
    conn = conn_db()
    cur = conn.cursor()
    exists = cur.tables(table=name).fetchone() is not None
    conn.close()
    return exists

def create_classes_table():
    if not table_exists('Classes'):
        conn = conn_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE Classes (
                ClassID AUTOINCREMENT PRIMARY KEY,
                ClassName TEXT(50)
            )
        """)
        conn.commit()
        conn.close()

def create_students_table():
    if not table_exists('Students'):
        conn = conn_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE Students (
                RollNo AUTOINCREMENT PRIMARY KEY,
                Name TEXT(100),
                Age INT,
                Email TEXT(100),
                ClassID INT,
                FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
            )
        """)
        conn.commit()
        conn.close()

def create_teachers_table():
    if not table_exists('Teachers'):
        conn = conn_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE Teachers (
                TeacherID AUTOINCREMENT PRIMARY KEY,
                Name TEXT(100),
                Email TEXT(100),
                SubjectID INT,
                FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
            )
        """)
        conn.commit()
        conn.close()

def create_subjects_table():
    if not table_exists('Subjects'):
        conn = conn_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE Subjects (
                SubjectID AUTOINCREMENT PRIMARY KEY,
                Name TEXT(100),
                ClassID INT,
                FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
            )
        """)
        conn.commit()
        conn.close()

def create_teacher_class_map():
    if not table_exists('TeacherClassMap'):
        conn = conn_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE TeacherClassMap (
                ID AUTOINCREMENT PRIMARY KEY,
                TeacherID INT,
                ClassID INT,
                FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID),
                FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
            )
        """)
        conn.commit()
        conn.close()

def create_classsubjects_table():
    if not table_exists('ClassSubjects'):
        conn = conn_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE ClassSubjects (
                CSID AUTOINCREMENT PRIMARY KEY,
                ClassID INT,
                SubjectID INT,
                TeacherID INT,
                FOREIGN KEY (ClassID) REFERENCES Classes(ClassID),
                FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID),
                FOREIGN KEY (TeacherID) REFERENCES Teachers(TeacherID)
            )
        """)
        conn.commit()
        conn.close()

def create_marks_table():
    if not table_exists('Marks'):
        conn = conn_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE Marks (
                MarksID AUTOINCREMENT PRIMARY KEY,
                RollNo INT,
                SubjectID INT,
                Mark FLOAT,
                ExamDate DATETIME,
                FOREIGN KEY (RollNo) REFERENCES Students(RollNo),
                FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
            )
        """)
        conn.commit()
        conn.close()

def create_attendance_table():
    if not table_exists('Attendance'):
        conn = conn_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE Attendance (
                AttendanceID AUTOINCREMENT PRIMARY KEY,
                RollNo INT,
                SubjectID INT,
                AttendanceDate DATETIME,
                Status TEXT(10),
                FOREIGN KEY (RollNo) REFERENCES Students(RollNo),
                FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
            )
        """)
        conn.commit()
        conn.close()

def setup_database():
    create_classes_table()
    create_subjects_table()
    create_teachers_table()
    create_students_table()
    create_classsubjects_table()
    create_marks_table()
    create_teacher_class_map()
    create_attendance_table()

def fetch_students(class_id: int = None):
    conn = conn_db()
    cursor = conn.cursor()
    if class_id:
        cursor.execute("SELECT * FROM Students WHERE ClassID = ?", (class_id,))
    else:
        cursor.execute("SELECT * FROM Students")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_student(name: str, age: int, email: str, class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Students (Name, Age, Email, ClassID) VALUES (?, ?, ?, ?)", (name, age, email, class_id))
    conn.commit()
    conn.close()

def update_student(roll: int, name: str, age: int, email: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Students SET Name = ?, Age = ?, Email = ? WHERE RollNo = ?", (name, age, email, roll))
    conn.commit()
    conn.close()

def delete_student(roll: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Students WHERE RollNo = ?", (roll,))
    conn.commit()
    conn.close()

def roll_exists(roll: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Students WHERE RollNo = ?", (roll,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def fetch_teacher_class_map():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TeacherClassMap")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_teacher_class(teacher_id: int, class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO TeacherClassMap (TeacherID, ClassID) VALUES (?, ?)", (teacher_id, class_id))
    conn.commit()
    conn.close()

def update_teacher_class_map(map_id: int, teacher_id: int, class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE TeacherClassMap SET TeacherID = ?, ClassID = ? WHERE ID = ?", (teacher_id, class_id, map_id))
    conn.commit()
    conn.close()

def delete_teacher_class_map(map_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TeacherClassMap WHERE ID = ?", (map_id,))
    conn.commit()
    conn.close()

def teacher_class_map_exists(map_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM TeacherClassMap WHERE ID = ?", (map_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def fetch_classes_for_teacher(teacher_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ClassID FROM TeacherClassMap WHERE TeacherID = ?", (teacher_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row.ClassID for row in rows]

def fetch_teachers_for_class(class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT TeacherID FROM TeacherClassMap WHERE ClassID = ?", (class_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row.TeacherID for row in rows]

def fetch_teachers():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teachers")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_teacher(name: str, email: str, subject_id: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Teachers (Name, Email, SubjectID) VALUES (?, ?, ?)", (name, email, subject_id))
    conn.commit()
    conn.close()

def update_teacher(teacher_id: int, name: str, email: str, subject_id: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Teachers SET Name = ?, Email = ?, SubjectID = ? WHERE TeacherID = ?", (name, email, subject_id, teacher_id))
    conn.commit()
    conn.close()

def delete_teacher(teacher_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Teachers WHERE TeacherID = ?", (teacher_id,))
    conn.commit()
    conn.close()

def teacher_exists(teacher_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Teachers WHERE TeacherID = ?", (teacher_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def fetch_subjects(class_id: int = None):
    conn = conn_db()
    cursor = conn.cursor()
    if class_id:
        cursor.execute("SELECT * FROM Subjects WHERE ClassID = ?", (class_id,))
    else:
        cursor.execute("SELECT * FROM Subjects")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_subject(name: str, class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Subjects (Name, ClassID) VALUES (?, ?)", (name, class_id))
    conn.commit()
    conn.close()

def update_subject(subject_id: int, name: str, class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Subjects SET Name = ?, ClassID = ? WHERE SubjectID = ?", (name, class_id, subject_id))
    conn.commit()
    conn.close()

def delete_subject(subject_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Subjects WHERE SubjectID = ?", (subject_id,))
    conn.commit()
    conn.close()

def subject_exists(subject_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Subjects WHERE SubjectID = ?", (subject_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def fetch_classes():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Classes")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_class(name: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Classes (ClassName) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def update_class(class_id: int, name: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Classes SET ClassName = ? WHERE ClassID = ?", (name, class_id))
    conn.commit()
    conn.close()

def delete_class(class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Classes WHERE ClassID = ?", (class_id,))
    conn.commit()
    conn.close()

def class_exists(class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Classes WHERE ClassID = ?", (class_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def fetch_marks():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Marks")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_marks(roll_no: int, subject_id: int, mark: float, exam_date: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Marks (RollNo, SubjectID, Mark, ExamDate) VALUES (?, ?, ?, ?)",
        (roll_no, subject_id, mark, exam_date)
    )
    conn.commit()
    conn.close()

def update_marks(marks_id: int, roll_no: int, subject_id: int, mark: float, exam_date: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Marks SET RollNo = ?, SubjectID = ?, Mark = ?, ExamDate = ? WHERE MarksID = ?",
        (roll_no, subject_id, mark, exam_date, marks_id)
    )
    conn.commit()
    conn.close()

def delete_marks(marks_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Marks WHERE MarksID = ?", (marks_id,))
    conn.commit()
    conn.close()

def marks_exists(marks_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Marks WHERE MarksID = ?", (marks_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def fetch_attendance():
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Attendance")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_attendance(roll_no: int, subject_id: int, date: str, status: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Attendance (RollNo, SubjectID, AttendanceDate, Status) VALUES (?, ?, ?, ?)", (roll_no, subject_id, date, status))
    conn.commit()
    conn.close()

def update_attendance(attendance_id: int, roll_no: int, date: str, status: str):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE Attendance SET RollNo = ?, AttendanceDate = ?, Status = ? WHERE AttendanceID = ?", (roll_no, date, status, attendance_id))
    conn.commit()
    conn.close()

def delete_attendance(attendance_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Attendance WHERE AttendanceID = ?", (attendance_id,))
    conn.commit()
    conn.close()

def attendance_exists(attendance_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Attendance WHERE AttendanceID = ?", (attendance_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def get_student_subjects(roll_no: int):
    conn = conn_db()
    query = """
        SELECT Subjects.SubjectID, Subjects.Name, Teachers.Name AS TeacherName
        FROM Students
        INNER JOIN ClassSubjects ON Students.ClassID = ClassSubjects.ClassID
        INNER JOIN Subjects ON ClassSubjects.SubjectID = Subjects.SubjectID
        INNER JOIN Teachers ON ClassSubjects.TeacherID = Teachers.TeacherID
        WHERE Students.RollNo = ?
    """
    df = pd.read_sql(query, conn, params=(roll_no,))
    conn.close()
    return df

def get_student_marks(roll_no: int):
    conn = conn_db()
    query = """
        SELECT Subjects.Name AS Subject, Marks.Mark, Marks.ExamDate
        FROM Marks
        JOIN Subjects ON Marks.SubjectID = Subjects.SubjectID
        WHERE Marks.RollNo = ?
    """
    df = pd.read_sql(query, conn, params=(roll_no,))
    conn.close()
    return df

def get_student_attendance(roll_no: int):
    conn = conn_db()
    query = """
        SELECT AttendanceDate, Status
        FROM Attendance
        WHERE RollNo = ?
        ORDER BY AttendanceDate
    """
    df = pd.read_sql(query, conn, params=(roll_no,))
    conn.close()
    return df

def get_class_peers(roll_no: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ClassID FROM Students WHERE RollNo = ?", (roll_no,))
    result = cursor.fetchone()
    if not result:
        return pd.DataFrame()
    class_id = result[0]
    conn.close()

    conn = conn_db()
    df = pd.read_sql("SELECT * FROM Students WHERE ClassID = ?", conn, params=(class_id,))
    conn.close()
    return df

def get_class_marks_by_class(class_id: int):
    conn = conn_db()
    query = """
        SELECT Students.Name AS Student, Subjects.Name AS Subject, Marks.Mark
        FROM Marks
        JOIN Students ON Marks.RollNo = Students.RollNo
        JOIN Subjects ON Marks.SubjectID = Subjects.SubjectID
        WHERE Students.ClassID = ?
    """
    df = pd.read_sql(query, conn, params=(class_id,))
    conn.close()
    return df

def get_class_attendance_summary(class_id: int):
    conn = conn_db()
    query = """
        SELECT Students.Name, COUNT(*) AS TotalDays,
               SUM(IIF(Status='Present', 1, 0)) AS PresentDays
        FROM Attendance
        JOIN Students ON Attendance.RollNo = Students.RollNo
        WHERE Students.ClassID = ?
        GROUP BY Students.Name
    """
    df = pd.read_sql(query, conn, params=(class_id,))
    conn.close()
    return df

def assign_class_to_student(roll_no: int, class_id: int):
    conn = conn_db()
    cur = conn.cursor()
    cur.execute("UPDATE Students SET ClassID = ? WHERE RollNo = ?", (class_id, roll_no))
    conn.commit()
    conn.close()

def fetch_students_in_class(class_id: int) -> pd.DataFrame:
    conn = conn_db()
    df = pd.read_sql("SELECT RollNo, Name, Age, Email FROM Students WHERE ClassID = ?", conn, params=(class_id,))
    conn.close()
    return df

def fetch_subjects_for_class(class_id: int) -> pd.DataFrame:
    conn = conn_db()
    query = """
      SELECT Subjects.SubjectID, Subjects.Name AS SubjectName, Teachers.TeacherID, Teachers.Name AS TeacherName
      FROM ClassSubjects
      INNER JOIN Subjects ON ClassSubjects.SubjectID = Subjects.SubjectID
      INNER JOIN Teachers ON ClassSubjects.TeacherID = Teachers.TeacherID
      WHERE ClassSubjects.ClassID = ?
    """
    df = pd.read_sql(query, conn, params=(class_id,))
    conn.close()
    return df

def fetch_student_marks(roll_no: int) -> pd.DataFrame:
    conn = conn_db()
    df = pd.read_sql("""
        SELECT Marks.MarksID, Subjects.Name AS Subject, Marks.Mark
        FROM Marks
        INNER JOIN Subjects ON Marks.SubjectID = Subjects.SubjectID
        WHERE Marks.RollNo = ?
    """, conn, params=(roll_no,))
    conn.close()
    return df

def fetch_student_attendance(roll_no: int) -> pd.DataFrame:
    conn = conn_db()
    df = pd.read_sql("""
        SELECT Subjects.Name AS Subject, Attendance.AttendanceDate, Attendance.Status
        FROM Attendance
        INNER JOIN Subjects ON Attendance.SubjectID = Subjects.SubjectID
        WHERE Attendance.RollNo = ?
        ORDER BY Attendance.AttendanceDate
    """, conn, params=(roll_no,))
    conn.close()
    return df


def fetch_class_marks_summary(class_id: int) -> pd.DataFrame:
    conn = conn_db()
    df = pd.read_sql("""
        SELECT Students.Name AS Student, Subjects.Name AS Subject, Marks.Mark
        FROM Marks
        INNER JOIN Students ON Marks.RollNo = Students.RollNo
        INNER JOIN Subjects ON Marks.SubjectID = Subjects.SubjectID
        WHERE Students.ClassID = ?
    """, conn, params=(class_id,))
    conn.close()
    return df

def fetch_class_attendance_summary(class_id: int) -> pd.DataFrame:
    conn = conn_db()
    df = pd.read_sql("""
        SELECT Students.Name AS Student,
            COUNT(Attendance.AttendanceID) AS Total,
            SUM(IIF(Attendance.Status='Present',1,0)) AS Present
        FROM Attendance
        INNER JOIN Students ON Attendance.RollNo = Students.RollNo
        WHERE Students.ClassID = ?
        GROUP BY Students.Name
    """, conn, params=(class_id,))
    conn.close()
    return df

def fetch_teacher_classes(teacher_id: int) -> pd.DataFrame:
    conn = conn_db()
    df = pd.read_sql("""
        SELECT DISTINCT Classes.ClassID, Classes.ClassName
        FROM ClassSubjects
        INNER JOIN Classes ON ClassSubjects.ClassID = Classes.ClassID
        WHERE ClassSubjects.TeacherID = ?
    """, conn, params=(teacher_id,))
    conn.close()
    return df

def fetch_class_subjects_for_teacher(teacher_id: int) -> pd.DataFrame:
    conn = conn_db()
    df = pd.read_sql("""
      SELECT cs.ClassID, c.ClassName, subj.SubjectID, subj.Name AS SubjectName
      FROM ClassSubjects cs
      JOIN Classes c ON cs.ClassID = c.ClassID
      JOIN Subjects subj ON cs.SubjectID = subj.SubjectID
      WHERE cs.TeacherID = ?
    """, conn, params=(teacher_id,))
    conn.close()
    return df

import pandas as pd

def get_student_overview(roll_no: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Subjects.SubjectID, Subjects.Name 
        FROM Students, Subjects
        WHERE Students.ClassID = Subjects.ClassID AND Students.RollNo = ?
    """, (roll_no,))
    subjects = cursor.fetchall()

    marks_df = pd.read_sql_query("""
        SELECT Subjects.Name AS Subject, Marks.ExamDate, Marks.Mark
        FROM Marks
        INNER JOIN Subjects ON Marks.SubjectID = Subjects.SubjectID
        WHERE Marks.RollNo = ?
        ORDER BY Marks.ExamDate
    """, conn, params=(roll_no,))

    attendance_df = pd.read_sql_query("""
        SELECT AttendanceDate, Status
        FROM Attendance
        WHERE RollNo = ?
        ORDER BY AttendanceDate
    """, conn, params=(roll_no,))

    conn.close()
    return {
        "subjects": subjects,
        "marks": marks_df,
        "attendance": attendance_df
    }

def compare_student_performance(roll_no: int):
    conn = conn_db()
    cursor = conn.cursor()
    cursor.execute("SELECT ClassID FROM Students WHERE RollNo = ?", (roll_no,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return None
    class_id = result[0]
    cursor.execute("SELECT SubjectID, Name FROM Subjects WHERE ClassID = ?", (class_id,))
    subjects = cursor.fetchall()
    data = []
    for subj in subjects:
        subject_id, subject_name = subj[0], subj[1]
        cursor.execute("""
            SELECT AVG(Mark) as avg_mark 
            FROM Marks 
            WHERE RollNo = ? AND SubjectID = ?
        """, (roll_no, subject_id))
        student_avg_result = cursor.fetchone()
        student_avg = student_avg_result[0] if student_avg_result and student_avg_result[0] is not None else 0
        cursor.execute("""
            SELECT AVG(Mark) as avg_mark 
            FROM Marks 
            WHERE SubjectID = ? AND RollNo IN (
                SELECT RollNo FROM Students WHERE ClassID = ?
            )
        """, (subject_id, class_id))
        class_avg_result = cursor.fetchone()
        class_avg = class_avg_result[0] if class_avg_result and class_avg_result[0] is not None else 0
        data.append({
            "Subject": subject_name,
            "Student_Avg": student_avg,
            "Class_Avg": class_avg
        })
    conn.close()
    return pd.DataFrame(data)

def get_class_performance_summary(teacher_id: int):
    conn = conn_db()
    cursor = conn.cursor()

    cursor.execute("SELECT ClassID FROM TeacherClassMap WHERE TeacherID = ?", (teacher_id,))
    class_ids = [row.ClassID for row in cursor.fetchall()]
    if not class_ids:
        conn.close()
        return None

    class_placeholder = ",".join("?" * len(class_ids))
    students_df = pd.read_sql_query(f"""
        SELECT RollNo, Name, ClassID
        FROM Students
        WHERE ClassID IN ({class_placeholder})
    """, conn, params=class_ids)

    if students_df.empty:
        conn.close()
        return None

    roll_nos = students_df["RollNo"].tolist()
    roll_placeholder = ",".join("?" * len(roll_nos))

    attendance_df = pd.read_sql_query(f"""
        SELECT RollNo, 
               AVG(IIF(Status = 'Present', 1, 0)) * 100 AS AttendancePercent
        FROM Attendance
        WHERE RollNo IN ({roll_placeholder})
        GROUP BY RollNo
    """, conn, params=roll_nos)

    performance_df = pd.read_sql_query(f"""
        SELECT RollNo, AVG(Mark) AS AverageMark
        FROM Marks
        WHERE RollNo IN ({roll_placeholder})
        GROUP BY RollNo
    """, conn, params=roll_nos)

    conn.close()

    return {
        "students": students_df,
        "attendance_summary": attendance_df,
        "performance_summary": performance_df
    }

def get_overall_class_summary(class_id: int):
    conn = conn_db()
    cursor = conn.cursor()
    attendance_df = pd.read_sql_query("""
        SELECT RollNo, AVG(IIF(Status = 'Present' THEN 1 ELSE 0 END))*100 AS AttendancePercent
        FROM Attendance
        WHERE RollNo IN (SELECT RollNo FROM Students WHERE ClassID = ?)
        GROUP BY RollNo
    """, conn, params=(class_id,))
    attendance_avg = attendance_df['AttendancePercent'].mean() if not attendance_df.empty else 0
    performance_df = pd.read_sql_query("""
        SELECT AVG(Mark) AS AvgMark
        FROM Marks
        WHERE RollNo IN (SELECT RollNo FROM Students WHERE ClassID = ?)
    """, conn, params=(class_id,))
    performance_avg = performance_df['AvgMark'].iloc[0] if not performance_df.empty else 0
    subject_perf_df = pd.read_sql_query("""
            SELECT Subjects.Name AS Subject, AVG(Marks.Mark) AS AvgMark
            FROM Marks
            INNER JOIN Subjects ON Marks.SubjectID = Subjects.SubjectID
            WHERE Marks.RollNo IN (SELECT RollNo FROM Students WHERE ClassID = ?)
            GROUP BY Subjects.Name
            """, conn, params=(class_id,))
    conn.close()
    return {
        "attendance_avg": attendance_avg,
        "performance_avg": performance_avg,
        "subject_performance": subject_perf_df
    }

