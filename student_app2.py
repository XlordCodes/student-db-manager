import tkinter as tk
from tkinter import messagebox
from db_mgr import *

class StudentTeacherApp:
    setup_database()
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database Management System")
        self.root.geometry("600x400")
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Student", width=20, command=self.student_login).pack(pady=10)
        tk.Button(self.root, text="Teacher", width=20, command=self.teacher_login).pack(pady=10)

    def student_login(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Roll Number:", font=("Arial", 14)).pack(pady=10)
        self.roll_entry = tk.Entry(self.root)
        self.roll_entry.pack(pady=5)
        tk.Button(self.root, text="Submit", command=self.handle_student_view).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def teacher_login(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Teacher ID:", font=("Arial", 14)).pack(pady=10)
        self.teacher_entry = tk.Entry(self.root)
        self.teacher_entry.pack(pady=5)
        tk.Button(self.root, text="Submit", command=self.handle_teacher_view).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def handle_student_view(self):
        try:
            roll_no = int(self.roll_entry.get())
            self.show_student_menu(roll_no)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Roll Number")

    def handle_teacher_view(self):
        try:
            teacher_id = int(self.teacher_entry.get())
            self.show_teacher_menu(teacher_id)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Teacher ID")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_student_menu(self, roll_no):
        self.clear_window()
        tk.Label(self.root, text=f"Student Menu - Roll No: {roll_no}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="View Subjects", width=25,
                  command=lambda: self.display_student_subjects(roll_no)).pack(pady=5)
        tk.Button(self.root, text="View Marks", width=25,
                  command=lambda: self.display_student_marks(roll_no)).pack(pady=5)
        tk.Button(self.root, text="View Attendance", width=25,
                  command=lambda: self.display_student_attendance(roll_no)).pack(pady=5)
        tk.Button(self.root, text="Compare Performance", width=25,
                  command=lambda: self.display_student_comparison(roll_no)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=10)

    def popup_message(self, title, message):
        top = tk.Toplevel(self.root)
        top.title(title)
        text = tk.Text(top, wrap=tk.WORD)
        text.insert(tk.END, message)
        text.pack(expand=True, fill="both")
        tk.Button(top, text="Close", command=top.destroy).pack(pady=5)

    def display_student_subjects(self, roll_no):
        overview = get_student_overview(roll_no)
        if overview["subjects"]:
            text = "\n".join([f"{row[0]} - {row[1]}" for row in overview["subjects"]])
        else:
            text = "No subjects found"
        self.popup_message("Subjects", text)

    def display_student_marks(self, roll_no):
        df = fetch_student_marks(roll_no)
        text = df.to_string(index=False) if not df.empty else "No marks found"
        self.popup_message("Marks", text)

    def display_student_attendance(self, roll_no):
        df = fetch_student_attendance(roll_no)
        text = df.to_string(index=False) if not df.empty else "No attendance records found"
        self.popup_message("Attendance", text)

    def display_student_comparison(self, roll_no):
        df = compare_student_performance(roll_no)
        text = df.to_string(index=False) if df is not None and not df.empty else "No performance data found"
        self.popup_message("Comparison", text)

    def show_teacher_menu(self, teacher_id):
        self.clear_window()
        label = tk.Label(self.root, text=f"Teacher Menu - ID: {teacher_id}", font=("Arial", 14))
        label.pack(pady=10)
        tk.Button(self.root, text="View Assigned Classes", width=25,
                  command=lambda: self.display_teacher_classes(teacher_id)).pack(pady=5)
        tk.Button(self.root, text="Class Performance Summary", width=25,
                  command=lambda: self.display_class_performance(teacher_id)).pack(pady=5)
        tk.Button(self.root, text="View Student Details", width=25,
                  command=lambda: self.ask_student_id_for_details()).pack(pady=5)
        tk.Button(self.root, text="Add / Update Marks", width=25,
                  command=self.add_update_marks).pack(pady=5)
        tk.Button(self.root, text="Add Attendance", width=25,
                  command=self.add_attendance_record).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=10)

    def display_teacher_classes(self, teacher_id):
        df = fetch_teacher_classes(teacher_id)
        if not df.empty:
            text = df.to_string(index=False)
        else:
            text = "No assigned classes"
        self.popup_message("Assigned Classes", text)

    def display_class_performance(self, teacher_id):
        result = get_class_performance_summary(teacher_id)
        if not result:
            self.popup_message("Performance", "No data found")
            return
        df1 = result["students"]
        df2 = result["attendance_summary"]
        df3 = result["performance_summary"]
        combined = df1.merge(df2, on="RollNo", how="left").merge(df3, on="RollNo", how="left")
        text = combined.to_string(index=False)
        self.popup_message("Class Performance", text)

    def ask_student_id_for_details(self):
        self.clear_window()
        label = tk.Label(self.root, text="Enter Student Roll Number:", font=("Arial", 14))
        label.pack(pady=10)
        entry = tk.Entry(self.root)
        entry.pack(pady=5)
        tk.Button(self.root, text="View", command=lambda: self.display_individual_student(entry.get())).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def display_individual_student(self, roll_no):
        try:
            roll_no = int(roll_no)
            marks_df = fetch_student_marks(roll_no)
            attend_df = fetch_student_attendance(roll_no)
            result = f"Marks:\n{marks_df.to_string(index=False)}\n\nAttendance:\n{attend_df.to_string(index=False)}"
            self.popup_message(f"Student {roll_no} Details", result)
        except:
            messagebox.showerror("Error", "Invalid Roll Number or No Data")

    def add_update_marks(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Roll No").pack()
        roll_entry = tk.Entry(self.root)
        roll_entry.pack()
        tk.Label(self.root, text="Enter Subject ID").pack()
        subject_entry = tk.Entry(self.root)
        subject_entry.pack()
        tk.Label(self.root, text="Enter Mark").pack()
        mark_entry = tk.Entry(self.root)
        mark_entry.pack()
        tk.Label(self.root, text="Enter Exam Date (YYYY-MM-DD)").pack()
        date_entry = tk.Entry(self.root)
        date_entry.pack()
        tk.Button(self.root, text="Submit", command=lambda: self.save_mark(
            roll_entry.get(), subject_entry.get(), mark_entry.get(), date_entry.get())).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def save_mark(self, roll, subject, mark, date):
        try:
            conn = conn_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT MarksID FROM Marks
                WHERE RollNo=? AND SubjectID=? AND ExamDate=?
            """, (roll, subject, date))
            existing = cursor.fetchone()
            if existing:
                cursor.execute("""
                    UPDATE Marks SET Mark=? WHERE MarksID=?
                """, (mark, existing.MarksID))
            else:
                cursor.execute("""
                    INSERT INTO Marks (RollNo, SubjectID, Mark, ExamDate) VALUES (?, ?, ?, ?)
                """, (roll, subject, mark, date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Mark saved")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_attendance_record(self):
        self.clear_window()
        tk.Label(self.root, text="Enter Roll No").pack()
        roll_entry = tk.Entry(self.root)
        roll_entry.pack()
        tk.Label(self.root, text="Enter Subject ID").pack()
        subject_entry = tk.Entry(self.root)
        subject_entry.pack()
        tk.Label(self.root, text="Enter Date (YYYY-MM-DD)").pack()
        date_entry = tk.Entry(self.root)
        date_entry.pack()
        tk.Label(self.root, text="Enter Status (Present/Absent)").pack()
        status_entry = tk.Entry(self.root)
        status_entry.pack()
        tk.Button(self.root, text="Submit", command=lambda: self.save_attendance(
            roll_entry.get(), subject_entry.get(), date_entry.get(), status_entry.get())).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def save_attendance(self, roll, subject, date, status):
        try:
            conn = conn_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Attendance (RollNo, SubjectID, AttendanceDate, Status)
                VALUES (?, ?, ?, ?)
            """, (roll, subject, date, status))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Attendance recorded")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentTeacherApp(root)
    root.mainloop()