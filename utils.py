# utils.py
# Utility functions for SchoolApp

import os

def get_photo_path(user_photo, default="assets/default_photo.png"):
    """Returns the path to a user's photo or a default image."""
    if user_photo and os.path.exists(user_photo):
        return user_photo
    return default

def get_school_photo():
    """Returns the school photo path or a placeholder."""
    path = "assets/school_photo.jpg"
    if os.path.exists(path):
        return path
    return "assets/default_school_photo.png"
