import tkinter as tk
from tkinter import Toplevel
from db_mgr import *

def open_add_window():
    win = Toplevel(root)
    win.title("Add Student")
    win.geometry("350x220")
    win.resizable(False, False)

    tk.Label(win, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(win, text="Age").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(win, text="Email").grid(row=2, column=0, padx=10, pady=5, sticky="e")

    name_var = tk.StringVar()
    age_var = tk.StringVar()
    email_var = tk.StringVar()

    tk.Entry(win, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)
    tk.Entry(win, textvariable=age_var).grid(row=1, column=1, padx=10, pady=5)
    tk.Entry(win, textvariable=email_var).grid(row=2, column=1, padx=10, pady=5)

    res_label = tk.Label(win, text="")
    res_label.grid(row=4, columnspan=2, padx=10, pady=5)

    def submit():
        try:
            name = name_var.get().strip()
            age = int(age_var.get().strip())
            email = email_var.get().strip()

            if not name or not email or not age_var.get():
                res_label.config(text="Fill all details.")
                return
            if age < 5 or age > 100:
                res_label.config(text="Enter valid age.")
                return
            if "@" not in email or "." not in email:
                res_label.config(text="Enter valid email.")
                return

            add_student(name, age, email)
            res_label.config(text="Student added!")
        except Exception as e:
            res_label.config(text=f"Error: {e}")

    tk.Button(win, text="Add", command=submit, width=15).grid(row=3, columnspan=2, pady=10)

def open_view_window():
    win = Toplevel(root)
    win.title("All Students")
    win.geometry("400x300")

    students = fetch_students()
    for id, s in enumerate(students):
        text = f"{s.RollNo} - {s.Name} - {s.Age} - {s.Email}"
        tk.Label(win, text=text, anchor="w").grid(row=id, column=0, sticky="w", padx=10, pady=2)

def open_update_window():
    win = Toplevel(root)
    win.title("Update Student")
    win.geometry("350x250")

    tk.Label(win, text="Roll Number (to update)").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(win, text="New Name").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(win, text="New Age").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    tk.Label(win, text="New Email").grid(row=3, column=0, padx=10, pady=5, sticky="e")

    roll_var = tk.StringVar()
    name_var = tk.StringVar()
    age_var = tk.StringVar()
    email_var = tk.StringVar()

    tk.Entry(win, textvariable=roll_var).grid(row=0, column=1, padx=10, pady=5)
    tk.Entry(win, textvariable=name_var).grid(row=1, column=1, padx=10, pady=5)
    tk.Entry(win, textvariable=age_var).grid(row=2, column=1, padx=10, pady=5)
    tk.Entry(win, textvariable=email_var).grid(row=3, column=1, padx=10, pady=5)

    res_label = tk.Label(win, text="")
    res_label.grid(row=5, columnspan=2, padx=10, pady=5)

    def submit():
        try:
            name = name_var.get().strip()
            age = int(age_var.get().strip())
            email = email_var.get().strip()
            roll = int(roll_var.get())

            if not name or not email or not roll_var.get() or not age_var.get():
                res_label.config(text="Fill all details.")
                return
            if age < 5 or age > 100:
                res_label.config(text="Enter valid age.")
                return
            if "@" not in email or "." not in email:
                res_label.config(text="Enter valid email.")
                return
            if not roll_exists(roll):
                res_label.config(text="Roll Number doesn't exist.")
                return

            update_student(roll, name, age, email)
            res_label.config(text="Student updated!")
        except Exception as e:
            res_label.config(text=f"Error: {e}")

    tk.Button(win, text="Update", command=submit, width=15).grid(row=4, columnspan=2, pady=10)

def open_delete_window():
    win = Toplevel(root)
    win.title("Delete Student")
    win.geometry("300x150")

    tk.Label(win, text="Roll Number").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    roll_var = tk.StringVar()
    tk.Entry(win, textvariable=roll_var).grid(row=0, column=1, padx=10, pady=10)

    res_label = tk.Label(win, text="")
    res_label.grid(row=2, columnspan=2, padx=10, pady=5)

    def submit():
        try:
            roll = int(roll_var.get())
            if not roll_exists(roll):
                res_label.config(text="Roll Number doesn't exist.")
                return
            delete_student(roll)
            res_label.config(text="Student deleted!")
        except Exception as e:
            res_label.config(text=f"Error: {e}")

    tk.Button(win, text="Delete", command=submit, width=15).grid(row=1, columnspan=2, pady=5)

root = tk.Tk()
root.title("Student Database Manager")
root.geometry("300x300")

setup_database()

tk.Label(root, text="Choose an action:", font=("Arial", 14)).pack(pady=20)
tk.Button(root, text="View Students", width=25, command=open_view_window).pack(pady=5)
tk.Button(root, text="Add Student", width=25, command=open_add_window).pack(pady=5)
tk.Button(root, text="Update Student", width=25, command=open_update_window).pack(pady=5)
tk.Button(root, text="Delete Student", width=25, command=open_delete_window).pack(pady=5)

root.mainloop()
