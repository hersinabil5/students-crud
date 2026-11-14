# Student Database - PostgreSQL CRUD Application

A simple Python application that connects to a PostgreSQL database and lets users manage student records. It supports adding, viewing, updating, and deleting students through a command-line menu.

## Demonstration Video

**Video link:** [Add YouTube or Vimeo link here]

## Project Structure

```text
students-crud/
├── database/
│   ├── schema.sql
│   └── seed.sql
├── app/
│   ├── students_app.py
│   └── requirements.txt
└── README.md
```

## Requirements

- PostgreSQL
- pgAdmin 4 (optional, for managing the database)
- Python 3.8 or newer

## 1. Setting Up the Database

First, create a database called `student_db`.

Using pgAdmin:

1. Open pgAdmin and right-click **Databases**.
2. Select **Create → Database**.
3. Enter `student_db` as the database name.
4. Open the Query Tool for the new database.
5. Run the contents of `database/schema.sql`.
6. Run `database/seed.sql` to add the sample students.

You can check that the records were added by running:

```sql
SELECT * FROM students;
```

You can also set everything up using the terminal:

```bash
createdb student_db
psql -d student_db -f database/schema.sql
psql -d student_db -f database/seed.sql
```

### Table Structure

| Column          | Type                 | Description                |
| --------------- | -------------------- | -------------------------- |
| student_id      | SERIAL PRIMARY KEY   | Automatically generated ID |
| first_name      | TEXT NOT NULL        | Student's first name       |
| last_name       | TEXT NOT NULL        | Student's last name        |
| email           | TEXT NOT NULL UNIQUE | Student's email address    |
| enrollment_date | DATE                 | Date the student enrolled  |

## 2. Installing and Running

Open a terminal in the project folder and run:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, activate the environment with:

```bash
venv\Scripts\activate
```

Install the required package:

```bash
pip install -r app/requirements.txt
```

Start the application:

```bash
python3 app/students_app.py
```

### Database Connection

The database connection settings are defined near the top of `students_app.py`.

| Setting  | Default      |
| -------- | ------------ |
| Database | `student_db` |
| User     | `nabilhersi` |
| Password | Empty        |
| Host     | `localhost`  |
| Port     | `5432`       |

These settings can also be changed using environment variables.

For example:

```bash
DB_USER=postgres DB_PASSWORD=yourpassword python3 app/students_app.py
```

## 3. Using the Application

When the program starts, a menu appears with the following options:

```text
1. View all students
2. Add a student
3. Update a student's email
4. Delete a student
5. Exit
```

Select an option by entering its corresponding number. The application will ask for the information needed to complete the selected operation.

## Functions

| Function                                                    | Operation | What it does                                               |
| ----------------------------------------------------------- | --------- | ---------------------------------------------------------- |
| `getAllStudents()`                                          | READ      | Displays all students, ordered by their ID.                |
| `addStudent(first_name, last_name, email, enrollment_date)` | CREATE    | Adds a new student and displays their generated ID.        |
| `updateStudentEmail(student_id, new_email)`                 | UPDATE    | Changes the email address for a student with the given ID. |
| `deleteStudent(student_id)`                                 | DELETE    | Deletes a student using their ID.                          |

## Error Handling

The application handles a few common errors:

- **SQL injection:** Uses parameterized queries with `%s` placeholders.
- **Duplicate emails:** Prevents duplicate email addresses and displays an error message.
- **Missing information:** Handles missing required fields.
- **Invalid dates:** Catches invalid date inputs.
- **Student not found:** Checks whether a student exists before updating or deleting.
- **Database connection:** Displays an error if the application cannot connect to PostgreSQL.
