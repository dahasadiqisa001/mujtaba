# roles.py
# Contains role-based dashboard logic and navigation for SchoolApp (Kivy)

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty
from kivy.app import App
import sqlite3

from utils import get_photo_path

class AdminDashboardScreen(Screen):
    username = StringProperty("")
    photo = StringProperty("")
    def on_pre_enter(self):
        # Fetch admin profile info if needed
        pass

class TeacherDashboardScreen(Screen):
    username = StringProperty("")
    photo = StringProperty("")
    teacher_name = StringProperty("")
    def on_pre_enter(self):
        db = App.get_running_app().get_db()
        c = db.cursor()
        c.execute("SELECT name, photo FROM teachers WHERE username=?", (self.username,))
        row = c.fetchone()
        self.teacher_name = row[0] if row else self.username
        self.photo = get_photo_path(row[1]) if row and row[1] else "assets/default_photo.png"
        db.close()

class StudentDashboardScreen(Screen):
    username = StringProperty("")
    student_id = StringProperty("")
    photo = StringProperty("")
    student_name = StringProperty("")
    def on_pre_enter(self):
        db = App.get_running_app().get_db()
        c = db.cursor()
        c.execute("SELECT id, name, photo FROM students WHERE name=?", (self.username,))
        row = c.fetchone()
        if row:
            self.student_id = str(row[0])
            self.student_name = row[1]
            self.photo = get_photo_path(row[2])
        db.close()

class ParentDashboardScreen(Screen):
    username = StringProperty("")
    parent_id = StringProperty("")
    student_name = StringProperty("")
    def on_pre_enter(self):
        db = App.get_running_app().get_db()
        c = db.cursor()
        c.execute("SELECT id, parent_name, student_id FROM parents WHERE parent_name=?", (self.username,))
        row = c.fetchone()
        if row:
            self.parent_id = str(row[0])
            sid = row[2]
            c.execute("SELECT name FROM students WHERE id=?", (sid,))
            srow = c.fetchone()
            self.student_name = srow[0] if srow else ""
        db.close()

# Profile/About/Privacy/History screens
class ProfileScreen(Screen):
    role = StringProperty("")
    username = StringProperty("")
    info = ObjectProperty({})
    def on_pre_enter(self):
        db = App.get_running_app().get_db()
        c = db.cursor()
        if self.role == "admin":
            c.execute("SELECT username, photo FROM users WHERE username=?", (self.username,))
            row = c.fetchone()
            self.info = {"Username": row[0], "Role": "Admin"}
        elif self.role == "teacher":
            c.execute("SELECT name, email, phone_number, address, section, class FROM teachers WHERE username=?", (self.username,))
            row = c.fetchone()
            self.info = {
                "Name": row[0], "Email": row[1], "Phone": row[2],
                "Address": row[3], "Section": row[4], "Class": row[5]}
        elif self.role == "student":
            c.execute("SELECT name, dob, class, section, parent_name, parent_phone FROM students WHERE name=?", (self.username,))
            row = c.fetchone()
            self.info = {
                "Name": row[0], "DOB": row[1], "Class": row[2], "Section": row[3],
                "Parent": row[4], "Parent Phone": row[5]}
        elif self.role == "parent":
            c.execute("SELECT parent_name, phone, address FROM parents WHERE parent_name=?", (self.username,))
            row = c.fetchone()
            self.info = {
                "Name": row[0], "Phone": row[1], "Address": row[2]}
        db.close()

class AboutScreen(Screen):
    pass

class PrivacyScreen(Screen):
    pass

class SchoolHistoryScreen(Screen):
    pass
