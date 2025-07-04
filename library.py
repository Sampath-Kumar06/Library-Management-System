import mysql.connector
try:
    conn=mysql.connector.connect(
        host='localhost',
        user='root',
        password='sampath#125#',
        database='library_system'
    )
    cursor=conn.cursor()
except Exception as e:
    print(e)

# Admin login
def admin_login():
    attempts = 3
    while attempts > 0:
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            print(f"\n Login successful. Welcome, {username}\n")
            return True
        else:
            attempts -= 1
            print("Invalid credentials")
            if attempts > 0:
                print(f"You have {attempts} attempts left.\n")
            else:
                print("Login failed. No attempts left.\n")
                return False

def main():
    while True:
        print("---- MAIN MENU -----")
        print("Library Management System")
        print("Select options to perform operations:")
        print("1. View all students")
        print("2. View all books")
        print("3. view all issuelogs")
        print("4. Issue a book")
        print("5. Return a book")
        print("6. Search books")
        print("7. Add Student")
        print("8. Add Book")
        print("9. Delete Student")
        print("10. Delete Book")
        print("11. Update Book Information")
        print("12. Update Student Information")
        print("13. View Available Books")
        print("14. View Issued Books")
        print("15. Exit")
        print("\n")
        choice=int(input("Enter your choice from above menu:"))
        rangee=[i for i in range(1,16)]
        if choice not in rangee:
            print(f"Please select only from {rangee} numbers")
        else:
            if choice == 1:
                view_students()
            if choice==2:
                view_books()
            if choice==3:
                issuelogs()
            if choice==4:
                issue_book()
            if choice==5:
                return_book()
            if choice==6:
                search_book()
            if choice == 7:
                add_student()
            if choice == 8:
                add_book()
            if choice == 9:
                delete_student()
            if choice == 10:
                delete_book()
            if choice == 11:
                update_book()
            if choice == 12:
                update_student()
            if choice == 13:
                view_available_books()
            if choice == 14:
                view_issued_books()
            if choice == 15:
                print("Exited sucessfully.")
                break
                
        
# view all students
def view_students():
    print("[ Schema: Student_id,  Student_name,  Department,  Email ]")
    cursor.execute("select * from students")
    for row in cursor.fetchall():
        print(row)
    print("\n")
        
# view all books
def view_books():
    print("[ Schema: Book_id,  Book_name,  Author,  Genre,  Status ]")
    cursor.execute("select * from books")
    for row in cursor.fetchall():
        print(row)
    print("\n")

# view all issuelogs
def issuelogs():
    print("[ Schema: student_id,  student_name,  book_id,  book_name,  issue_date,  return_date,  status ]")
    cursor.execute("""select i.student_id,s.name,i.book_id,b.title,i.issue_date,i.return_date,i.status 
                    from issuelogs i
                    join students s on i.student_id=s.student_id
                    join books b on i.book_id=b.book_id""")
    for row in cursor.fetchall():
        print(row)
        
# issue a book
def issue_book():
    """
    Issue a book only if it is currently marked as AVAILABLE.
    Updates both `issuelogs` and `books` in a single transaction.
    """
    # Show available books for quick reference
    view_available_books()

    stu_id  = input("Enter student id: ").strip()
    book_id = input("Enter book id: ").strip()

    # Make sure the book exists and is available
    cursor.execute("SELECT status FROM books WHERE book_id = %s", (book_id,))
    res = cursor.fetchone()
    if not res:
        print("Book ID not found")
        return
    if res[0].lower() != "available":
        print("Book is already issued or unavailable")
        return

    # Record issue + lock the book in a single commit
    try:
        cursor.execute("""
            INSERT INTO issuelogs (student_id, book_id, issue_date, status)
            VALUES (%s, %s, CURDATE(), 'issued')
        """, (stu_id, book_id))
        cursor.execute("""
            UPDATE books SET status = 'issued' WHERE book_id = %s
        """, (book_id,))
        conn.commit()
        print("Book issued successfully")
    except Exception as e:
        conn.rollback()
        print("Error issuing book:", e)

# return book
def return_book():
    """
    Return a book only if the selected issue record is still marked ISSUED.
    Marks the issue as RETURNED and the book as AVAILABLE.
    """
    print("[ Schema: issue_id,  student_name,  student_id,  book_name,  book_id,  issue_status ]")
    cursor.execute("""
        SELECT i.issue_id, s.name, i.student_id, b.title, i.book_id, i.status
        FROM issuelogs i
        JOIN students s ON i.student_id = s.student_id
        JOIN books   b ON i.book_id   = b.book_id
    """)
    for row in cursor.fetchall():
        print(row)
    print()

    issue_id = input("Enter issue_id to return: ").strip()

    # Confirm that this issue record exists and is still 'issued'
    cursor.execute("""
        SELECT book_id, status FROM issuelogs WHERE issue_id = %s
    """, (issue_id,))
    res = cursor.fetchone()
    if not res:
        print("Issue ID not found")
        return
    if res[1].lower() != "issued":
        print("This book has already been returned")
        return

    book_id = res[0]

    # Update both tables atomically
    try:
        cursor.execute("""
            UPDATE issuelogs
            SET return_date = CURDATE(), status = 'returned'
            WHERE issue_id = %s
        """, (issue_id,))
        cursor.execute("""
            UPDATE books SET status = 'available' WHERE book_id = %s
            """, (book_id,))
        conn.commit()
        print("Book returned successfully")
    except Exception as e:
        conn.rollback()
        print("Error returning book:", e)



# search book
def search_book():
    print("[ Schema:book_id,  book_title ]")
    cursor.execute("""select book_id,title from books""")
    for i in cursor.fetchall():
        print(i)
    query=input("Please enter your query:")
    cursor.execute(query)
    for i in cursor.fetchall():
        print("output-->:",i)
    print("\n")

# student registration
def add_student():
    print("Student Registration.")
    student_name=input("Enter student name:")
    department=input("Enter department:")
    email=input("Enter student Email:")
    try:
        cursor.execute("INSERT into students (name,department,email) values (%s,%s,%s)",(student_name,department,email))
        conn.commit()
        print(f"{student_name} student added sucessfully.")
    except Exception as e:
        print(e)
    print("\n")


# Add Book
def add_book():
    print("Book Registration.")
    book_name=input("Enter book name:")
    author=input("Enter book author:")
    genre=input("Enter book genre:")
    try:
        cursor.execute("INSERT into books (title,author,genre,status) values (%s,%s,%s,'available')",(book_name,author,genre))
        conn.commit()
        print(f"{book_name} book added sucessfully.")
    except Exception as e:
        print(e)

# delete student
def delete_student():
    print("Deleting Student.")
    cursor.execute("SELECT student_id,name,department from students")
    for i in cursor.fetchall():
        print(i)
    student_id=input("Enter student_id")
    try:
        cursor.execute("DELETE from students where student_id=%s",(student_id,))
        conn.commit()
        print("Student Deleted Succesfully.")
    except Exception as e:
        print(e)

# delete book
def delete_book():
    print("Deleting Book.")
    cursor.execute("SELECT book_id,title from books")
    for i in cursor.fetchall():
        print(i)
    book_id=input("Enter book_id:")
    try:
        cursor.execute("DELETE from books where book_id=%s",(book_id,))
        conn.commit()
        print("Book Deleted Sucessfully")
    except Exception as e:
        print(e)

# Update book information
def update_book():
    view_books()
    book_id = input("Enter the book ID to update: ")
    new_title = input("Enter new title: ")
    new_author = input("Enter new author: ")
    new_genre = input("Enter new genre: ")
    new_status = input("Enter new status (available/issued): ")
    try:
        cursor.execute("""
            UPDATE books
            SET title = %s, author = %s, genre = %s, status = %s
            WHERE book_id = %s
        """, (new_title, new_author, new_genre, new_status, book_id))
        conn.commit()
        print("Book updated successfully.\n")
    except Exception as e:
        print("Error while updating book:", e)

#update student information
def update_student():
    view_students()
    student_id = input("Enter the student ID to update: ")
    new_name = input("Enter new name: ")
    new_dept = input("Enter new department: ")
    new_email = input("Enter new email: ")
    try:
        cursor.execute("""
            UPDATE students
            SET name = %s, department = %s, email = %s
            WHERE student_id = %s
        """, (new_name, new_dept, new_email, student_id))
        conn.commit()
        print("Student updated successfully.\n")
    except Exception as e:
        print("Error while updating student:", e)

# available books
def view_available_books():
    print("[ Available Books ]")
    cursor.execute("SELECT * FROM books WHERE status = 'available'")
    for row in cursor.fetchall():
        print(row)
    print("\n")

# issued books
def view_issued_books():
    print("[ Issued Books ]")
    cursor.execute("""
        SELECT b.book_id, b.title, s.name, i.issue_date
        FROM books b
        JOIN issuelogs i ON b.book_id = i.book_id
        JOIN students s ON i.student_id = s.student_id
        WHERE i.status = 'issued'
    """)
    for row in cursor.fetchall():
        print(row)
    print("\n")

print("Welcome to Library Management System Admin Login")
if admin_login():
    main()
else:
    print("Exiting program.")

conn.close()
