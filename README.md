#  Library Management System (CLI-Based)

##  Project Overview
This is a simple Command-Line Interface (CLI) based **Library Management System** built using **Python and MySQL**. It allows admins to manage books, students, and issue/return logs efficiently.

Developed as part of the internship program at **Thamizan Skills**.

---

##  Tech Stack
- **Python 3**
- **MySQL Database**
- MySQL Workbench (for DB design/export)

---

##  Features
-  Admin login system with attempt limits
-  Book Management (Add, View, Update, Delete)
-  Student Management (Add, View, Update, Delete)
-  Book Issue and Return with logging
-  Search books
-  View available vs issued books
-  Issue Logs with full transaction history

---

##  Database Tables
- `students`: Stores student details
- `books`: Stores book details and status (available/issued)
- `issuelogs`: Tracks issue and return records with dates
- `admins`: Stores login credentials for admin users

---

##  How to Run
1. Ensure MySQL Server is running.
2. Import the `database_schema.sql` file into MySQL Workbench.
3. Update your database credentials in `library.py` if needed.
4. Run the app:
   ```bash
   python library.py
