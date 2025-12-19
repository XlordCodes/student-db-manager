Student Information & Database Management System
A robust, Python-based desktop application designed to manage educational records. This project features a multi-portal system for students and teachers, utilizing a Microsoft Access backend managed via pyodbc and pandas for data analysis.

🚀 Features
👤 Student Portal
Subject Overview: View assigned subjects and respective teachers.

Academic Tracking: Access marks and performance history.

Attendance Monitoring: Check real-time attendance status.

Performance Comparison: Compare individual averages against the class mean using data analytics.

👩‍🏫 Teacher Portal
Class Management: View all assigned classes and student rosters.

Data Entry: Add or update student marks and record daily attendance.

Analytics: Generate class performance summaries and individual student deep-dives.

⚙️ Administrative & Database Logic
Automated Setup: Self-initializing database schema including tables for Classes, Students, Teachers, Subjects, Marks, and Attendance.

Relational Mapping: Complex table relationships (e.g., Teacher-Class mapping, Class-Subject associations).

Sample Data Utility: A dedicated script to populate the system for testing.

🛠️ Tech Stack
Language: Python 3.x

GUI Framework: Tkinter

Database: Microsoft Access (.accdb or .mdb)

Libraries: * pyodbc: For database connectivity.

pandas: For data manipulation and reporting.

numpy: For numerical operations.

📂 Project Structure
Plaintext

├── db_mgr.py        # Core database engine & CRUD operations
├── student_app.py   # Basic administrative GUI for student records
├── student_app1.py  # Portal-based GUI (Student/Teacher view)
├── student_app2.py  # Advanced GUI with Mark entry and detailed analytics
├── use.py           # Utility script to populate sample data
└── .gitignore       # Git exclusion rules
🚦 Getting Started
1. Prerequisites
MS Access Database Engine: Ensure you have the Microsoft Access Driver installed on your Windows machine.

Python Libraries:

Bash

pip install pyodbc pandas numpy
2. Database Configuration
Create an empty Microsoft Access file (e.g., SchoolDB.accdb).

Open db_mgr.py and update the db_path variable with your local path:

Python

db_path = r'C:\Your\Path\To\SchoolDB.accdb'
3. Initialization
Run the use.py script once to generate the tables and populate the system with sample students, teachers, and marks:

Bash

python use.py
4. Running the App
To launch the full-featured portal (Student & Teacher login), run:

Bash

python student_app2.py
📊 Data Insights
The system uses pandas to perform SQL-like joins and aggregations, providing teachers with a "Class Performance Summary" that merges student identity, attendance percentages, and average marks into a single scannable view.

📝 License
This project is open-source. Feel free to fork and modify it for your own educational or management needs.
