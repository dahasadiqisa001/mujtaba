# db_schema.py
# This file defines and creates the SQLite database schema for the SchoolApp Kivy app.
# It is safe to run multiple times (will not overwrite existing tables/data).

import sqlite3

def create_database(db_path="school.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Users table (for login)
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        photo TEXT
    )
    """)

    # Teachers table
    c.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        address TEXT,
        phone_number TEXT,
        email TEXT,
        section TEXT,
        class TEXT,
        education TEXT,
        photo TEXT
    )
    """)

    # Students table
    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        gender TEXT,
        dob TEXT,
        admission_date TEXT,
        address TEXT,
        email TEXT,
        section TEXT,
        class TEXT,
        parent_name TEXT,
        parent_phone TEXT,
        photo TEXT
    )
    """)

    # Parents table
    c.execute("""
    CREATE TABLE IF NOT EXISTS parents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_name TEXT,
        relationship TEXT,
        address TEXT,
        phone TEXT,
        email TEXT,
        occupation TEXT,
        workplace TEXT,
        emergency_name TEXT,
        emergency_phone TEXT,
        emergency_relationship TEXT,
        id_type TEXT,
        id_number TEXT,
        marital_status TEXT,
        language TEXT,
        custody TEXT,
        student_id INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    # Subjects table
    c.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class TEXT,
        section TEXT
    )
    """)

    # Timetable table
    c.execute("""
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class TEXT,
        section TEXT,
        day TEXT,
        period TEXT,
        start_time TEXT,
        end_time TEXT,
        subject_id INTEGER,
        teacher_username TEXT
    )
    """)

    # Marks table
    c.execute("""
    CREATE TABLE IF NOT EXISTS marks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        exam_name TEXT,
        marks INTEGER,
        max_marks INTEGER,
        date TEXT
    )
    """)

    # Attendance (students)
    c.execute("""
    CREATE TABLE IF NOT EXISTS student_attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    # Announcements
    c.execute("""
    CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        message TEXT,
        audience TEXT
    )
    """)

    # Events
    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        description TEXT
    )
    """)

    # Resources
    c.execute("""
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        type TEXT,
        location TEXT
    )
    """)

    # Fees
    c.execute("""
    CREATE TABLE IF NOT EXISTS fees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        amount_due TEXT,
        due_date TEXT
    )
    """)

    # Transport
    c.execute("""
    CREATE TABLE IF NOT EXISTS transport (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route TEXT,
        bus_number TEXT,
        driver TEXT
    )
    """)

    # Cafeteria
    c.execute("""
    CREATE TABLE IF NOT EXISTS cafeteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        category TEXT,
        price TEXT
    )
    """)

    # Clubs
    c.execute("""
    CREATE TABLE IF NOT EXISTS clubs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        supervisor TEXT,
        description TEXT
    )
    """)

    # Achievements
    c.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        title TEXT,
        description TEXT
    )
    """)

    # Emergency Contacts
    c.execute("""
    CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        role TEXT
    )
    """)

    # Assignments
    c.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_username TEXT,
        subject TEXT,
        title TEXT,
        description TEXT,
        class TEXT,
        section TEXT,
        due_date TEXT,
        mark INTEGER,
        questions TEXT
    )
    """)

    # Assignment Submissions
    c.execute("""
    CREATE TABLE IF NOT EXISTS assignment_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER,
        student_id INTEGER,
        answer TEXT,
        submitted_on TEXT,
        mark_obtained INTEGER,
        feedback TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created and initialized.")
