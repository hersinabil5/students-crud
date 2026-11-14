
"""
students_app.py

This program connects to a PostgreSQL database and allows users
to view, add, update, and delete student records.
"""

import os
import sys

import psycopg2
from psycopg2 import errors


# Database connection settings.
# Environment variables can be used to change these values.
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "student_db"),
    "user": os.getenv("DB_USER", "nabilhersi"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432"))
}


# Opens a connection to the PostgreSQL database.
def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# READ: Gets all students from the database and displays them.
def getAllStudents():
    query = """
        SELECT student_id, first_name, last_name, email, enrollment_date
        FROM students
        ORDER BY student_id;
    """

    # Run the query and get all the student records.
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                students = cur.fetchall()

    except psycopg2.Error as e:
        print(f"Error retrieving students: {e}")
        return []

    # Check if there are any students to display.
    if not students:
        print("No students found.")
        return []

    # Print the student information in columns.
    header = f"{'ID':<4} {'First Name':<12} {'Last Name':<12} {'Email':<30} {'Enrolled':<10}"
    print(header)
    print("-" * len(header))

    for student in students:
        student_id, first, last, email, enrolled = student
        print(f"{student_id:<4} {first:<12} {last:<12} {email:<30} {str(enrolled):<10}")

    return students


# CREATE: Adds a new student to the database.
def addStudent(first_name, last_name, email, enrollment_date):
    query = """
        INSERT INTO students (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s)
        RETURNING student_id;
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Use None for empty fields so they are stored as NULL.
                cur.execute(query, (
                    first_name or None,
                    last_name or None,
                    email or None,
                    enrollment_date or None
                ))

                # Get the ID assigned to the new student.
                new_id = cur.fetchone()[0]

        print(f"Student added with student_id = {new_id}.")
        return new_id

    # Handle cases where the email is already in the database.
    except errors.UniqueViolation:
        print(f"Error: the email '{email}' is already in use.")

    # Make sure required fields have been entered.
    except errors.NotNullViolation:
        print("Error: first name, last name and email are required.")

    # Handle dates that are not in the correct format.
    except (errors.InvalidDatetimeFormat, errors.DatetimeFieldOverflow):
        print("Error: enrollment date must be in YYYY-MM-DD format.")

    # Handle any other database errors.
    except psycopg2.Error as e:
        print(f"Error adding student: {e}")

    return None


# UPDATE: Changes the email address of an existing student.
def updateStudentEmail(student_id, new_email):
    query = "UPDATE students SET email = %s WHERE student_id = %s;"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (new_email, student_id))

                # Check how many student records were updated.
                updated = cur.rowcount

        if updated > 0:
            print(f"Email for student {student_id} updated to {new_email}.")
        else:
            print(f"No student found with student_id = {student_id}.")

        return updated

    # Handle cases where another student already has this email.
    except errors.UniqueViolation:
        print(f"Error: the email '{new_email}' is already in use.")

    except psycopg2.Error as e:
        print(f"Error updating email: {e}")

    return 0


# DELETE: Removes a student from the database using their ID.
def deleteStudent(student_id):
    query = "DELETE FROM students WHERE student_id = %s;"

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (student_id,))

                # Check if a student was actually deleted.
                deleted = cur.rowcount

        if deleted > 0:
            print(f"Student {student_id} deleted.")
        else:
            print(f"No student found with student_id = {student_id}.")

        return deleted

    except psycopg2.Error as e:
        print(f"Error deleting student: {e}")

    return 0


# Keeps asking the user for a number until a valid integer is entered.
def ask_int(prompt):
    while True:
        value = input(prompt).strip()

        if value.isdigit():
            return int(value)

        print("Please enter a valid number.")


# Main menu where the user chooses which operation to perform.
def main():

    # Check the database connection before showing the menu.
    try:
        get_connection().close()
    except psycopg2.Error as e:
        print(f"Could not connect to the database: {e}")
        sys.exit(1)

    menu = """
===== Student Database =====
1. View all students
2. Add a student
3. Update a student's email
4. Delete a student
5. Exit
"""

    # Keep showing the menu until the user chooses to exit.
    while True:
        print(menu)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            getAllStudents()

        elif choice == "2":
            # Ask for the information needed to add a student.
            first = input("First name: ").strip()
            last = input("Last name: ").strip()
            email = input("Email: ").strip()
            date = input("Enrollment date (YYYY-MM-DD, blank for none): ").strip()

            addStudent(first, last, email, date)

        elif choice == "3":
            # Get the student's ID and their new email address.
            sid = ask_int("Student ID: ")
            new_email = input("New email: ").strip()

            updateStudentEmail(sid, new_email)

        elif choice == "4":
            # Ask which student should be removed.
            sid = ask_int("Student ID to delete: ")
            deleteStudent(sid)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-5.")


# Start the program when this file is run.
if __name__ == "__main__":
    main()
