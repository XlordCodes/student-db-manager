import tkinter as tk
from tkinter import messagebox
from db_mgr import *

class StudentTeacherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student-Teacher Information Portal")
        self.root.geometry("600x400")
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        title = tk.Label(self.root, text="Welcome", font=("Arial", 20))
        title.pack(pady=20)
        student_btn = tk.Button(self.root, text="Student", width=20, command=self.student_login)
        student_btn.pack(pady=10)
        teacher_btn = tk.Button(self.root, text="Teacher", width=20, command=self.teacher_login)
        teacher_btn.pack(pady=10)

    def student_login(self):
        self.clear_window()
        label = tk.Label(self.root, text="Enter Roll Number:", font=("Arial", 14))
        label.pack(pady=10)
        self.roll_entry = tk.Entry(self.root)
        self.roll_entry.pack(pady=5)
        submit_btn = tk.Button(self.root, text="Submit", command=self.handle_student_view)
        submit_btn.pack(pady=10)
        back_btn = tk.Button(self.root, text="Back", command=self.show_main_menu)
        back_btn.pack(pady=5)

    def teacher_login(self):
        self.clear_window()
        label = tk.Label(self.root, text="Enter Teacher ID:", font=("Arial", 14))
        label.pack(pady=10)
        self.teacher_entry = tk.Entry(self.root)
        self.teacher_entry.pack(pady=5)
        submit_btn = tk.Button(self.root, text="Submit", command=self.handle_teacher_view)
        submit_btn.pack(pady=10)
        back_btn = tk.Button(self.root, text="Back", command=self.show_main_menu)
        back_btn.pack(pady=5)

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
        label = tk.Label(self.root, text=f"Student Menu - Roll No: {roll_no}", font=("Arial", 14))
        label.pack(pady=10)
        btn1 = tk.Button(self.root, text="View Subjects", width=25,
                         command=lambda: self.display_student_subjects(roll_no))
        btn1.pack(pady=5)
        btn2 = tk.Button(self.root, text="View Marks", width=25,
                         command=lambda: self.display_student_marks(roll_no))
        btn2.pack(pady=5)
        btn3 = tk.Button(self.root, text="View Attendance", width=25,
                         command=lambda: self.display_student_attendance(roll_no))
        btn3.pack(pady=5)
        btn4 = tk.Button(self.root, text="Compare Performance", width=25,
                         command=lambda: self.display_student_comparison(roll_no))
        btn4.pack(pady=5)
        back_btn = tk.Button(self.root, text="Back", command=self.show_main_menu)
        back_btn.pack(pady=10)

    def display_student_subjects(self, roll_no):
        overview = get_student_overview(roll_no)
        if overview["subjects"]:
            text = "\n".join([f"{row[0]} - {row[1]}" for row in overview["subjects"]])
        else:
            text = "No subjects found"
        self.popup_message("Subjects", text)

    def display_student_marks(self, roll_no):
        df = fetch_student_marks(roll_no)
        if not df.empty:
            text = df.to_string(index=False)
        else:
            text = "No marks found"
        self.popup_message("Marks", text)

    def display_student_attendance(self, roll_no):
        df = fetch_student_attendance(roll_no)
        if not df.empty:
            text = df.to_string(index=False)
        else:
            text = "No attendance records found"
        self.popup_message("Attendance", text)

    def display_student_comparison(self, roll_no):
        df = compare_student_performance(roll_no)
        if df is None or df.empty:
            text = "No performance data found"
        else:
            text = df.to_string(index=False)
        self.popup_message("Comparison", text)

    def popup_message(self, title, message):
        top = tk.Toplevel(self.root)
        top.title(title)
        text = tk.Text(top, wrap=tk.WORD)
        text.insert(tk.END, message)
        text.pack(expand=True, fill="both")
        close_btn = tk.Button(top, text="Close", command=top.destroy)
        close_btn.pack(pady=5)

    def show_teacher_menu(self, teacher_id):
        self.clear_window()
        label = tk.Label(self.root, text=f"Teacher Menu - ID: {teacher_id}", font=("Arial", 14))
        label.pack(pady=10)
        btn1 = tk.Button(self.root, text="View Assigned Classes", width=25,
                         command=lambda: self.display_teacher_classes(teacher_id))
        btn1.pack(pady=5)
        btn2 = tk.Button(self.root, text="Class Performance Summary", width=25,
                         command=lambda: self.display_class_performance(teacher_id))
        btn2.pack(pady=5)
        btn3 = tk.Button(self.root, text="Back", command=self.show_main_menu)
        btn3.pack(pady=10)

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

root = tk.Tk()
app = StudentTeacherApp(root)
root.mainloop()
