# SchoolApp - Kivy Version (Part 1/5)
# This file initializes the Kivy app, sets up the main navigation, splash, and top-level screens.
# All settings, theming, and menu logic are included here.
# Make sure to add your school logo, splash image, and background in the assets/ directory.

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.core.window import Window
import os
import sqlite3

Window.size = (420, 800)  # For desktop testing

ASSETS_DIR = "assets"
SCHOOL_PHOTO_PATH = os.path.join(ASSETS_DIR, "school_photo.jpg")  # Replace with your image
APP_LOGO_PATH = os.path.join(ASSETS_DIR, "app_logo.png")         # Replace with your image
SPLASH_PATH = os.path.join(ASSETS_DIR, "splash.png")             # Replace with your image

class SplashScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class MenuPopup(Popup):
    pass

class ProfileScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

class PrivacyScreen(Screen):
    pass

class SchoolHistoryScreen(Screen):
    pass

class DashboardScreen(Screen):
    role = StringProperty("")
    username = StringProperty("")
    dashboard_img = StringProperty(SCHOOL_PHOTO_PATH)
    def on_pre_enter(self, *args):
        pass

class MyScreenManager(ScreenManager):
    pass

class SchoolApp(App):
    sm = ObjectProperty(None)

    def build(self):
        self.icon = APP_LOGO_PATH if os.path.exists(APP_LOGO_PATH) else None
        self.title = "SchoolApp"
        self.sm = Builder.load_file("screens.kv")
        return self.sm

    def show_menu(self):
        mp = MenuPopup()
        mp.open()

    def logout(self):
        self.sm.current = "login"

    def open_profile(self):
        self.sm.current = "profile"

    def open_about(self):
        self.sm.current = "about"

    def open_privacy(self):
        self.sm.current = "privacy"

    def open_school_history(self):
        self.sm.current = "school_history"

    def show_dashboard(self, role, username):
        dash_screen = self.sm.get_screen('dashboard')
        dash_screen.role = role
        dash_screen.username = username
        self.sm.current = "dashboard"

    def get_db(self):
        if not os.path.exists("school.db"):
            from db_schema import create_database
            create_database()
        return sqlite3.connect("school.db")

if __name__ == "__main__":
    SchoolApp().run()
