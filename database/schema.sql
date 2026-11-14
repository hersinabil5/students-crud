
-- Create the table used to store student information.

-- Remove the old table if it already exists.
DROP TABLE IF EXISTS students;

-- Create a new students table.
CREATE TABLE students (

    -- Automatically generates a unique ID for each student.
    student_id SERIAL PRIMARY KEY,

    -- First and last names are required.
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,

    -- Each student must have a different email address.
    email TEXT NOT NULL UNIQUE,

    -- Stores the enrollment date. This field is optional.
    enrollment_date DATE
);
