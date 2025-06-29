# app_glue.py
# Final Integration, role switching, and feature connection for SchoolApp (Kivy)
# This file glues together main.py, roles.py, features.py, and the .kv screens

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import sqlite3

from roles import (
    AdminDashboardScreen, TeacherDashboardScreen,
    StudentDashboardScreen, ParentDashboardScreen,
    ProfileScreen, AboutScreen, PrivacyScreen, SchoolHistoryScreen
)
from features import (
    ADMIN_FEATURES, TEACHER_FEATURES, STUDENT_FEATURES, PARENT_FEATURES
)
from utils import get_photo_path

# --- Role switching / login logic ---
def authenticate_user(username, password):
    db = App.get_running_app().get_db()
    c = db.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    db.close()
    return row[0] if row else None

def show_error(message):
    popup = Popup(title="Error", content=Label(text=message), size_hint=(None, None), size=(350, 200))
    popup.open()

def do_login(app, username, password):
    role = authenticate_user(username, password)
    if not role:
        show_error("Invalid username or password.")
        return
    if role == "admin":
        app.root.current = "admin_dashboard"
        app.root.get_screen("admin_dashboard").username = username
    elif role == "teacher":
        scr = app.root.get_screen("teacher_dashboard")
        scr.username = username
        app.root.current = "teacher_dashboard"
    elif role == "student":
        scr = app.root.get_screen("student_dashboard")
        scr.username = username
        app.root.current = "student_dashboard"
    elif role == "parent":
        scr = app.root.get_screen("parent_dashboard")
        scr.username = username
        app.root.current = "parent_dashboard"
    else:
        show_error("Unknown role: {}".format(role))

# --- Dashboard feature button connections ---
def add_feature_buttons(screen, features):
    # Dynamically clears and adds feature buttons for the dashboard
    grid = screen.ids.get('features_grid', None)
    if grid:
        grid.clear_widgets()
        for label, func in features:
            from kivy.uix.button import Button
            b = Button(text=label, size_hint_y=None, height=50)
            b.bind(on_release=lambda btn, f=func: f())
            grid.add_widget(b)

# --- Profile/About/Privacy/History navigation ---
def open_profile(app, role, username):
    scr = app.root.get_screen("profile")
    scr.role = role
    scr.username = username
    scr.on_pre_enter()
    app.root.current = "profile"

def open_about(app):
    app.root.current = "about"

def open_privacy(app):
    app.root.current = "privacy"

def open_school_history(app):
    app.root.current = "school_history"

# --- Error Handling and Feedback ---
def show_success(message):
    popup = Popup(title="Success", content=Label(text=message), size_hint=(None, None), size=(350, 200))
    popup.open()

# --- Example: Connect these in your main.py ---
# In your build() or after building the ScreenManager, call:
#   add_feature_buttons(sm.get_screen("admin_dashboard"), ADMIN_FEATURES)
#   add_feature_buttons(sm.get_screen("teacher_dashboard"), TEACHER_FEATURES)
#   add_feature_buttons(sm.get_screen("student_dashboard"), STUDENT_FEATURES)
#   add_feature_buttons(sm.get_screen("parent_dashboard"), PARENT_FEATURES)

# You can also connect the login button in your login screen:
#   Button(on_release=lambda: do_login(app, username_input.text, password_input.text))

# And connect menu options:
#   open_profile(app, role, username)
#   open_about(app)
#   open_privacy(app)
#   open_school_history(app)
