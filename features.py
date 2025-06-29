# features.py
# This file implements the main features for each role's dashboard.
# Each feature is a function that opens a popup or navigates to a screen.

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
import sqlite3

def show_info_popup(title, message):
    layout = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(16))
    layout.add_widget(Label(text=message, font_size=dp(15)))
    btn = Button(text="Close", size_hint_y=None, height=dp(40))
    layout.add_widget(btn)
    popup = Popup(title=title, content=layout, size_hint=(None, None), size=(dp(340), dp(280)))
    btn.bind(on_release=popup.dismiss)
    popup.open()

# ------------- ADMIN Features -------------

def manage_students():
    show_info_popup("Manage Students", "Add, view, edit, or delete students here.\n(Feature to be filled in detail.)")

def manage_teachers():
    show_info_popup("Manage Teachers", "Add, view, edit, or delete teachers here.\n(Feature to be filled in detail.)")

def manage_parents():
    show_info_popup("Manage Parents", "Add, view, edit, or delete parents here.\n(Feature to be filled in detail.)")

def manage_announcements():
    show_info_popup("Manage Announcements", "Add, view, or delete school announcements.")

def manage_events():
    show_info_popup("Manage Events", "Add or view school events.")

def manage_resources():
    show_info_popup("Manage Resources", "Add books, PDFs, and learning materials.")

def manage_fees():
    show_info_popup("Manage Fees", "Add/view fee notices for students.")

def manage_transport():
    show_info_popup("Manage Transport", "Add/view bus routes and drivers.")

def manage_cafeteria():
    show_info_popup("Manage Cafeteria", "Add/view menu items.")

def manage_clubs():
    show_info_popup("Manage Clubs", "Add/view clubs and activities.")

def manage_achievements():
    show_info_popup("Manage Achievements", "Add/view student awards and badges.")

def manage_emergency():
    show_info_popup("Manage Emergency Contacts", "Edit school emergency contact information.")

def manage_assignments():
    show_info_popup("Manage Assignments", "Review, edit, or delete assignments.")

# ------------- TEACHER Features -------------

def teacher_give_assignment():
    show_info_popup("Give Assignment", "Create and assign homework or tests to students.")

def teacher_view_assignments():
    show_info_popup("View Given Assignments", "See all assignments you have given.")

def teacher_attendance():
    show_info_popup("Attendance", "Mark and review student attendance.")

def teacher_timetable():
    show_info_popup("Timetable", "View your teaching timetable.")

def teacher_announcements():
    show_info_popup("Announcements", "See latest school announcements.")

def teacher_events():
    show_info_popup("Events", "See upcoming events.")

# ------------- STUDENT Features -------------

def student_timetable():
    show_info_popup("Timetable", "View your class timetable.")

def student_assignments():
    show_info_popup("Assignments", "See and answer assignments.")

def student_announcements():
    show_info_popup("Announcements", "See announcements for students.")

def student_events():
    show_info_popup("Events", "See school events.")

def student_resources():
    show_info_popup("Resources", "Access learning resources.")

def student_fees():
    show_info_popup("Fees", "View your fee payments and dues.")

def student_transport():
    show_info_popup("Transport", "See your assigned bus and route.")

def student_cafeteria():
    show_info_popup("Cafeteria", "See cafeteria menu.")

def student_clubs():
    show_info_popup("Clubs & Activities", "Join or view clubs.")

def student_achievements():
    show_info_popup("Achievements", "View your awards and badges.")

def student_emergency():
    show_info_popup("Emergency Info", "Access emergency contact info.")

def student_attendance():
    show_info_popup("Attendance", "See your attendance record.")

def student_marks():
    show_info_popup("Marks/Results", "View your test and exam results.")

# ------------- PARENT Features -------------

def parent_announcements():
    show_info_popup("Announcements", "See school announcements.")

def parent_events():
    show_info_popup("Events", "See school events.")

def parent_resources():
    show_info_popup("Resources", "Access school resources.")

def parent_fees():
    show_info_popup("Fees", "See your child's fees.")

def parent_transport():
    show_info_popup("Transport", "See your child's bus/route.")

def parent_clubs():
    show_info_popup("Clubs & Activities", "See your child's clubs.")

def parent_achievements():
    show_info_popup("Achievements", "See your child's awards.")

def parent_emergency():
    show_info_popup("Emergency Info", "Access emergency contacts.")

def parent_attendance():
    show_info_popup("Attendance", "See your child's attendance.")

def parent_marks():
    show_info_popup("Marks/Results", "See your child's results.")

# ------------- BUTTON MAPPINGS -------------

# These can be connected in your .kv files or dashboard setup routines

ADMIN_FEATURES = [
    ("Students", manage_students),
    ("Teachers", manage_teachers),
    ("Parents", manage_parents),
    ("Announcements", manage_announcements),
    ("Events", manage_events),
    ("Resources", manage_resources),
    ("Fees", manage_fees),
    ("Transport", manage_transport),
    ("Cafeteria", manage_cafeteria),
    ("Clubs", manage_clubs),
    ("Achievements", manage_achievements),
    ("Emergency", manage_emergency),
    ("Assignments", manage_assignments),
]

TEACHER_FEATURES = [
    ("Give Assignment", teacher_give_assignment),
    ("View Assignments", teacher_view_assignments),
    ("Attendance", teacher_attendance),
    ("Timetable", teacher_timetable),
    ("Announcements", teacher_announcements),
    ("Events", teacher_events),
]

STUDENT_FEATURES = [
    ("Timetable", student_timetable),
    ("Assignments", student_assignments),
    ("Announcements", student_announcements),
    ("Events", student_events),
    ("Resources", student_resources),
    ("Fees", student_fees),
    ("Transport", student_transport),
    ("Cafeteria", student_cafeteria),
    ("Clubs", student_clubs),
    ("Achievements", student_achievements),
    ("Emergency", student_emergency),
    ("Attendance", student_attendance),
    ("Marks", student_marks),
]

PARENT_FEATURES = [
    ("Announcements", parent_announcements),
    ("Events", parent_events),
    ("Resources", parent_resources),
    ("Fees", parent_fees),
    ("Transport", parent_transport),
    ("Clubs", parent_clubs),
    ("Achievements", parent_achievements),
    ("Emergency", parent_emergency),
    ("Attendance", parent_attendance),
    ("Marks", parent_marks),
]
