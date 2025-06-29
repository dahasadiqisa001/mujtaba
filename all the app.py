import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import datetime
from PIL import Image, ImageTk
import shutil
import datetime

def create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

class RoundedFrame(tk.Frame):
    def __init__(self, parent, width=800, height=650, bg="#e3f2fd", border_color="#1976d2", radius=25, **kwargs):
        super().__init__(parent, bg=bg, **kwargs)
        self.width = width
        self.height = height
        self.radius = radius
        self.bg = bg
        self.border_color = border_color

        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0, bg=bg)
        self.canvas.pack(fill="both", expand=True)
        self.rounded_rect = create_rounded_rect(
            self.canvas, 5, 5, width-5, height-5, radius=radius,
            fill=bg, outline=border_color, width=3
        )
        self.inner = tk.Frame(self.canvas, bg=bg)
        self.inner.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

class SchoolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School App")
        self.root.geometry("900x900")
        self.primary = "#1976d2"
        self.secondary = "#42a5f5"
        self.accent = "#e3f2fd"
        self.bg_main = "#bbdefb"
        self.success = "#2e7d32"
        self.danger = "#c62828"

        # Feature data
        self.assignments = []
        self.notices = []
        self.messages = []
        self.clubs = []
        self.events = []
        self.resources = []
        self.fees = []
        self.buses = []
        self.cafeteria_menu = []
        self.forums = []
        self.achievements = []
        self.reminders = []
        self.exams = []
        self.languages = ['English', 'Arabic', 'French', 'Spanish']


        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background=self.accent, font=("Segoe UI", 13))
        style.configure("TButton", font=("Segoe UI", 13), padding=6)
        style.configure("TEntry", font=("Segoe UI", 13))
        style.configure("Treeview", font=("Segoe UI", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Segoe UI", 13, "bold"), background=self.primary, foreground="white")
        style.map("TButton",
            background=[('active', self.secondary), ('!active', self.primary)],
            foreground=[('active', 'black'), ('!active', 'white')]
        )

        # Main canvas & frame
        self.canvas = tk.Canvas(self.root, width=700, height=900, bg="#bbdefb", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.root, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_frame = tk.Frame(self.canvas, bg="#87CEEB", width=700, height=1400)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor='nw')
        self.main_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Notebook as main section inside the scrollable frame
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(pady=10, fill="both", expand=True)
        self.options_frame = RoundedFrame(self.notebook, width=600, height=820, bg="#f5faff", border_color=self.secondary, radius=20)
        self.notebook.add(self.options_frame, text="Options")
        self.select_options()


    def create_database(self):
        import sqlite3
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    admission_date TEXT NOT NULL,
                    address TEXT NOT NULL,
                    email TEXT,
                    section TEXT NOT NULL,
                    class TEXT NOT NULL,
                    parent_name TEXT NOT NULL,
                    parent_phone TEXT NOT NULL,
                    photo TEXT
                )
            """)
            # Parents table
            c.execute("""
                CREATE TABLE IF NOT EXISTS parents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    parent_name TEXT NOT NULL,
                    relationship TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    occupation TEXT,
                    workplace TEXT,
                    emergency_name TEXT NOT NULL,
                    emergency_phone TEXT NOT NULL,
                    emergency_relationship TEXT,
                    id_type TEXT,
                    id_number TEXT,
                    marital_status TEXT,
                    language TEXT,
                    custody TEXT,
                    student_id INTEGER NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )
            """)
            # Student attendance table
            c.execute("""
                CREATE TABLE IF NOT EXISTS student_attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    date TEXT,
                    status TEXT,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )
            """)
            # Teachers table
            c.execute("""
                CREATE TABLE IF NOT EXISTS teachers (
                    username TEXT,
                    name TEXT,
                    address TEXT,
                    phone_number TEXT,
                    email TEXT,
                    section TEXT,
                    class TEXT,
                    education TEXT,
                    photo TEXT,
                    username TEXT
                )
            """)
            # Users table
            c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    role TEXT,
                    photo TEXT
                )
            """)
            # Teacher attendance table
            c.execute("""
                CREATE TABLE IF NOT EXISTS teacher_attendance (
                    name TEXT,
                    class TEXT,
                    attendance TEXT
                )
            """)
            # Subjects table
            c.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    class TEXT,
                    section TEXT
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
                    date TEXT,
                    FOREIGN KEY(student_id) REFERENCES students(id),
                    FOREIGN KEY(subject_id) REFERENCES subjects(id)
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
                    teacher_username TEXT,
                    FOREIGN KEY(subject_id) REFERENCES subjects(id),
                    FOREIGN KEY(teacher_username) REFERENCES teachers(username)
                )
            """)
            # Profile updates table
            c.execute("""
                CREATE TABLE IF NOT EXISTS profile_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    field_name TEXT,
                    old_value TEXT,
                    new_value TEXT,
                    date TEXT,
                    approved INTEGER DEFAULT 0
                )
            """)
            # Announcements table
            c.execute("""
                CREATE TABLE IF NOT EXISTS announcements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    message TEXT,
                    audience TEXT
                )
            """)
            c.execute("DROP TABLE IF EXISTS events;")
            c.execute("""
                CREATE TABLE events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    date TEXT,
                    description TEXT
                );
            """)
            # Resources table
            c.execute("""
                CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    type TEXT,
                    location TEXT
                )
            """)
            # Fees table
            c.execute("""
                CREATE TABLE IF NOT EXISTS fees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    amount_due TEXT,
                    due_date TEXT,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )
            """)
            # Transport table
            c.execute("""
                CREATE TABLE IF NOT EXISTS transport (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    route TEXT,
                    bus_number TEXT,
                    driver TEXT
                )
            """)
            # Cafeteria table
            c.execute("""
                CREATE TABLE IF NOT EXISTS cafeteria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT,
                    category TEXT,
                    price TEXT
                )
            """)
            # Clubs table
            c.execute("""
                CREATE TABLE IF NOT EXISTS clubs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    supervisor TEXT,
                    description TEXT
                )
            """)
            # Achievements table
            c.execute("""
                CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    title TEXT,
                    description TEXT,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                )
            """)
            # Emergency contacts table
            c.execute("""
                CREATE TABLE IF NOT EXISTS emergency_contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    role TEXT
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher TEXT,
                    subject TEX T,
                    title TEXT,
                    description TEXT,
                    class TEXT,
                    section TEXT,
                    due_date TEXT,
                    model_answer TEXT,
                    mark INTEGER
                )
            """)
            c.execute("""
                CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    name TEXT,
                    class TEXT,
                    section TEXT
                )
                """)
        # Subjects
        c.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    class TEXT,
                    section TEXT
                )
                """)
        # Students
        c.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    class TEXT,
                    section TEXT
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
        c.execute("""
                CREATE TABLE IF NOT EXISTS assignment_submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assignment_id INTEGER,
                    student_id INTEGER,
                    answer TEXT,
                    submitted_on TEXT,
                    mark_obtained INTEGER,
                    feedback TEXT,
                    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
                    FOREIGN KEY (student_id) REFERENCES students(id)
                )
                """)
        conn.commit()
        
    def clear_options(self):
        for widget in self.options_frame.inner.winfo_children():
            widget.destroy()

    def select_options(self):
        self.clear_options()
        frame = self.options_frame.inner
        title = tk.Label(
            frame,
            text="Welcome to School App",
            font=("Segoe UI", 22, "bold"),
            fg=self.primary,
            bg="#f5faff"
        )
        title.pack(pady=(40,10))
        btn_style = {"width": 22, "height": 2, "font": ("Segoe UI", 13), "bg": self.primary, "fg": "white", "bd": 0, "activebackground": self.secondary}
        tk.Button(frame, text="Show All Roles", command=self.show_all_roles_frame, **btn_style).pack(pady=18)
        tk.Button(frame, text="School Info", command=self.school_info, **btn_style).pack(pady=18)
        tk.Button(frame, text="Responsibilities", command=self.responsibilities, **btn_style).pack(pady=18)
        tk.Button(frame, text="Daily Azkaar", command=self.daily_azkaar, **btn_style).pack(pady=18)
        tk.Button(frame, text="Quiz Game", command=self.quiz_game, **btn_style).pack(pady=18)

    def school_info(self):
        self.clear_options()
        frame = self.options_frame.inner
        tk.Label(frame, text="School Name:", bg="#f5faff", font=("Segoe UI", 14, "bold")).pack(pady=(15, 3))
        tk.Label(frame, text="مدرسة تهذيب الأطفال والغلمان في التأديب وقراءة القرءان", bg="#f5faff", font=("Arial Unicode MS", 14)).pack(pady=2)
        tk.Label(frame, text="Address: no. 307 Kofar Mata", bg="#f5faff", font=("Segoe UI", 13)).pack(pady=2)
        tk.Label(frame, text="Contact: 08158881499", bg="#f5faff", font=("Segoe UI", 13)).pack(pady=2)
        tk.Label(frame, text="Motto: Get Qur'an memorization after graduate school", bg="#f5faff", font=("Segoe UI", 13, "italic")).pack(pady=2)
        tk.Label(frame, text="Get best certificate", bg="#f5faff", font=("Segoe UI", 13)).pack(pady=2)
        tk.Button(frame, text="Back", command=self.select_options, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=15)

    def responsibilities(self):
        self.clear_options()
        frame = self.options_frame.inner
        tk.Label(frame, text="Responsibilities", bg="#C9E4CA", font=("Arial", 18)).pack(pady=20)
        tk.Label(frame, text="* Students: Attend classes regularly, Complete homework and assignments", bg="#C9E4CA", font=("Arial", 14)).pack()
        tk.Label(frame, text="* Teachers: Teach students, Prepare lesson plans, Assess student performance", bg="#C9E4CA", font=("Arial", 14)).pack()
        tk.Button(frame, text="Back", command=self.select_options).pack()

    def daily_azkaar(self):
        self.clear_options()
        frame = self.options_frame.inner
        tk.Label(frame, text="Daily Azkaar", bg="#F7D2C4", font=("Arial", 18)).pack(pady=20)
        tk.Label(frame, text="* Morning Azkaar: Subhanallah wa bihamdihi, Alhamdulillah", bg="#F7D2C4", font=("Arial", 14)).pack()
        tk.Label(frame, text="* Evening Azkaar: Astaghfirullah, Allahumma inni as'alukal jannah", bg="#F7D2C4", font=("Arial", 14)).pack()
        tk.Button(frame, text="Back", command=self.select_options).pack()

    def quiz_game(self):
        self.clear_options()
        # Remove any previous quiz_game_frame tab if exists
        for idx in range(len(self.notebook.tabs())):
            if self.notebook.tab(idx, "text") == "Quiz Game":
                self.notebook.forget(idx)
                break
        self.quiz_game_frame = tk.Frame(self.notebook, bg="#6495ED")
        self.notebook.add(self.quiz_game_frame, text="Quiz Game")
        self.notebook.select(self.quiz_game_frame)
        tk.Label(self.quiz_game_frame, text="Quiz Game", bg="#6495ED", font=("Arial", 24, "bold")).pack(pady=50)
        self.questions = [ 
            {"question": "What is the holy book of Islam?", "options": ["Quran", "Bible", "Torah"], "answer": "Quran"},
            {"question": "Who is the prophet of Islam?", "options": ["Muhammad", "Jesus", "Moses"], "answer": "Muhammad"},
            {"question": "What is the direction of prayer in Islam?", "options": ["Qibla", "East", "West"], "answer": "Qibla"},
            {"question": "What is the Islamic greeting?", "options": ["As-salamu alaykum", "Hello", "Goodbye"], "answer": "As-salamu alaykum"},
            {"question": "What is the name of the Islamic month of fasting?", "options": ["Ramadan", "Shawwal", "Dhu al-Hijjah"], "answer": "Ramadan"},
            {"question": "Who is the father of Prophet Muhammad?", "options": ["Abdullah", "Abu Talib", "Abd al-Muttalib"], "answer": "Abdullah"},
            {"question": "What is the name of the first wife of Prophet Muhammad?", "options": ["Khadijah", "Aisha", "Fatima"], "answer": "Khadijah"},
            {"question": "What is the Islamic term for charity?", "options": ["Zakat", "Sadaqah", "Hajj"], "answer": "Zakat"},
            {"question": "What is the name of the night journey of Prophet Muhammad?", "options": ["Isra' wal-Mi'raj", "Hijra", "Jihad"], "answer": "Isra' wal-Mi'raj"},
            {"question": "Who is the angel that revealed the Quran to Prophet Muhammad?", "options": ["Jibril", "Mikail", "Israfil"], "answer": "Jibril"},
            {"question": "What is the name of the Islamic pilgrimage to Mecca?", "options": ["Hajj", "Umrah", "Ziyarah"], "answer": "Hajj"},
            {"question": "What is the Islamic term for the struggle or striving?", "options": ["Jihad", "Qital", "Riba"], "answer": "Jihad"},
            {"question": "What is the name of the first month in the Islamic calendar?", "options": ["Muharram", "Safar", "Rabi' al-awwal"], "answer": "Muharram"},
            {"question": "Who is the companion of Prophet Muhammad that was known for his generosity?", "options": ["Abu Bakr", "Umar", "Uthman"], "answer": "Uthman"},
            {"question": "What is the Islamic term for the morning prayer?", "options": ["Fajr", "Dhuhr", "Asr"], "answer": "Fajr"},
            {"question": "Who is the companion of Prophet Muhammad that was known for his bravery?", "options": ["Ali", "Hamza", "Abu Bakr"], "answer": "Hamza"},
            {"question": "What is the Islamic term for the evening prayer?", "options": ["Maghrib", "Makkah", "Madina"], "answer": "Maghrib"}
        ]
        self.current_question = 0
        self.score = 0
        self.display_question()

    def display_question(self):
        for widget in self.quiz_game_frame.winfo_children():
            widget.destroy()
        question_frame = tk.Frame(self.quiz_game_frame, bg="#6495ED")
        question_frame.pack(pady=10)
        tk.Label(question_frame, text=f"Question {self.current_question + 1}: {self.questions[self.current_question]['question']}", bg="#6495ED", font=("Arial", 18), wraplength=400).pack()
        for i, option in enumerate(self.questions[self.current_question]['options']):
            tk.Button(question_frame, text=f"{i+1}. {option}", bg="#4CAF50", fg="#ffffff", font=("Arial", 16), width=20, command=lambda option=option: self.check_answer(option)).pack(pady=5)
        tk.Button(self.quiz_game_frame, text="Back", bg="#4CAF50", fg="#ffffff", font=("Arial", 16), width=10, command=self.select_options).pack(pady=10)

    def check_answer(self, answer):
        if answer == self.questions[self.current_question]['answer']:
            self.score += 5
        self.next_question()

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display_question()
        else:
            result_window = tk.Toplevel(self.root)
            result_window.title("Quiz Result")
            result_window.geometry("400x200")
            tk.Label(result_window, text=f"Quiz completed! Your final score is {self.score} out of {len(self.questions) * 5}", font=("Arial", 18)).pack(pady=20)
            
    def show_all_roles_frame(self):
        self.clear_options()
        container = tk.Frame(self.options_frame.inner, bg="#f5faff")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        admin_frame = tk.LabelFrame(container, text="Admin", font=("Segoe UI", 14, "bold"), bg="#e3f2fd", fg=self.primary, labelanchor='n')
        teacher_frame = tk.LabelFrame(container, text="Teacher", font=("Segoe UI", 14, "bold"), bg="#e8f5e9", fg=self.primary, labelanchor='n')
        student_frame = tk.LabelFrame(container, text="Student", font=("Segoe UI", 14, "bold"), bg="#fffde7", fg=self.primary, labelanchor='n')
        parent_frame = tk.LabelFrame(container, text="Parent", font=("Segoe UI", 14, "bold"), bg="#fce4ec", fg=self.primary, labelanchor='n')
        admin_frame.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        teacher_frame.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        student_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        parent_frame.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        tk.Label(admin_frame, text="Manage Teachers", bg="#e3f2fd", font=("Segoe UI", 12)).pack(pady=3)
        tk.Label(admin_frame, text="Manage Students", bg="#e3f2fd", font=("Segoe UI", 12)).pack(pady=3)
        tk.Label(admin_frame, text="Manage Parents", bg="#e3f2fd", font=("Segoe UI", 12)).pack(pady=3)
        tk.Button(admin_frame, text="Admin Login", command=self.admin_login, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=5)
        tk.Label(teacher_frame, text="Mark Attendance", bg="#e8f5e9", font=("Segoe UI", 12)).pack(pady=3)
        tk.Label(teacher_frame, text="View Timetable", bg="#e8f5e9", font=("Segoe UI", 12)).pack(pady=3)
        tk.Label(teacher_frame, text="View Gradebook", bg="#e8f5e9", font=("Segoe UI", 12)).pack(pady=3)
        tk.Button(teacher_frame, text="Teacher Login", command=self.teacher_login, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=5)
        tk.Label(student_frame, text="View Attendance", bg="#fffde7", font=("Segoe UI", 12)).pack(pady=3)
        tk.Label(student_frame, text="View Gradebook", bg="#fffde7", font=("Segoe UI", 12)).pack(pady=3)
        tk.Label(student_frame, text="View Timetable", bg="#fffde7", font=("Segoe UI", 12)).pack(pady=3)
        tk.Button(student_frame, text="Student Login", command=self.student_login, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=5)
        tk.Label(parent_frame, text="View Child's Attendance", bg="#fce4ec", font=("Segoe UI", 12)).pack(pady=3)
        tk.Button(parent_frame, text="Parent Login", command=self.parent_login, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=5)
        tk.Button(container, text="Back", command=self.select_options, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").grid(row=2, column=0, columnspan=2, pady=10)

    # --- Admin Login ---
    def admin_login(self):
        self.clear_options()
        font = ('Segoe UI', 16)
        tk.Label(self.options_frame.inner, text="Username:", font=font, bg="#f5faff").pack(pady=10)
        username_entry = ttk.Entry(self.options_frame.inner, font=font, width=30)
        username_entry.pack(ipady=5, pady=10)
        tk.Label(self.options_frame.inner, text="Password:", font=font, bg="#f5faff").pack(pady=10)
        password_entry = ttk.Entry(self.options_frame.inner, font=font, width=30, show="*")
        password_entry.pack(ipady=5, pady=10)
        show_password_var = tk.IntVar()
        def toggle_password():
            password_entry.config(show="" if show_password_var.get() else "*")
        tk.Checkbutton(self.options_frame.inner, text="Show Password", variable=show_password_var, command=toggle_password, bg="#f5faff").pack()
        def check_admin():
            username = username_entry.get()
            password = password_entry.get()
            if username == 'AHMAD ISA TIJJANI' and password == 'AHMADISA':
                self.admin_dashboard()
            else:
                messagebox.showerror("Invalid Credentials", "Username or password is incorrect")
        tk.Button(self.options_frame.inner, height=2, width=28, text="Login", command=check_admin, bg=self.primary, fg="white", font=font, bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, height=2, width=28, text="Menu", command=self.select_options, bg="#9e9e9e", fg="white", font=font, bd=0, activebackground="#bdbdbd").pack(pady=7)

    # --- Teacher Login/Dashboard ---
    def teacher_login(self):
        self.clear_options()
        font = ('Segoe UI', 14)
        tk.Label(self.options_frame.inner, text="Username:", font=font, bg="#f5faff").pack(pady=10)
        username_entry = ttk.Entry(self.options_frame.inner, font=font, width=30)
        username_entry.pack(pady=10)
        tk.Label(self.options_frame.inner, text="Password:", font=font, bg="#f5faff").pack(pady=10)
        password_entry = ttk.Entry(self.options_frame.inner, font=font, width=30, show="*")
        password_entry.pack(pady=10)
        def check_teacher():
            username = username_entry.get()
            password = password_entry.get()
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=? AND password=? AND role='teacher'", (username, password))
                teacher = c.fetchone()
            if teacher:
                self.logged_in_teacher = username
                self.teacher_dashboard()
            else:
                messagebox.showerror("Invalid Credentials", "Username or password is incorrect")
        tk.Button(self.options_frame.inner, text="Login", command=check_teacher, width=20, height=2, font=font, bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Menu", command=self.select_options, width=20, height=2, font=font, bg="#9e9e9e", fg="white", bd=0, activebackground="#bdbdbd").pack(pady=10)

    # --- Teacher Dashboard ---
    def teacher_dashboard(self):
        self.clear_options()
        # Fetch teacher info from DB
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT name, username, section, class, photo, education
                FROM teachers
                WHERE username=?
            """, (self.logged_in_teacher,))
            result = c.fetchone()

        if result:
            name, username, section, class_, photo_path, education = result

            # Top frame for welcome and photo
            top_frame = tk.Frame(self.options_frame.inner, bg="#e3f2fd")
            top_frame.pack(pady=10, fill=tk.X)

            # Teacher photo
            if photo_path and os.path.exists(photo_path):
                try:
                    img = Image.open(photo_path)
                    img.thumbnail((80, 80))
                    img_tk = ImageTk.PhotoImage(img)
                    photo_label = tk.Label(top_frame, image=img_tk, bg="#e3f2fd")
                    photo_label.image = img_tk
                    photo_label.pack(side=tk.LEFT, padx=10)
                except Exception:
                    tk.Label(top_frame, text="Photo error", bg="#e3f2fd", font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=10)
            else:
                tk.Label(top_frame, text="No Photo", bg="#e3f2fd", font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=10)

            # Info labels
            info_text = (
                f"Welcome,\n"
                f"Name: {name}\n"
                f"Username: {username}\n"
                f"Section: {section}\n"
                f"Class: {class_}\n"
                f"Education: {education}"
            )
            tk.Label(top_frame, text=info_text, font=("Segoe UI", 13), bg="#e3f2fd", justify=tk.LEFT).pack(side=tk.LEFT, padx=10)

        # Core teacher features
        features = [
            ("Mark Student Attendance", self.mark_student_attendance),
            ("View My Timetable", self.teacher_timetable),
            ("View My Gradebook", self.teacher_gradebook),
            ("Give Assignment", self.teacher_give_assignment),
            ("Announcements", self.teacher_view_announcements),
            ("Events", self.teacher_view_events),
            ("Resource Center", self.teacher_view_resources),
            ("Fee Notices", self.teacher_view_fees),
            ("Transport Info", self.teacher_view_transport),
            ("Cafeteria Menu", self.teacher_view_cafeteria),
            ("Clubs & Activities", self.teacher_view_clubs),
            ("Achievements", self.teacher_view_achievements),
            ("Emergency Info", self.teacher_view_emergency),
            ("Notifications", lambda: self.show_notifications('teacher', self.logged_in_teacher)),
            ("Menu", self.select_options)
        ]
        for text, cmd in features:
            tk.Button(
                self.options_frame.inner,
                text=text,
                command=cmd,
                width=20, height=2,
                font=("Segoe UI", 14),
                bg=self.primary if text != "Notifications" else self.success,
                fg="white",
                bd=0,
                activebackground=self.secondary if text != "Notifications" else "#66bb6a"
            ).pack(pady=10)

    def teacher_timetable(self):
        username = self.logged_in_teacher
        top = tk.Toplevel(self.root)
        top.title(f"{username}'s Timetable")
        top.geometry("1100x700")

        # Find all unique (class, section) for this teacher
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT DISTINCT class, section FROM timetable WHERE teacher_username=?", (username,))
            classes = c.fetchall()

        if not classes:
            tk.Label(top, text="No timetable entries found for you.", font=("Segoe UI", 16)).pack(pady=30)
            return

        for idx, (class_, section) in enumerate(classes):
            tk.Label(top, text=f"Class: {class_}  |  Section: {section}", font=("Segoe UI", 14, "bold")).pack(pady=(25 if idx > 0 else 10, 10))

            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            periods = [str(i) for i in range(1, 17)]
            # Time ranges for each period (from 9:00 to 17:00, 30 min per period)
            time_blocks = []
            h, m = 9, 0
            for _ in range(16):
                start = f"{h:02}:{m:02}"
                m += 30
                if m >= 60:
                    h += 1
                    m = 0
                end = f"{h:02}:{m:02}"
                time_blocks.append((start, end))

            table_frame = tk.Frame(top)
            table_frame.pack(pady=5)

            # Headers
            for col, day in enumerate(["Period"] + days):
                tk.Label(table_frame, text=day, font=("Segoe UI", 10, "bold"), borderwidth=1, relief="solid", width=17, bg="#e3f2fd").grid(row=0, column=col)

            # Content
            for row, period in enumerate(periods, 1):
                tk.Label(table_frame, text=f"P{period}\n{time_blocks[row-1][0]}-{time_blocks[row-1][1]}", font=("Segoe UI", 10), borderwidth=1, relief="solid", width=17, bg="#e3f2fd").grid(row=row, column=0)
                for col, day in enumerate(days, 1):
                    with sqlite3.connect('school.db') as conn:
                        c = conn.cursor()
                        c.execute("""
                            SELECT s.name FROM timetable t
                            JOIN subjects s ON t.subject_id = s.id
                            WHERE t.class=? AND t.section=? AND t.day=? AND t.period=? AND t.teacher_username=?
                        """, (class_, section, day, period, username))
                        subject = c.fetchone()
                        cell = subject[0] if subject else ""
                    tk.Label(table_frame, text=cell, font=("Segoe UI", 10), borderwidth=1, relief="solid", width=17, height=2, bg="#f5faff").grid(row=row, column=col)

        tk.Button(top, text="Close", command=top.destroy, font=("Segoe UI", 12), bg="#bdbdbd", fg="black").pack(pady=10)

    def teacher_gradebook(self):
        self.view_teacher_gradebook(self.logged_in_teacher)


        
    # --- Admin Dashboard ---
    def admin_dashboard(self):
        self.clear_options()
        features = [
            ("View Teacher Attendance", self.view_teacher_attendance),
            ("View Student Attendance", self.view_student_attendance),
            ("Manage Teachers", self.manage_teachers),
            ("Manage Parents", self.manage_parents),
            ("Manage Students", self.manage_students),
            ("Manage Timetable", self.manage_timetable),
            ("Manage Announcements", self.admin_manage_announcements),
            ("Manage Events", self.admin_manage_events),
            ("Manage Resources", self.admin_manage_resources),
            ("Fee Payment Management", self.admin_manage_fees),
            ("Transport Management", self.admin_manage_transport),
            ("Cafeteria Management", self.admin_manage_cafeteria),
            ("Clubs & Activities", self.admin_manage_clubs),
            ("Achievements & Badges", self.admin_manage_achievements),
            ("Emergency Contacts", self.admin_manage_emergency),
            ("Menu", self.select_options)
        ]
        for text, cmd in features:
            tk.Button(
                self.options_frame.inner,
                text=text,
                command=cmd,
                width=20, height=2,
                font=("Segoe UI", 14),
                bg=self.primary if text != "Menu" else "#9e9e9e",
                fg="white",
                bd=0,
                activebackground=self.secondary if text != "Menu" else "#bdbdbd"
            ).pack(pady=10)

    def view_teacher_attendance(self):
        self.clear_options()
        tk.Label(self.options_frame.inner, text="Teacher Attendance", font=("Segoe UI", 16), bg="#f5faff", fg=self.primary).pack()
        tk.Label(self.options_frame.inner, text="(Not implemented in this demo)", font=("Segoe UI", 12), bg="#f5faff", fg=self.secondary).pack()
        tk.Button(self.options_frame.inner, text="Back", command=self.admin_dashboard, width=20, height=2, font=("Segoe UI", 14), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=10)

    def view_student_attendance(self):
        self.clear_options()
        tk.Label(self.options_frame.inner, text="Student Attendance", font=("Segoe UI", 16), bg="#f5faff", fg=self.primary).pack()
        tree = ttk.Treeview(self.options_frame.inner, columns=('Student Name', 'Date', 'Status'), show='headings')
        tree.heading('Student Name', text='Student Name')
        tree.heading('Date', text='Date')
        tree.heading('Status', text='Status')
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT s.name, sa.date, sa.status
                FROM student_attendance sa
                JOIN students s ON sa.student_id = s.id
                ORDER BY sa.date DESC
            """)
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(self.options_frame.inner, text="Back", command=self.admin_dashboard, width=20, height=2, font=("Segoe UI", 14), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=10)

    # --- Teacher Management ---
    def manage_teachers(self):
        self.clear_options()
        btn_frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Add Teacher", command=self.add_teacher, font=("Segoe UI", 14), width=18, bg=self.success, fg="white", bd=0).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="View Teachers", command=self.view_teachers, font=("Segoe UI", 14), width=18, bg=self.secondary, fg="white", bd=0).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="Back", command=self.admin_dashboard, font=("Sogue UI", 14), width=18, bg=self.secondary, fg="White", bd=0).pack(padx=8)

    def add_teacher(self):
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(pady=20)
        entries = {}

        # Username
        tk.Label(frame, text="Username:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        username_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        username_entry.pack(pady=5)
        entries["username"] = username_entry

        # Password
        tk.Label(frame, text="Password (min 8 chars):", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        password_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30, show="*")
        password_entry.pack(pady=5)
        entries["password"] = password_entry

        # Name
        tk.Label(frame, text="Name:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        name_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        name_entry.pack(pady=5)
        entries["name"] = name_entry

        # Address
        tk.Label(frame, text="Address:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        address_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        address_entry.pack(pady=5)
        entries["address"] = address_entry

        # Phone Number
        tk.Label(frame, text="Phone Number:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        phone_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        phone_entry.pack(pady=5)
        entries["phone_number"] = phone_entry

        # Email
        tk.Label(frame, text="Email:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        email_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        email_entry.pack(pady=5)
        entries["email"] = email_entry

        # Section OptionMenu
        tk.Label(frame, text="Section:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        section_var = tk.StringVar(value="Nursery")
        section_menu = tk.OptionMenu(frame, section_var, "Nursery", "Primary", "Secondary")
        section_menu.config(font=("Segoe UI", 14), width=26)
        section_menu.pack(pady=5)
        entries["section"] = section_var

        # Class Combobox (dynamic options)
        tk.Label(frame, text="Class:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        class_var = tk.StringVar()
        class_combo = ttk.Combobox(frame, textvariable=class_var, font=("Segoe UI", 14), width=28, state="readonly")
        class_combo.pack(pady=5)
        entries["class_"] = class_var

        def update_class_options(*_):
            sec = section_var.get()
            if sec == "Nursery":
                class_combo["values"] = ["Nursery 1", "Nursery 2"]
                class_var.set("Nursery 1")
            elif sec == "Primary":
                class_combo["values"] = [f"Primary {i}" for i in range(1, 7)]
                class_var.set("Primary 1")
            elif sec == "Secondary":
                class_combo["values"] = [f"Secondary {i}" for i in range(1, 4)]
                class_var.set("Secondary 1")
        section_var.trace_add('write', update_class_options)
        update_class_options()

        # Education
        tk.Label(frame, text="Education:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        education_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        education_entry.pack(pady=5)
        entries["education"] = education_entry

        # Photo
        tk.Label(frame, text="Photo:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        photo_path = tk.StringVar()
        photo_preview = tk.Label(frame, bg="#f5faff")
        photo_preview.pack(pady=2)
        def select_photo():
            file = filedialog.askopenfilename(
                title="Choose Photo",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
            )
            if file:
                photo_path.set(file)
                try:
                    img = Image.open(file)
                    img.thumbnail((80, 80))
                    img_tk = ImageTk.PhotoImage(img)
                    photo_preview.configure(image=img_tk)
                    photo_preview.image = img_tk
                except Exception:
                    photo_preview.configure(text="Invalid image")
                    photo_preview.image = None
        tk.Button(frame, text="Upload Photo", command=select_photo, font=("Segoe UI", 12)).pack(pady=2)

        def save_teacher():
            username = entries["username"].get().strip()
            password = entries["password"].get().strip()
            name = entries["name"].get().strip()
            address = entries["address"].get().strip()
            phone_number = entries["phone_number"].get().strip()
            email = entries["email"].get().strip()
            section = entries["section"].get().strip()
            class_ = entries["class_"].get().strip()
            education = entries["education"].get().strip()
            photo = photo_path.get()
            if not all([username, password, name, address, phone_number, email, section, class_, education, photo]):
                messagebox.showerror("Error", "All fields are required, including photo.")
                return
            if len(password) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters.")
                return
            # Save photo to local directory
            photos_dir = "photos"
            os.makedirs(photos_dir, exist_ok=True)
            dest_path = os.path.join(photos_dir, f"{username}_{os.path.basename(photo)}")
            try:
                shutil.copy(photo, dest_path)
            except Exception as e:
                messagebox.showerror("Photo Error", f"Could not save photo: {e}")
                return
            try:
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("""
                        INSERT INTO teachers (username, name, address, phone_number, email, section, class, education, photo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (username, name, address, phone_number, email, section, class_, education, dest_path))
                    c.execute("""
                        INSERT INTO users (username, password, role, photo)
                        VALUES (?, ?, 'teacher', ?)
                    """, (username, password, dest_path))
                    conn.commit()
                messagebox.showinfo("Success", "Teacher added successfully!")
                self.manage_teachers()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))

        tk.Button(
            frame, text="Save", command=save_teacher, width=20, height=2, font=("Segoe UI", 14),
            bg=self.success, fg="white", bd=0, activebackground="#66bb6a"
        ).pack(pady=10)
        tk.Button(
            frame, text="Back", command=self.manage_teachers, width=20, height=2, font=("Segoe UI", 14),
            bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0"
        ).pack(pady=10)

    def view_teachers(self):
        self.clear_options()
        frame = tk.Frame(self.options_frame, bg="#f5faff")
        frame.pack(pady=20, fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(
            frame,
            columns=('Photo', 'Username', 'Name', 'Address', 'Phone', 'Email', 'Section', 'Class', 'Education'),
            show='headings',
            height=10
        )
        for col in ('Photo', 'Username', 'Name', 'Address', 'Phone', 'Email', 'Section', 'Class', 'Education'):
            tree.heading(col, text=col)
            if col == 'Photo':
                tree.column(col, width=70, anchor=tk.CENTER)
            else:
                tree.column(col, width=110 if col != 'Name' else 120, anchor=tk.W)
        # Store image objects to prevent garbage collection
        self.photo_thumbnails = {}
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT photo, username, name, address, phone_number, email, section, class, education FROM teachers")
            for row in c.fetchall():
                photo_path = row[0]
                img_tk = None
                if photo_path and os.path.exists(photo_path):
                    img = Image.open(photo_path)
                    img.thumbnail((40, 40))
                    img_tk = ImageTk.PhotoImage(img)
                    self.photo_thumbnails[row[1]] = img_tk  # Keyed on username
                tree.insert('', tk.END, values=row, image=img_tk)
        tree.pack(fill=tk.BOTH, expand=True)

        def on_double_click(event):
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], 'values')
                username = values[1]
                self.teacher_popup(username)
        tree.bind("<Double-1>", on_double_click)

        tk.Button(
            frame, text="Back", command=self.manage_teachers, width=20, height=2, font=("Segoe UI", 14),
            bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0"
        ).pack(pady=10)

    def teacher_popup(self, username):
        popup = tk.Toplevel(self.root)
        popup.title("Teacher Actions")
        popup.geometry("350x330")
        popup.configure(bg="#e3f2fd")
        tk.Label(popup, text=f"Actions for {username}", font=("Segoe UI", 14), bg="#e3f2fd").pack(pady=10)
        # Show teacher photo
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT photo FROM teachers WHERE username=?", (username,))
            res = c.fetchone()
            photo_path = res[0] if res else None
        if photo_path and os.path.exists(photo_path):
            img = Image.open(photo_path)
            img.thumbnail((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(popup, image=img_tk, bg="#e3f2fd")
            img_label.image = img_tk
            img_label.pack()

        def assign_timetable():
            popup.destroy()
            self.assign_teacher_timetable(username)

        def assign_gradebook():
            popup.destroy()
            self.assign_teacher_gradebook(username)

        def update_teacher():
            popup.destroy()
            self.update_teacher_form(username)

        def delete_teacher():
            if messagebox.askyesno("Confirm", f"Delete teacher {username}?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM teachers WHERE username=?", (username,))
                    c.execute("DELETE FROM users WHERE username=?", (username,))
                    conn.commit()
                popup.destroy()
                self.view_teachers()

        tk.Button(popup, text="Assign Timetable", command=assign_timetable, width=15, font=("Segoe UI", 12), bg=self.secondary, fg="white", bd=0).pack(pady=7)
        tk.Button(popup, text="Assign Gradebook", command=assign_gradebook, width=15, font=("Segoe UI", 12), bg=self.secondary, fg="white", bd=0).pack(pady=7)
        tk.Button(popup, text="Update", command=update_teacher, width=15, font=("Segoe UI", 12), bg=self.secondary, fg="white", bd=0).pack(pady=7)
        tk.Button(popup, text="Delete", command=delete_teacher, width=15, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0).pack(pady=7)

    def assign_teacher_timetable(self, username):
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(pady=20)
        tk.Label(frame, text=f"Assign Timetable for {username}", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        day_var = tk.StringVar(value="Monday")
        period_var = tk.StringVar()
        start_var = tk.StringVar()
        end_var = tk.StringVar()
        subject_var = tk.StringVar()
        class_var = tk.StringVar()
        section_var = tk.StringVar()
        tk.Label(frame, text="Day:", font=("Segoe UI", 12), bg="#f5faff").pack()
        tk.OptionMenu(frame, day_var, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday").pack()
        tk.Label(frame, text="Period:", font=("Segoe UI", 12), bg="#f5faff").pack()
        tk.Entry(frame, textvariable=period_var, font=("Segoe UI", 12)).pack()
        tk.Label(frame, text="Start Time (HH:MM):", font=("Segoe UI", 12), bg="#f5faff").pack()
        tk.Entry(frame, textvariable=start_var, font=("Segoe UI", 12)).pack()
        tk.Label(frame, text="End Time (HH:MM):", font=("Segoe UI", 12), bg="#f5faff").pack()
        tk.Entry(frame, textvariable=end_var, font=("Segoe UI", 12)).pack()
        tk.Label(frame, text="Subject Name:", font=("Segoe UI", 12), bg="#f5faff").pack()
        tk.Entry(frame, textvariable=subject_var, font=("Segoe UI", 12)).pack()
        tk.Label(frame, text="Class:", font=("Segoe UI", 12), bg="#f5faff").pack()
        tk.Entry(frame, textvariable=class_var, font=("Segoe UI", 12)).pack()
        tk.Label(frame, text="Section:", font=("Segoe UI", 12), bg="#f5faff").pack()
        tk.Entry(frame, textvariable=section_var, font=("Segoe UI", 12)).pack()
        def save_timetable():
            day = day_var.get()
            period = period_var.get()
            start = start_var.get()
            end = end_var.get()
            subject = subject_var.get().strip()
            class_ = class_var.get().strip()
            section = section_var.get().strip()
            if not all([day, period, start, end, subject, class_, section]):
                messagebox.showerror("Error", "All fields required")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id FROM subjects WHERE name=? AND class=? AND section=?", (subject, class_, section))
                row = c.fetchone()
                if row:
                    subject_id = row[0]
                else:
                    c.execute("INSERT INTO subjects (name, class, section) VALUES (?, ?, ?)", (subject, class_, section))
                    subject_id = c.lastrowid
                c.execute(
                    "INSERT INTO timetable (class, section, day, period, start_time, end_time, subject_id, teacher_username) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (class_, section, day, period, start, end, subject_id, username)
                )
                conn.commit()
            messagebox.showinfo("Success", "Timetable entry saved.")
            self.view_teachers()
        tk.Button(frame, text="Save", command=save_timetable, font=("Segoe UI", 12), bg=self.success, fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.view_teachers, font=("Segoe UI", 12), bg="#bdbdbd", fg="white").pack(pady=10)

    def assign_teacher_gradebook(self, username):
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(pady=20)
        tk.Label(frame, text=f"Assign Gradebook For {username}", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT class, section FROM teachers WHERE username=?", (username,))
            row = c.fetchone()
            if not row:
                tk.Label(frame, text="No class found for teacher.", bg="#f5faff", fg="red").pack()
                return
            class_, section = row
            c.execute("SELECT id, name FROM students WHERE class=? AND section=?", (class_, section))
            students = c.fetchall()
        tk.Label(frame, text=f"Class: {class_}   Section: {section}", font=("Segoe UI", 12), bg="#f5faff").pack()
        tk.Label(frame, text="Subject Name:", font=("Segoe UI", 12), bg="#f5faff").pack()
        subject_var = tk.StringVar()
        tk.Entry(frame, textvariable=subject_var, font=("Segoe UI", 12)).pack()
        tk.Label(frame, text="Exam Name:", font=("Segoe UI", 12), bg="#f5faff").pack()
        exam_var = tk.StringVar()
        tk.Entry(frame, textvariable=exam_var, font=("Segoe UI", 12)).pack()
        tk.Label(frame, text="Max Marks:", font=("Segoe UI", 12), bg="#f5faff").pack()
        maxmarks_var = tk.StringVar()
        tk.Entry(frame, textvariable=maxmarks_var, font=("Segoe UI", 12)).pack()
        entries = []
        for student_id, student_name in students:
            row_frame = tk.Frame(frame, bg="#f5faff")
            row_frame.pack()
            tk.Label(row_frame, text=student_name, font=("Segoe UI", 12), bg="#f5faff", width=18).pack(side=tk.LEFT)
            mark_var = tk.StringVar()
            tk.Entry(row_frame, textvariable=mark_var, font=("Segoe UI", 12), width=5).pack(side=tk.LEFT)
            entries.append((student_id, mark_var))
        def save_grades():
            subject = subject_var.get().strip()
            exam = exam_var.get().strip()
            maxmarks = maxmarks_var.get().strip()
            if not subject or not exam or not maxmarks:
                messagebox.showerror("Error", "All fields required")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id FROM subjects WHERE name=? AND class=? AND section=?", (subject, class_, section))
                row = c.fetchone()
                if row:
                    subject_id = row[0]
                else:
                    c.execute("INSERT INTO subjects (name, class, section) VALUES (?, ?, ?)", (subject, class_, section))
                    subject_id = c.lastrowid
                for student_id, mark_var in entries:
                    try:
                        marks = int(mark_var.get())
                    except:
                        marks = 0
                    c.execute(
                        "INSERT INTO marks (student_id, subject_id, exam_name, marks, max_marks, date) VALUES (?, ?, ?, ?, ?, ?)",
                        (student_id, subject_id, exam, marks, maxmarks, datetime.date.today().isoformat())
                    )
                conn.commit()
            messagebox.showinfo("Success", "Gradebook entries saved.")
            self.view_teachers()
        tk.Button(frame, text="Save", command=save_grades, font=("Segoe UI", 12), bg=self.success, fg="white").pack(pady=10)
        tk.Button(frame, text="Back", command=self.view_teachers, font=("Segoe UI", 12), bg="#bdbdbd", fg="white").pack(pady=10)


    # --- Student Management ---
    def manage_students(self):
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff", width=800, height=600)
        frame.pack(pady=20)
        tk.Button(frame, text="Add Student", command=self.add_student, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(frame, text="View Students", command=self.view_students, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(frame, text="Back", command=self.admin_dashboard, width=20, height=2, font=("Segoe UI", 14), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=10)

    def add_student(self):
        self.clear_options()
        frame = tk.Frame(self.options_frame, bg="#f5faff", width=800, height=600)
        frame.pack(pady=20)
        # --- Fields ---
        tk.Label(frame, text="Student Name:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        name_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        name_entry.pack(pady=7)

        tk.Label(frame, text="Gender:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        gender_var = tk.StringVar(value="Male")
        tk.OptionMenu(frame, gender_var, "Male", "Female", "Other").pack(pady=7)

        tk.Label(frame, text="Photo:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        photo_path = tk.StringVar()
        photo_preview = tk.Label(frame, bg="#f5faff")
        photo_preview.pack(pady=2)
        def select_photo():
            file = filedialog.askopenfilename(
                title="Choose Photo",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
            )
            if file:
                photo_path.set(file)
                img = Image.open(file)
                img.thumbnail((80, 80))
                img_tk = ImageTk.PhotoImage(img)
                photo_preview.configure(image=img_tk)
                photo_preview.image = img_tk
        tk.Button(frame, text="Upload Photo", command=select_photo, font=("Segoe UI", 12)).pack(pady=2)

        tk.Label(frame, text="Parent/Guardian Name:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        parent_name_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        parent_name_entry.pack(pady=7)

        tk.Label(frame, text="Parent/Guardian Phone Number:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        parent_phone_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        parent_phone_entry.pack(pady=7)

        # --- Date of Birth with selectors ---
        tk.Label(frame, text="Student DOB:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        dob_frame = tk.Frame(frame, bg="#f5faff")
        dob_frame.pack(pady=2)
        # Year, Month, Day dropdowns
        years = [str(y) for y in range(date.today().year-25, date.today().year+1)]
        months = [str(m).zfill(2) for m in range(1, 13)]
        days = [str(d).zfill(2) for d in range(1, 32)]
        year_var = tk.StringVar(value=years[-10])
        month_var = tk.StringVar(value="01")
        day_var = tk.StringVar(value="01")
        tk.Label(dob_frame, text="YYYY", bg="#f5faff", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.OptionMenu(dob_frame, year_var, *years).pack(side=tk.LEFT)
        tk.Label(dob_frame, text="MM", bg="#f5faff", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.OptionMenu(dob_frame, month_var, *months).pack(side=tk.LEFT)
        tk.Label(dob_frame, text="DD", bg="#f5faff", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.OptionMenu(dob_frame, day_var, *days).pack(side=tk.LEFT)

        tk.Label(frame, text="Admission Date:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        adm_frame = tk.Frame(frame, bg="#f5faff")
        adm_frame.pack(pady=2)
        years_adm = [str(y) for y in range(date.today().year-10, date.today().year+1)]
        year_adm_var = tk.StringVar(value=str(date.today().year))
        month_adm_var = tk.StringVar(value=str(date.today().month).zfill(2))
        day_adm_var = tk.StringVar(value=str(date.today().day).zfill(2))
        tk.Label(adm_frame, text="YYYY", bg="#f5faff", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.OptionMenu(adm_frame, year_adm_var, *years_adm).pack(side=tk.LEFT)
        tk.Label(adm_frame, text="MM", bg="#f5faff", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.OptionMenu(adm_frame, month_adm_var, *months).pack(side=tk.LEFT)
        tk.Label(adm_frame, text="DD", bg="#f5faff", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        tk.OptionMenu(adm_frame, day_adm_var, *days).pack(side=tk.LEFT)

        tk.Label(frame, text="Student Address:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        address_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        address_entry.pack(pady=7)

        tk.Label(frame, text="Student Email (optional):", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        email_entry = tk.Entry(frame, font=("Segoe UI", 14), width=30)
        email_entry.pack(pady=7)

        tk.Label(frame, text="Student Section:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        section_var = tk.StringVar(value="Nursery")
        tk.OptionMenu(frame, section_var, "Nursery", "Primary", "Secondary").pack(pady=7)

        tk.Label(frame, text="Student Class:", font=("Segoe UI", 14), bg="#f5faff").pack(pady=7)
        class_var = tk.StringVar()
        class_menu = ttk.Combobox(frame, textvariable=class_var, font=("Segoe UI", 14), width=28, state="readonly")
        def update_class_options(*_):
            sec = section_var.get()
            if sec == "Nursery":
                class_menu['values'] = ["Nursery 1", "Nursery 2"]
                class_menu.set("Nursery 1")
            elif sec == "Primary":
                class_menu['values'] = [f"Primary {i}" for i in range(1, 7)]
                class_menu.set("Primary 1")
            elif sec == "Secondary":
                class_menu['values'] = [f"Secondary {i}" for i in range(1, 4)]
                class_menu.set("Secondary 1")
        section_var.trace_add('write', update_class_options)
        class_menu.pack(pady=7)
        update_class_options()

        # --- Save ---
        def save_student():
            name = name_entry.get().strip()
            gender = gender_var.get().strip()
            parent_name = parent_name_entry.get().strip()
            parent_phone = parent_phone_entry.get().strip()
            dob = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
            admission_date = f"{year_adm_var.get()}-{month_adm_var.get()}-{day_adm_var.get()}"
            address = address_entry.get().strip()
            email = email_entry.get().strip()
            section = section_var.get()
            class_ = class_var.get()
            photo = photo_path.get()
            if not all([name, gender, parent_name, parent_phone, dob, address, section, class_, admission_date, photo]):
                messagebox.showerror("Error", "Please fill all required fields, including photo and dates.")
                return
            # Save photo to local directory
            photos_dir = "student_photos"
            os.makedirs(photos_dir, exist_ok=True)
            dest_path = os.path.join(photos_dir, f"{name.replace(' ','_')}_{os.path.basename(photo)}")
            try:
                shutil.copy(photo, dest_path)
            except Exception as e:
                messagebox.showerror("Photo Error", f"Could not save photo: {e}")
                return
            try:
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("""
                        INSERT INTO students 
                        (name, gender, dob, admission_date, address, email, section, class, parent_name, parent_phone, photo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (name, gender, dob, admission_date, address, email, section, class_, parent_name, parent_phone, dest_path))
                    conn.commit()
                messagebox.showinfo("Success", "Student added successfully")
                self.manage_students()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
        tk.Button(frame, text="Add", command=save_student, width=20, height=2, font=("Segoe UI", 14), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").pack(pady=10)
        tk.Button(frame, text="Back", command=self.manage_students, width=20, height=2, font=("Segoe UI", 14), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=10)

    def view_students(self):
        self.clear_options()
        frame = tk.Frame(self.options_frame, bg="#f5faff", width=1000, height=600)
        frame.pack(pady=20, fill=tk.BOTH, expand=True)

        columns = (
            'Photo', 'ID', 'Name', 'Gender', 'DOB', 'Admission Date', 'Address',
            'Email', 'Section', 'Class', 'Parent Name', 'Parent Phone'
        )
        tree = ttk.Treeview(
            frame,
            columns=columns,
            show='headings',
            height=15
        )

        for col in columns:
            tree.heading(col, text=col)
            if col == 'Photo':
                tree.column(col, width=70, anchor=tk.CENTER)
            else:
                tree.column(col, width=110 if col not in ['Name', 'Address'] else 150, anchor=tk.W)

        # Store image objects to prevent garbage collection
        self.student_photo_thumbnails = {}

        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT photo, id, name, gender, dob, admission_date, address, email,
                       section, class, parent_name, parent_phone
                FROM students
            """)
            for row in c.fetchall():
                photo_path = row[0]
                img_tk = None
                if photo_path and os.path.exists(photo_path):
                    img = Image.open(photo_path)
                    img.thumbnail((40, 40))
                    img_tk = ImageTk.PhotoImage(img)
                    self.student_photo_thumbnails[row[1]] = img_tk  # Keyed on id
                # Insert all columns, Photo column will be blank (but can be shown on select)
                tree.insert('', tk.END, values=row, image=img_tk)

        tree.pack(fill=tk.BOTH, expand=True)

        # On double-click, show full photo and details in a popup
        def on_double_click(event):
            selected = tree.selection()
            if selected:
                values = tree.item(selected[0], 'values')
                photo_path = values[0]
                popup = tk.Toplevel(self.root)
                popup.title("Student Details")
                popup.geometry("400x600")
                popup.configure(bg="#e3f2fd")
                # Photo
                if photo_path and os.path.exists(photo_path):
                    img = Image.open(photo_path)
                    img.thumbnail((200, 200))
                    img_tk = ImageTk.PhotoImage(img)
                    img_label = tk.Label(popup, image=img_tk, bg="#e3f2fd")
                    img_label.image = img_tk
                    img_label.pack(pady=10)
                else:
                    tk.Label(popup, text="No Photo", bg="#e3f2fd", font=("Segoe UI", 12)).pack(pady=10)
                # All other fields displayed
                labels = [
                    f"ID: {values[1]}",
                    f"Name: {values[2]}",
                    f"Gender: {values[3]}",
                    f"DOB: {values[4]}",
                    f"Admission Date: {values[5]}",
                    f"Address: {values[6]}",
                    f"Email: {values[7]}",
                    f"Section: {values[8]}",
                    f"Class: {values[9]}",
                    f"Parent Name: {values[10]}",
                    f"Parent Phone: {values[11]}"
                ]
                for text in labels:
                    tk.Label(popup, text=text, font=("Segoe UI", 13), bg="#e3f2fd", anchor="w", justify=tk.LEFT).pack(fill=tk.X, padx=30, pady=2)

        tree.bind("<Double-1>", on_double_click)

        tk.Button(
            frame, text="Back", command=self.manage_students,
            width=20, height=2, font=("Segoe UI", 14),
            bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0"
        ).pack(pady=10)
    
    # --- Parent Management ---
    def manage_parents(self):
        self.clear_options()
        tk.Button(self.options_frame.inner, text="Add Parent/Guardian", command=self.add_parent, width=20, height=2, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="View Parents/Guardians", command=self.view_parents, width=20, height=2, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Back", command=self.admin_dashboard, width=10, height=2, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=5)
        tk.Button(self.options_frame.inner, text="Menu", command=self.select_options, width=10, height=2, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=5)

    def add_parent(self):
        self.clear_options()
        tk.Label(self.options_frame.inner, text="Search Student:", font=("Segoe UI", 14), bg="#f5faff").pack()
        search_var = tk.StringVar()
        search_entry = tk.Entry(self.options_frame.inner, textvariable=search_var, width=30, font=("Segoe UI", 12))
        search_entry.pack(pady=5)
        students_frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        students_frame.pack(fill=tk.BOTH, expand=True)
        tree = ttk.Treeview(students_frame, columns=('ID', 'Name', 'Section', 'Class', 'DOB'), show='headings')
        for col in ('ID', 'Name', 'Section', 'Class', 'DOB'):
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.W, width=100 if col != 'Name' else 150)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_students(search=""):
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                if search:
                    c.execute("SELECT id, name, section, class, dob FROM students WHERE name LIKE ?", (f'%{search}%',))
                else:
                    c.execute("SELECT id, name, section, class, dob FROM students")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def on_search(*_):
            load_students(search_var.get())
        search_var.trace_add('write', on_search)
        load_students()
        def on_double_click(event):
            selected = tree.selection()
            if selected:
                student_id, student_name, section, class_, dob = tree.item(selected[0], 'values')
                self.add_parent_to_student(student_id, student_name)
        tree.bind("<Double-1>", on_double_click)
        tk.Button(self.options_frame.inner, text="Back", command=self.manage_parents, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=5)

    def add_parent_to_student(self, student_id, student_name):
        self.clear_options()
        tk.Label(self.options_frame.inner, text=f"Add Parent/Guardian for {student_name}", font=("Segoe UI", 14), bg="#f5faff").pack(pady=10)
        fields = [
            ("Parent/Guardian Full Name*", "parent_name"),
            ("Relationship to Student*", "relationship"),
            ("Home Address*", "address"),
            ("Phone Number*", "phone"),
            ("Email Address", "email"),
            ("Occupation", "occupation"),
            ("Workplace", "workplace"),
            ("Emergency Contact Name*", "emergency_name"),
            ("Emergency Contact Phone*", "emergency_phone"),
            ("Emergency Contact Relationship", "emergency_relationship"),
            ("ID Type (Optional)", "id_type"),
            ("ID Number (Optional)", "id_number"),
            ("Marital Status (Optional)", "marital_status"),
            ("Preferred Language (Optional)", "language"),
            ("Special Custody/Access Arrangements (Optional)", "custody"),
        ]
        entries = {}
        for label, key in fields:
            tk.Label(self.options_frame.inner, text=label, font=("Segoe UI", 12), bg="#f5faff").pack()
            entry = tk.Entry(self.options_frame.inner, width=40, font=("Segoe UI", 12))
            entry.pack(pady=2)
            entries[key] = entry
        def save_parent():
            data = {key: entries[key].get().strip() for _, key in fields}
            required = ["parent_name", "relationship", "address", "phone", "emergency_name", "emergency_phone"]
            if any(not data[key] for key in required):
                messagebox.showerror("Error", "Please fill all required fields marked with *.")
                return
            try:
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("""
                        INSERT INTO parents (
                            parent_name, relationship, address, phone, email, occupation, workplace,
                            emergency_name, emergency_phone, emergency_relationship, id_type, id_number,
                            marital_status, language, custody, student_id
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        data["parent_name"], data["relationship"], data["address"], data["phone"], data["email"], data["occupation"], data["workplace"],
                        data["emergency_name"], data["emergency_phone"], data["emergency_relationship"], data["id_type"], data["id_number"],
                        data["marital_status"], data["language"], data["custody"], student_id
                    ))
                    conn.commit()
                messagebox.showinfo("Success", "Parent/Guardian added successfully")
                self.manage_parents()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", str(e))
        tk.Button(self.options_frame.inner, text="Save", command=save_parent, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").pack(pady=10)
        tk.Button(self.options_frame.inner, text="Back", command=self.manage_parents, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=5)

    def view_parents(self):
        self.clear_options()
        columns = (
            'Parent Name', 'Relationship', 'Home Address', 'Phone', 'Email', 'Occupation', 'Workplace',
            'Emergency Name', 'Emergency Phone', 'Emergency Relationship', 'ID Type', 'ID Number',
            'Marital Status', 'Language', 'Custody', 'Student Name'
        )
        table_frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        table_frame.pack(fill=tk.BOTH, expand=True)
        xscroll = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        yscroll = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        tree = ttk.Treeview(
            table_frame, columns=columns, show='headings',
            xscrollcommand=xscroll.set, yscrollcommand=yscroll.set
        )
        xscroll.config(command=tree.xview)
        yscroll.config(command=tree.yview)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.W, width=120)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT p.parent_name, p.relationship, p.address, p.phone, p.email, p.occupation, p.workplace,
                       p.emergency_name, p.emergency_phone, p.emergency_relationship, p.id_type, p.id_number,
                       p.marital_status, p.language, p.custody, s.name
                FROM parents p JOIN students s ON p.student_id = s.id
            """)
            rows = c.fetchall()
            for row in rows:
                tree.insert('', tk.END, values=row)
        if not rows:
            tk.Label(self.options_frame.inner, text="No parent records found.", font=("Segoe UI", 12), bg="#f5faff", fg="red").pack(pady=10)
        tk.Button(self.options_frame.inner, text="Back", command=self.manage_parents, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=5)
        tk.Button(self.options_frame.inner, text="Menu", command=self.select_options, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=5)



    # --- Parent Login/Dashboard ---
    def parent_login(self):
        self.clear_options()
        tk.Label(self.options_frame.inner, text="Parent/Guardian Name:", font=("Segoe UI", 12), bg="#f5faff").pack()
        name_entry = tk.Entry(self.options_frame.inner, font=("Segoe UI", 12))
        name_entry.pack()
        tk.Label(self.options_frame.inner, text="Parent/Guardian Phone Number:", font=("Segoe UI", 12), bg="#f5faff").pack()
        phone_entry = tk.Entry(self.options_frame.inner, font=("Segoe UI", 12))
        phone_entry.pack()
        def check_parent():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("""
                    SELECT id, student_id FROM parents WHERE parent_name=? AND phone=?
                """, (name, phone))
                parent = c.fetchone()
            if parent:
                self.logged_in_parent = parent
                self.parent_dashboard(parent[1])
            else:
                messagebox.showerror("Invalid Credentials", "Parent/guardian not found or incorrect details.")
        tk.Button(self.options_frame.inner, text="Login", command=check_parent, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Menu", command=self.select_options, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack()

    def parent_dashboard(self, student_id):
        self.clear_options()
        tk.Label(self.options_frame.inner, text="Parent Dashboard", font=("Segoe UI", 14), bg="#f5faff", fg=self.primary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="View Child's Attendance", command=lambda: self.view_child_attendance(student_id), font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="View Announcements", command=self.parent_view_announcements, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Events", command=self.parent_view_events, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Resource Center", command=self.parent_view_resources, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Fee Payments", command=self.parent_view_fees, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Transport Info", command=self.parent_view_transport, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Cafeteria Menu", command=self.parent_view_cafeteria, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Clubs & Activities", command=self.parent_view_clubs, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Achievements", command=self.parent_view_achievements, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Emergency Info", command=self.parent_view_emergency, width=20, height=2, font=("Segoe UI", 14), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)
        tk.Button(self.options_frame.inner, text="Notifications", command=self.show_notifications, width=20, height=2, font=("Segoe UI", 14), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").pack(pady=10)
        tk.Button(self.options_frame.inner, text="Logout", command=self.select_options, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=10)


    def view_child_attendance(self, student_id):
        self.clear_options()
        tk.Label(self.options_frame.inner, text="Child's Attendance", font=("Segoe UI", 14), bg="#f5faff", fg=self.primary).pack(pady=10)
        tree = ttk.Treeview(self.options_frame.inner, columns=('Date', 'Status'), show='headings')
        tree.heading('Date', text='Date')
        tree.heading('Status', text='Status')
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT date, status FROM student_attendance WHERE student_id=?
            """, (student_id,))
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(self.options_frame.inner, text="Back", command=lambda: self.parent_dashboard(student_id), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=10)

    # --- Mark Student Attendance (for Teacher) ---
    def mark_student_attendance(self):
        self.clear_options()
        tk.Label(self.options_frame.inner, text="Mark Student Attendance", font=("Segoe UI", 16), bg="#f5faff", fg=self.primary).pack()
        self.attendance_status = {}
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, name, class FROM students")
            rows = c.fetchall()
            if rows:
                tree = ttk.Treeview(self.options_frame.inner, selectmode="browse")
                tree['columns'] = ('ID', 'Name', 'Class', 'Attendance')
                tree.column("#0", width=0, stretch=tk.NO)
                tree.column("ID", anchor=tk.W, width=50)
                tree.column("Name", anchor=tk.W, width=180)
                tree.column("Class", anchor=tk.W, width=100)
                tree.column("Attendance", anchor=tk.W, width=100)
                tree.heading("#0", text='', anchor=tk.W)
                tree.heading('ID', text='ID', anchor=tk.W)
                tree.heading('Name', text='Name', anchor=tk.W)
                tree.heading('Class', text='Class', anchor=tk.W)
                tree.heading('Attendance', text='Attendance', anchor=tk.W)
                for row in rows:
                    tree.insert('', 'end', values=(row[0], row[1], row[2], ''))
                    self.attendance_status[row[0]] = None
                tree.pack()
                def on_row_click(event):
                    item = tree.identify_row(event.y)
                    if item:
                        student_id = tree.item(item, 'values')[0]
                        student_name = tree.item(item, 'values')[1]
                        self.open_attendance_popup(student_id, student_name, tree, item)
                tree.bind("<Double-1>", on_row_click)
                tk.Label(self.options_frame.inner, text="(Double-click a student to mark attendance)", font=("Segoe UI", 10), bg="#f5faff", fg=self.secondary).pack()
                tk.Button(self.options_frame.inner, text="Submit Attendance", command=lambda: self.submit_attendance(tree), width=20, height=2, font=("Segoe UI", 14), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").pack(pady=10)
            else:
                tk.Label(self.options_frame.inner, text="No students in database.", font=("Segoe UI", 14), bg="#f5faff", fg=self.danger).pack(pady=15)
        tk.Button(self.options_frame.inner, text="Back", command=self.teacher_dashboard, width=20, height=2, font=("Segoe UI", 14), bg="#bdbdbd", fg="white", bd=0, activebackground="#e0e0e0").pack(pady=10)

    def open_attendance_popup(self, student_id, student_name, tree, item_id):
        popup = tk.Toplevel(self.root)
        popup.title(f"Mark Attendance for {student_name}")
        popup.configure(bg="#e3f2fd")
        tk.Label(popup, text=f"Mark attendance for {student_name}:", font=("Segoe UI", 14), bg="#e3f2fd", fg=self.primary).pack(pady=10)
        status_var = tk.StringVar(value=self.attendance_status.get(student_id) or "Present")
        for status in ["Present", "Absent", "Late"]:
            tk.Radiobutton(popup, text=status, variable=status_var, value=status, font=("Segoe UI", 12), bg="#e3f2fd").pack(anchor='w')
        def save():
            self.attendance_status[student_id] = status_var.get()
            tree.set(item_id, column="Attendance", value=status_var.get())
            popup.destroy()
        tk.Button(popup, text="Save", command=save, width=10, font=("Segoe UI", 12), bg=self.primary, fg="white", bd=0, activebackground=self.secondary).pack(pady=10)

    def submit_attendance(self, tree):
        today = datetime.date.today().isoformat()
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            for row_id in tree.get_children():
                student_id = tree.item(row_id)['values'][0]
                attendance = self.attendance_status.get(student_id)
                if attendance is None:
                    attendance = "Present"
                c.execute("INSERT INTO student_attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, today, attendance))
            conn.commit()
        messagebox.showinfo("Success", "Attendance submitted successfully")


    # --- Student Login/Dashboard ---
    def student_login(self):
        self.clear_options()
        tk.Label(self.options_frame.inner, text="Student Name:", font=("Segoe UI", 12), bg="#f5faff").pack()
        name_entry = tk.Entry(self.options_frame.inner, font=("Segoe UI", 12))
        name_entry.pack()
        tk.Label(self.options_frame.inner, text="Student DOB (YYYY-MM-DD):", font=("Segoe UI", 12), bg="#f5faff").pack()
        dob_entry = tk.Entry(self.options_frame.inner, font=("Segoe UI", 12))
        dob_entry.pack()
        def check_student():
            name = name_entry.get().strip()
            dob = dob_entry.get().strip()
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id FROM students WHERE name=? AND dob=?", (name, dob))
                student = c.fetchone()
            if student:
                self.student_dashboard(student[0], name)
            else:
                messagebox.showerror("Invalid Credentials", "Student not found or incorrect details.")
        tk.Button(
            self.options_frame.inner,
            text="Login",
            command=check_student,
            font=("Segoe UI", 12),
            bg=self.primary,
            fg="white",
            bd=0,
            activebackground=self.secondary
        ).pack(pady=10)
        tk.Button(
            self.options_frame.inner,
            text="Menu",
            command=self.select_options,
            font=("Segoe UI", 12),
            bg="#bdbdbd",
            fg="white",
            bd=0,
            activebackground="#e0e0e0"
        ).pack()

    
    def student_dashboard(self, student_id, student_name):
        self.clear_options()
        # --- Fetch student info from DB ---
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT name, gender, dob, admission_date, address, email, section, class, parent_name, parent_phone, photo
                FROM students WHERE id=?
            """, (student_id,))
            result = c.fetchone()
        if result:
            (name, gender, dob, admission_date, address, email,
             section, class_, parent_name, parent_phone, photo_path) = result

            top_frame = tk.Frame(self.options_frame.inner, bg="#e3f2fd")
            top_frame.pack(pady=10, fill=tk.X)

            # Photo
            if photo_path and os.path.exists(photo_path):
                img = Image.open(photo_path)
                img.thumbnail((80, 80))
                img_tk = ImageTk.PhotoImage(img)
                photo_label = tk.Label(top_frame, image=img_tk, bg="#e3f2fd")
                photo_label.image = img_tk
                photo_label.pack(side=tk.LEFT, padx=10)
            else:
                photo_label = tk.Label(top_frame, text="No Photo", bg="#e3f2fd", font=("Segoe UI", 12))
                photo_label.pack(side=tk.LEFT, padx=10)
            
            # Info labels
            info_text = (
                f"Welcome, {name}\n"
                f"Gender: {gender}\n"
                f"DOB: {dob}\n"
                f"Admission Date: {admission_date}\n"
                f"Class: {class_}    Section: {section}\n"
                f"Address: {address}\n"
                f"Email: {email}\n"
                f"Parent: {parent_name}\n"
                f"Parent Phone: {parent_phone}"
            )
            tk.Label(
                top_frame, text=info_text,
                font=("Segoe UI", 13), bg="#e3f2fd", justify=tk.LEFT, anchor="w"
            ).pack(side=tk.LEFT, padx=10)

            tk.Label(
                self.options_frame.inner,
                text=f"Welcome, {student_name}",
                font=("Segoe UI", 14),
                bg="#f5faff",
                fg=self.primary
            ).pack(pady=10)

        # Original student features
        tk.Button(
            self.options_frame.inner,
            text="View Attendance",
            command=lambda: self.view_child_attendance(student_id),
            font=("Segoe UI", 12),
            bg=self.primary,
            fg="white",
            bd=0,
            activebackground=self.secondary
        ).pack(pady=10)
        tk.Button(
            self.options_frame.inner,
            text="View Gradebook",
            command=lambda: self.student_gradebook(student_id),
            font=("Segoe UI", 12),
            bg=self.primary,
            fg="white",
            bd=0,
            activebackground=self.secondary
        ).pack(pady=10)
        tk.Button(
            self.options_frame.inner,
            text="View Timetable",
            command=lambda: self.view_timetable("student", student_id),
            font=("Segoe UI", 12),
            bg=self.primary,
            fg="white",
            bd=0,
            activebackground=self.secondary
        ).pack(pady=10)
        tk.Button(
            self.options_frame.inner,
            text="My Profile",
            command=lambda: self.my_profile("student", student_id),
            font=("Segoe UI", 12),
            bg=self.primary,
            fg="white",
            bd=0,
            activebackground=self.secondary
        ).pack(pady=10)

        # Feature-rich dashboard buttons
        tk.Button(
            self.options_frame.inner, text="Announcements",
            command=lambda: self.student_view_announcements(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Events",
            command=lambda: self.student_view_events(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Resource Center",
            command=lambda: self.student_view_resources(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Fee Notices",
            command=lambda: self.student_view_fees(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Transport Info",
            command=lambda: self.student_view_transport(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Cafeteria Menu",
            command=lambda: self.student_view_cafeteria(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Clubs & Activities",
            command=lambda: self.student_view_clubs(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Achievements",
            command=lambda: self.student_view_achievements(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Emergency Info",
            command=lambda: self.student_view_emergency(student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.primary, fg="white", bd=0, activebackground=self.secondary
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner, text="Notifications",
            command=lambda: self.show_notifications('student', student_id, student_name),
            width=20, height=2, font=("Segoe UI", 14),
            bg=self.success, fg="white", bd=0, activebackground="#66bb6a"
        ).pack(pady=10)

        tk.Button(
            self.options_frame.inner,
            text="Logout",
            command=self.select_options,
            font=("Segoe UI", 12),
            bg="#bdbdbd",
            fg="white",
            bd=0,
            activebackground="#e0e0e0"
        ).pack(pady=10)
        
    def student_gradebook(self, student_id):
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(pady=20)
        tk.Label(frame, text="Your Marks", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        tree = ttk.Treeview(frame, columns=('Subject', 'Exam', 'Marks', 'Max Marks', 'Date'), show='headings')
        for col in ('Subject', 'Exam', 'Marks', 'Max Marks', 'Date'):
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT sub.name, m.exam_name, m.marks, m.max_marks, m.date
                FROM marks m JOIN subjects sub ON m.subject_id=sub.id
                WHERE m.student_id=?
            """, (student_id,))
            results = c.fetchall()
            for row in results:
                tree.insert('', tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(
            frame,
            text="Back",
            command=lambda: self.student_dashboard(student_id, self.get_student_name_by_id(student_id)),
            font=("Segoe UI", 12), bg="#bdbdbd", fg="white"
        ).pack(pady=10)

    def get_student_name_by_id(self, student_id):
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT name FROM students WHERE id=?", (student_id,))
            row = c.fetchone()
            return row[0] if row else ""

    def view_teacher_gradebook(self, username):
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(pady=20)
        tk.Label(frame, text="Your Gradebook", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        tree = ttk.Treeview(frame, columns=('Student', 'Subject', 'Exam', 'Marks', 'Max Marks', 'Date'), show='headings')
        for col in ('Student', 'Subject', 'Exam', 'Marks', 'Max Marks', 'Date'):
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT class, section FROM teachers WHERE username=?", (username,))
            row = c.fetchone()
            if not row:
                frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
                tk.Label(frame, text="No class found.", font=("Segoe UI", 14), bg="#f5faff", fg="red").pack()
                return
            class_, section = row
            c.execute("""
                SELECT s.name, sub.name, m.exam_name, m.marks, m.max_marks, m.date
                FROM marks m
                JOIN students s ON m.student_id=s.id
                JOIN subjects sub ON m.subject_id=sub.id
                WHERE s.class=? AND s.section=?
            """, (class_, section))
            results = c.fetchall()
            for row in results:
                tree.insert('', tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(
            frame,
            text="Back",
            command=self.teacher_dashboard,
            font=("Segoe UI", 12), bg="#bdbdbd", fg="white"
        ).pack(pady=10)

    def view_timetable(self, user_type="student", user_id_or_username=None):
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(pady=20)
        tk.Label(frame, text="Class Timetable", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        columns = ('Day', 'Period', 'Start', 'End', 'Subject', 'Teacher')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.W)
        timetable_query = ""
        params = ()
        if user_type == "teacher" and user_id_or_username:
            timetable_query = "SELECT day, period, start_time, end_time, (SELECT name FROM subjects WHERE id=t.subject_id), teacher_username FROM timetable t WHERE teacher_username=?"
            params = (user_id_or_username,)
        elif user_type == "student" and user_id_or_username:
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT class, section FROM students WHERE id=?", (user_id_or_username,))
                res = c.fetchone()
                if res:
                    class_, section = res
                    timetable_query = "SELECT day, period, start_time, end_time, (SELECT name FROM subjects WHERE id=t.subject_id), teacher_username FROM timetable t WHERE class=? AND section=?"
                    params = (class_, section)
        else:
            timetable_query = "SELECT day, period, start_time, end_time, (SELECT name FROM subjects WHERE id=t.subject_id), teacher_username FROM timetable t"
            params = ()
        if timetable_query:
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute(timetable_query, params)
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True)
        if user_type == "teacher":
            tk.Button(
                frame,
                text="Back",
                command=self.teacher_dashboard,
                font=("Segoe UI", 12), bg="#bdbdbd", fg="white"
            ).pack(pady=10)
        elif user_type == "student" and user_id_or_username:
            tk.Button(
                frame,
                text="Back",
                command=lambda: self.student_dashboard(user_id_or_username, self.get_student_name_by_id(user_id_or_username)),
                font=("Segoe UI", 12), bg="#bdbdbd", fg="white"
            ).pack(pady=10)
        else:
            tk.Button(
                frame,
                text="Back",
                command=self.select_options,
                font=("Segoe UI", 12), bg="#bdbdbd", fg="white"
            ).pack(pady=10)

    def my_profile(self, user_type, user_id_or_username):
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(pady=20)
        tk.Label(frame, text="My Profile", font=("Segoe UI", 14), bg="#f5faff").pack(pady=5)
        info = {}
        if user_type == "student":
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT name, address, email, section, class FROM students WHERE id=?", (user_id_or_username,))
                row = c.fetchone()
                if row:
                    info = {"name": row[0], "address": row[1], "email": row[2], "section": row[3], "class": row[4]}
        entries = {}
        for label, key in (("Name", "name"), ("Address", "address"), ("Email", "email"), ("Section", "section"), ("Class", "class")):
            tk.Label(frame, text=label, font=("Segoe UI", 13), bg="#f5faff").pack()
            ent = tk.Entry(frame, font=("Segoe UI", 13), width=30)
            ent.insert(0, info.get(key, ""))
            ent.config(state="readonly")
            ent.pack(pady=2)
            entries[key] = ent
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(user_id_or_username, info.get("name", "")), font=("Segoe UI", 12), bg="#bdbdbd", fg="white").pack(pady=10)

    def manage_timetable(self):
        import sqlite3
        import tkinter as tk
        from tkinter import ttk, messagebox

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(pady=20, fill="both", expand=True)

        # Controls at the top
        tk.Label(frame, text="School Timetable Management", font=("Segoe UI", 18, "bold"), bg="#f5faff", fg=self.primary).pack(pady=(0, 10))

        # Section selection
        section_var = tk.StringVar(value="Nursery")
        tk.Label(frame, text="Select Section:", font=("Segoe UI", 14), bg="#f5faff").pack()
        section_menu = ttk.Combobox(frame, textvariable=section_var, values=["Nursery", "Primary", "Secondary"], font=("Segoe UI", 13), state="readonly", width=25)
        section_menu.pack(pady=5)

        # Class selection
        class_var = tk.StringVar()
        tk.Label(frame, text="Select Class:", font=("Segoe UI", 14), bg="#f5faff").pack()
        class_combo = ttk.Combobox(frame, textvariable=class_var, font=("Segoe UI", 13), state="readonly", width=25)
        class_combo.pack(pady=5)

        def update_class_combo(*_):
            sec = section_var.get()
            if sec == "Nursery":
                class_combo['values'] = ["Nursery 1", "Nursery 2"]
                class_combo.set("Nursery 1")
            elif sec == "Primary":
                class_combo['values'] = [f"Primary {i}" for i in range(1, 7)]
                class_combo.set("Primary 1")
            elif sec == "Secondary":
                class_combo['values'] = [f"Secondary {i}" for i in range(1, 4)]
                class_combo.set("Secondary 1")
        section_var.trace_add("write", update_class_combo)
        update_class_combo()

        # Timetable grid constants
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        periods = [str(i) for i in range(1, 17)]  # 16 periods from 9:00 to 17:00
        time_blocks = []
        h, m = 9, 0
        for _ in range(16):
            start = f"{h:02}:{m:02}"
            m += 30
            if m >= 60:
                h += 1
                m = 0
            end = f"{h:02}:{m:02}"
            time_blocks.append((start, end))

        # This dictionary will hold all cell data for saving
        cell_vars = {}

        # Table grid in its own sub-frame for .grid()
        table_frame = tk.Frame(frame, bg="#f5faff")
        table_frame.pack(pady=15)

        # Function to render timetable grid
        def render_grid():
            for widget in table_frame.winfo_children():
                widget.destroy()

            # Column headers
            for col, day in enumerate(["Period"] + days):
                tk.Label(table_frame, text=day, font=("Segoe UI", 10, "bold"), borderwidth=1, relief="solid", width=18, bg="#e3f2fd").grid(row=0, column=col)

            # Row headers and cells
            for row, period in enumerate(periods, 1):
                tk.Label(table_frame, text=f"P{period}\n{time_blocks[row-1][0]}-{time_blocks[row-1][1]}", font=("Segoe UI", 10), borderwidth=1, relief="solid", width=18, bg="#e3f2fd").grid(row=row, column=0)
                for col, day in enumerate(days, 1):
                    # Key for this cell
                    key = (day, period)
                    section = section_var.get()
                    class_ = class_var.get()
                    subject, teacher = "", ""
                    # Load from DB if possible
                    with sqlite3.connect('school.db') as conn:
                        c = conn.cursor()
                        c.execute("""SELECT s.name, t.teacher_username FROM timetable t
                                     JOIN subjects s ON t.subject_id=s.id
                                     WHERE t.class=? AND t.section=? AND t.day=? AND t.period=?""",
                                  (class_, section, day, period))
                        res = c.fetchone()
                        if res:
                            subject, teacher = res
                    var = tk.StringVar(value=f"{subject}\n{teacher}" if subject else "")
                    cell_vars[(day, period)] = [var, time_blocks[row-1][0], time_blocks[row-1][1]]

                    def make_on_cell_click(day=day, period=period, time_slot=time_blocks[row-1]):
                        def on_cell_click(event=None):
                            popup = tk.Toplevel(self.root)
                            popup.title(f"Edit {day} Period {period}")
                            popup.geometry("350x220")
                            tk.Label(popup, text=f"{day} Period {period}\nTime: {time_slot[0]}-{time_slot[1]}", font=("Segoe UI", 13)).pack(pady=10)
                            tk.Label(popup, text="Subject:", font=("Segoe UI", 12)).pack()
                            subj_entry = tk.Entry(popup, font=("Segoe UI", 12))
                            subj_entry.pack()
                            tk.Label(popup, text="Teacher Username:", font=("Segoe UI", 12)).pack()
                            teach_entry = tk.Entry(popup, font=("Segoe UI", 12))
                            teach_entry.pack()
                            # Fill previous value if any
                            if cell_vars[(day, period)][0].get():
                                split = cell_vars[(day, period)][0].get().split('\n')
                                subj_entry.insert(0, split[0])
                                if len(split) > 1:
                                    teach_entry.insert(0, split[1])
                            def save_cell():
                                subject = subj_entry.get().strip()
                                teacher = teach_entry.get().strip()
                                cell_vars[(day, period)][0].set(f"{subject}\n{teacher}" if subject else "")
                                popup.destroy()
                            tk.Button(popup, text="Save", command=save_cell, font=("Segoe UI", 12), bg="green", fg="white").pack(pady=12)
                        return on_cell_click

                    cell = tk.Label(table_frame, textvariable=var, font=("Segoe UI", 10), borderwidth=1, relief="solid", width=18, height=3, bg="#f5faff")
                    cell.grid(row=row, column=col, sticky="nsew")
                    cell.bind("<Button-1>", make_on_cell_click())

        # Refresh grid on class or section change
        class_var.trace_add("write", lambda *_: render_grid())
        section_var.trace_add("write", lambda *_: render_grid())

        render_grid()  # Initial display

        # Save all timetable entries to DB
        def save_all():
            section = section_var.get()
            class_ = class_var.get()
            if not (section and class_):
                messagebox.showerror("Error", "Please select section and class.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                # Remove old timetable for this class/section
                c.execute("DELETE FROM timetable WHERE class=? AND section=?", (class_, section))
                for (day, period), (var, start, end) in cell_vars.items():
                    if var.get():
                        split = var.get().split('\n')
                        subject = split[0]
                        teacher = split[1] if len(split) > 1 else ""
                        # Get or create subject
                        c.execute("SELECT id FROM subjects WHERE name=? AND class=? AND section=?", (subject, class_, section))
                        row = c.fetchone()
                        if row:
                            subject_id = row[0]
                        else:
                            c.execute("INSERT INTO subjects (name, class, section) VALUES (?, ?, ?)", (subject, class_, section))
                            subject_id = c.lastrowid
                        c.execute(
                            "INSERT INTO timetable (class, section, day, period, start_time, end_time, subject_id, teacher_username) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (class_, section, day, period, start, end, subject_id, teacher)
                        )
                conn.commit()
            messagebox.showinfo("Success", "Timetable saved!")

        tk.Button(frame, text="Save All", command=save_all, width=25, font=("Segoe UI", 14), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").pack(pady=10)

        # --- BACK AND MENU BUTTONS ---
        btn_style = {"width": 25, "font": ("Segoe UI", 14), "fg": "white", "bd": 0}
        tk.Button(frame, text="Back", command=self.admin_dashboard, bg="#bdbdbd", activebackground="#e0e0e0", **btn_style).pack(pady=6)
        tk.Button(frame, text="Menu", command=self.select_options, bg="#9e9e9e", activebackground="#bdbdbd", **btn_style).pack(pady=6)

    # --- Student Timetable View ---
    def student_timetable(self):
        import tkinter as tk
        import sqlite3

        # Get student's class and section from DB
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT class, section FROM students WHERE username=?", (self.logged_in_user,))
            row = c.fetchone()
            if not row:
                tk.messagebox.showerror("Error", "No class/section found for your account!")
                return
            class_, section = row

        top = tk.Toplevel(self.root)
        top.title(f"{self.logged_in_user}'s Class Timetable")
        top.geometry("1100x700")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        periods = [str(i) for i in range(1, 17)]

        # Get time ranges for each period
        time_blocks = []
        h, m = 9, 0
        for _ in range(16):
            start = f"{h:02}:{m:02}"
            m += 30
            if m >= 60:
                h += 1
                m = 0
            end = f"{h:02}:{m:02}"
            time_blocks.append((start, end))

        table_frame = tk.Frame(top)
        table_frame.pack(pady=5)

        tk.Label(top, text=f"Class: {class_}  |  Section: {section}", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Headers
        for col, day in enumerate(["Period"] + days):
            tk.Label(table_frame, text=day, font=("Segoe UI", 10, "bold"), borderwidth=1, relief="solid", width=17, bg="#e3f2fd").grid(row=0, column=col)

        # Content
        for row, period in enumerate(periods, 1):
            tk.Label(table_frame, text=f"P{period}\n{time_blocks[row-1][0]}-{time_blocks[row-1][1]}", font=("Segoe UI", 10), borderwidth=1, relief="solid", width=17, bg="#e3f2fd").grid(row=row, column=0)
            for col, day in enumerate(days, 1):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("""
                        SELECT s.name, t.teacher_username 
                        FROM timetable t
                        JOIN subjects s ON t.subject_id = s.id
                        WHERE t.class=? AND t.section=? AND t.day=? AND t.period=?
                    """, (class_, section, day, period))
                    got = c.fetchone()
                    cell = ""
                    if got:
                        cell = got[0]
                        if got[1]:
                            cell += "\n" + got[1]
                tk.Label(table_frame, text=cell, font=("Segoe UI", 10), borderwidth=1, relief="solid", width=17, height=2, bg="#f5faff").grid(row=row, column=col)

        tk.Button(top, text="Close", command=top.destroy, font=("Segoe UI", 12), bg="#bdbdbd", fg="black").pack(pady=10)

        # The following helper should be defined ONCE in your class (not inside manage_timetable)
        def find_any_student_id_by_class(self, section, class_):
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id FROM students WHERE section=? AND class=? LIMIT 1", (section, class_))
                row = c.fetchone()
                if row:
                    return row[0]
                return None
            
    def admin_manage_announcements(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Manage Announcements", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)

        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Title:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        title_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Message:", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        msg_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        msg_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Audience:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        audience_var = tk.StringVar(value="All")
        tk.OptionMenu(form_frame, audience_var, "All", "Teachers", "Parents", "Students").grid(row=2, column=1, sticky="w", padx=5, pady=2)
        def add_announcement():
            title = title_entry.get().strip()
            message = msg_entry.get().strip()
            audience = audience_var.get()
            if not title or not message:
                messagebox.showerror("Input Error", "Title and Message cannot be empty.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO announcements (title, message, audience) VALUES (?, ?, ?)", (title, message, audience))
                conn.commit()
            title_entry.delete(0, tk.END)
            msg_entry.delete(0, tk.END)
            audience_var.set("All")
            load_announcements()
            messagebox.showinfo("Success", "Announcement added.")
        tk.Button(form_frame, text="Add Announcement", command=add_announcement, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Title', 'Message', 'Audience')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Message' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_announcements():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, title, message, audience FROM announcements ORDER BY id DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select an announcement to delete.")
                return
            ann_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this announcement?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM announcements WHERE id=?", (ann_id,))
                    conn.commit()
                load_announcements()
                messagebox.showinfo("Deleted", "Announcement deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_announcements()

    def admin_manage_events(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Manage Events", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Event Name:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        date_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        date_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        desc_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        desc_entry.grid(row=2, column=1, padx=5, pady=2)
        def add_event():
            name = name_entry.get().strip()
            date = date_entry.get().strip()
            desc = desc_entry.get().strip()
            if not name or not date:
                messagebox.showerror("Input Error", "Event name and date cannot be empty.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO events (name, date, description) VALUES (?, ?, ?)", (name, date, desc))
                conn.commit()
            name_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            load_events()
            messagebox.showinfo("Success", "Event added.")
        tk.Button(form_frame, text="Add Event", command=add_event, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Event Name', 'Date', 'Description')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Description' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_events():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, name, date, description FROM events ORDER BY date DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select an event to delete.")
                return
            event_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this event?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM events WHERE id=?", (event_id,))
                    conn.commit()
                load_events()
                messagebox.showinfo("Deleted", "Event deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_events()

    def admin_manage_resources(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Manage Resources", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Resource Title:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        title_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Type (e.g. Book, PDF, Link):", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        type_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        type_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Location / URL:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        loc_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        loc_entry.grid(row=2, column=1, padx=5, pady=2)
        def add_resource():
            title = title_entry.get().strip()
            type_ = type_entry.get().strip()
            loc = loc_entry.get().strip()
            if not title or not type_:
                messagebox.showerror("Input Error", "Title and Type cannot be empty.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO resources (title, type, location) VALUES (?, ?, ?)", (title, type_, loc))
                conn.commit()
            title_entry.delete(0, tk.END)
            type_entry.delete(0, tk.END)
            loc_entry.delete(0, tk.END)
            load_resources()
            messagebox.showinfo("Success", "Resource added.")
        tk.Button(form_frame, text="Add Resource", command=add_resource, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Title', 'Type', 'Location')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Location' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_resources():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, title, type, location FROM resources ORDER BY id DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select a resource to delete.")
                return
            res_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this resource?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM resources WHERE id=?", (res_id,))
                    conn.commit()
                load_resources()
                messagebox.showinfo("Deleted", "Resource deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_resources()

    def admin_manage_fees(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Fee Payment Management", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Student ID:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        student_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        student_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Amount Due:", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        amt_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        amt_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Due Date (YYYY-MM-DD):", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        due_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        due_entry.grid(row=2, column=1, padx=5, pady=2)
        def add_fee():
            student_id = student_entry.get().strip()
            amt = amt_entry.get().strip()
            due = due_entry.get().strip()
            if not student_id or not amt or not due:
                messagebox.showerror("Input Error", "All fields are required.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO fees (student_id, amount_due, due_date) VALUES (?, ?, ?)", (student_id, amt, due))
                conn.commit()
            student_entry.delete(0, tk.END)
            amt_entry.delete(0, tk.END)
            due_entry.delete(0, tk.END)
            load_fees()
            messagebox.showinfo("Success", "Fee record added.")
        tk.Button(form_frame, text="Add Fee", command=add_fee, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Student ID', 'Amount Due', 'Due Date')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_fees():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, student_id, amount_due, due_date FROM fees ORDER BY due_date DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select a fee record to delete.")
                return
            fee_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this fee record?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM fees WHERE id=?", (fee_id,))
                    conn.commit()
                load_fees()
                messagebox.showinfo("Deleted", "Fee record deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_fees()

    def admin_manage_transport(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Transport Management", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Route Name:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        route_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        route_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Bus Number:", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        bus_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        bus_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Driver Name:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        driver_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        driver_entry.grid(row=2, column=1, padx=5, pady=2)
        def add_transport():
            route = route_entry.get().strip()
            bus = bus_entry.get().strip()
            driver = driver_entry.get().strip()
            if not route or not bus:
                messagebox.showerror("Input Error", "Route and Bus Number cannot be empty.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO transport (route, bus_number, driver) VALUES (?, ?, ?)", (route, bus, driver))
                conn.commit()
            route_entry.delete(0, tk.END)
            bus_entry.delete(0, tk.END)
            driver_entry.delete(0, tk.END)
            load_transport()
            messagebox.showinfo("Success", "Transport record added.")
        tk.Button(form_frame, text="Add Transport", command=add_transport, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Route', 'Bus Number', 'Driver')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_transport():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, route, bus_number, driver FROM transport ORDER BY id DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select a transport record to delete.")
                return
            transport_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this record?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM transport WHERE id=?", (transport_id,))
                    conn.commit()
                load_transport()
                messagebox.showinfo("Deleted", "Transport record deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_transport()

    def admin_manage_cafeteria(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Cafeteria Management", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Menu Item:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        item_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        item_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Category (e.g. Snack, Lunch):", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        cat_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        cat_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Price:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        price_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        price_entry.grid(row=2, column=1, padx=5, pady=2)
        def add_item():
            item = item_entry.get().strip()
            cat = cat_entry.get().strip()
            price = price_entry.get().strip()
            if not item or not cat or not price:
                messagebox.showerror("Input Error", "All fields are required.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO cafeteria (item, category, price) VALUES (?, ?, ?)", (item, cat, price))
                conn.commit()
            item_entry.delete(0, tk.END)
            cat_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
            load_items()
            messagebox.showinfo("Success", "Menu item added.")
        tk.Button(form_frame, text="Add Item", command=add_item, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Menu Item', 'Category', 'Price')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_items():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, item, category, price FROM cafeteria ORDER BY id DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select a menu item to delete.")
                return
            item_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this menu item?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM cafeteria WHERE id=?", (item_id,))
                    conn.commit()
                load_items()
                messagebox.showinfo("Deleted", "Menu item deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_items()

    def admin_manage_clubs(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Clubs & Activities Management", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Club Name:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Supervisor:", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        sup_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        sup_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        desc_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        desc_entry.grid(row=2, column=1, padx=5, pady=2)
        def add_club():
            name = name_entry.get().strip()
            sup = sup_entry.get().strip()
            desc = desc_entry.get().strip()
            if not name or not sup:
                messagebox.showerror("Input Error", "Club name and supervisor are required.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO clubs (name, supervisor, description) VALUES (?, ?, ?)", (name, sup, desc))
                conn.commit()
            name_entry.delete(0, tk.END)
            sup_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            load_clubs()
            messagebox.showinfo("Success", "Club added.")
        tk.Button(form_frame, text="Add Club", command=add_club, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Club Name', 'Supervisor', 'Description')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Description' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_clubs():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, name, supervisor, description FROM clubs ORDER BY id DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select a club to delete.")
                return
            club_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this club?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM clubs WHERE id=?", (club_id,))
                    conn.commit()
                load_clubs()
                messagebox.showinfo("Deleted", "Club deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_clubs()

    def admin_manage_achievements(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Achievements & Badges Management", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Student ID:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        sid_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        sid_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Title:", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        title_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        title_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        desc_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        desc_entry.grid(row=2, column=1, padx=5, pady=2)
        def add_achievement():
            sid = sid_entry.get().strip()
            title = title_entry.get().strip()
            desc = desc_entry.get().strip()
            if not sid or not title:
                messagebox.showerror("Input Error", "Student ID and title are required.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO achievements (student_id, title, description) VALUES (?, ?, ?)", (sid, title, desc))
                conn.commit()
            sid_entry.delete(0, tk.END)
            title_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            load_achievements()
            messagebox.showinfo("Success", "Achievement added.")
        tk.Button(form_frame, text="Add Achievement", command=add_achievement, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Student ID', 'Title', 'Description')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Description' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_achievements():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, student_id, title, description FROM achievements ORDER BY id DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select a record to delete.")
                return
            ach_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this achievement?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM achievements WHERE id=?", (ach_id,))
                    conn.commit()
                load_achievements()
                messagebox.showinfo("Deleted", "Achievement deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_achievements()

    def admin_manage_emergency(self):
        import tkinter as tk
        from tkinter import messagebox, ttk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Emergency Contacts Management", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)
        tk.Label(form_frame, text="Name:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Phone:", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        phone_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        phone_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(form_frame, text="Role:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        role_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        role_entry.grid(row=2, column=1, padx=5, pady=2)
        def add_contact():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            role = role_entry.get().strip()
            if not name or not phone:
                messagebox.showerror("Input Error", "Name and phone are required.")
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO emergency_contacts (name, phone, role) VALUES (?, ?, ?)", (name, phone, role))
                conn.commit()
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            role_entry.delete(0, tk.END)
            load_contacts()
            messagebox.showinfo("Success", "Emergency contact added.")
        tk.Button(form_frame, text="Add Contact", command=add_contact, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=3, columnspan=2, pady=8)
        list_frame = tk.Frame(frame, bg="#f5faff")
        list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        columns = ('ID', 'Name', 'Phone', 'Role')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_contacts():
            for item in tree.get_children():
                tree.delete(item)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("SELECT id, name, phone, role FROM emergency_contacts ORDER BY id DESC")
                for row in c.fetchall():
                    tree.insert('', tk.END, values=row)
        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Delete", "Select a contact to delete.")
                return
            c_id = tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Delete this contact?"):
                with sqlite3.connect('school.db') as conn:
                    c = conn.cursor()
                    c.execute("DELETE FROM emergency_contacts WHERE id=?", (c_id,))
                    conn.commit()
                load_contacts()
                messagebox.showinfo("Deleted", "Contact deleted.")
        tk.Button(frame, text="Delete Selected", command=delete_selected, font=("Segoe UI", 12), bg=self.danger, fg="white", bd=0, activebackground="#e57373").pack(pady=8)
        tk.Button(frame, text="Back", command=self.admin_dashboard, font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)
        load_contacts()


    def teacher_give_assignment(self):
        import tkinter as tk
        from tkinter import messagebox
        import sqlite3
        import json
        import datetime

        # Fetch teacher's name, class, section, subject
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute('SELECT name, class, section FROM teachers WHERE username=?', (self.logged_in_teacher,))
            row = c.fetchone()
            teacher_name = row[0] if row else ''
            class_ = row[1] if row else ''
            section = row[2] if row else ''
            c.execute('SELECT name FROM subjects WHERE class=? AND section=?', (class_, section))
            subj_row = c.fetchone()
            subject = subj_row[0] if subj_row else ''

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Top buttons
        top_frame = tk.Frame(frame, bg="#f5faff")
        top_frame.pack(fill=tk.X)
        tk.Button(top_frame, text="Give Assignment", font=("Segoe UI", 12), bg=self.primary, fg="white", command=self.teacher_give_assignment).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="View Assignments", font=("Segoe UI", 12), bg=self.secondary, fg="white", command=self.teacher_view_given_assignments).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Back", font=("Segoe UI", 12), bg="#bdbdbd", fg="white", command=self.teacher_dashboard).pack(side=tk.RIGHT, padx=5)

        tk.Label(frame, text="Give Assignment", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        form_frame = tk.Frame(frame, bg="#f5faff")
        form_frame.pack(pady=10)

        # Teacher name and subject (display only)
        tk.Label(form_frame, text="Teacher:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
        tk.Label(form_frame, text=teacher_name, font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=1, sticky="w", padx=5, pady=2)
        tk.Label(form_frame, text="Subject:", font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=0, sticky="e")
        tk.Label(form_frame, text=subject, font=("Segoe UI", 12), bg="#f5faff").grid(row=1, column=1, sticky="w", padx=5, pady=2)

        tk.Label(form_frame, text="Title:", font=("Segoe UI", 12), bg="#f5faff").grid(row=2, column=0, sticky="e")
        title_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        title_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Description:", font=("Segoe UI", 12), bg="#f5faff").grid(row=3, column=0, sticky="e")
        desc_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        desc_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Class:", font=("Segoe UI", 12), bg="#f5faff").grid(row=4, column=0, sticky="e")
        tk.Label(form_frame, text=class_, font=("Segoe UI", 12), bg="#f5faff").grid(row=4, column=1, sticky="w", padx=5, pady=2)
        tk.Label(form_frame, text="Section:", font=("Segoe UI", 12), bg="#f5faff").grid(row=5, column=0, sticky="e")
        tk.Label(form_frame, text=section, font=("Segoe UI", 12), bg="#f5faff").grid(row=5, column=1, sticky="w", padx=5, pady=2)

        tk.Label(form_frame, text="Due Date (YYYY-MM-DD):", font=("Segoe UI", 12), bg="#f5faff").grid(row=6, column=0, sticky="e")
        due_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        due_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        due_entry.grid(row=6, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Total Mark:", font=("Segoe UI", 12), bg="#f5faff").grid(row=7, column=0, sticky="e")
        mark_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=40)
        mark_entry.grid(row=7, column=1, padx=5, pady=2)

        tk.Label(form_frame, text="Amount of Questions:", font=("Segoe UI", 12), bg="#f5faff").grid(row=8, column=0, sticky="e")
        question_count_var = tk.IntVar(value=1)
        question_count_spin = tk.Spinbox(form_frame, from_=1, to=10, width=5, textvariable=question_count_var, font=("Segoe UI", 12))
        question_count_spin.grid(row=8, column=1, sticky="w", padx=5, pady=2)

        question_frame = tk.Frame(frame, bg="#f5faff")
        question_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        question_entries = []

        def refresh_questions(*args):
            for w in question_frame.winfo_children():
                w.destroy()
            question_entries.clear()
            for i in range(question_count_var.get()):
                row_frame = tk.Frame(question_frame, bg="#f5faff")
                row_frame.pack(anchor="w", pady=3)
                tk.Label(row_frame, text=f"Q{i+1}:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=0, sticky="e")
                q_entry = tk.Entry(row_frame, font=("Segoe UI", 12), width=35)
                q_entry.grid(row=0, column=1, padx=2)
                tk.Label(row_frame, text="Answer:", font=("Segoe UI", 12), bg="#f5faff").grid(row=0, column=2, sticky="e")
                a_entry = tk.Text(row_frame, font=("Segoe UI", 12), width=40, height=4, wrap='word')
                a_entry.grid(row=0, column=3, padx=2)
                question_entries.append((q_entry, a_entry))
        question_count_var.trace_add("write", lambda *a: refresh_questions())
        refresh_questions()

        def add_assignment():
            title = title_entry.get().strip()
            desc = desc_entry.get().strip()
            due = due_entry.get().strip()
            total_mark = mark_entry.get().strip()
            questions = []
            for q_entry, a_entry in question_entries:
                question = q_entry.get().strip()
                answer = a_entry.get("1.0", tk.END).strip()
                if not question or not answer or len(answer) < 10:
                    messagebox.showerror(
                        "Input Error",
                        "Every question and answer is required, and answers must be at least 10 characters."
                    )
                    return
                questions.append({"question": question, "answer": answer})
            if not title or not class_ or not due or not total_mark or not questions:
                messagebox.showerror(
                    "Input Error",
                    "Title, Class, Due Date, Total Mark, and all questions/answers are required."
                )
                return
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                c.execute("""
                    INSERT INTO assignments
                    (teacher_username, subject, title, description, class, section, due_date, mark, questions)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.logged_in_teacher, subject, title, desc, class_, section, due, int(total_mark), json.dumps(questions)
                ))
                conn.commit()
            title_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            due_entry.delete(0, tk.END)
            mark_entry.delete(0, tk.END)
            refresh_questions()
            messagebox.showinfo("Success", "Assignment added.")

        tk.Button(form_frame, text="Add Assignment", command=add_assignment, font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, activebackground="#66bb6a").grid(row=9, columnspan=2, pady=8)

    def teacher_view_given_assignments(self):
        import tkinter as tk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT id, subject, title, description, due_date, class, section, mark
                FROM assignments
                WHERE teacher_username=?
                ORDER BY due_date DESC
            """, (self.logged_in_teacher,))
            assignments = c.fetchall()

        tk.Label(frame, text="Your Given Assignments", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        if not assignments:
            tk.Label(frame, text="No assignments found.", font=("Segoe UI", 14), bg="#f5faff").pack(pady=20)
        else:
            for idx, (aid, subject, title, desc, due, class_, section, mark) in enumerate(assignments):
                af = tk.Frame(frame, bg="#eaf6fb", bd=2, relief='groove')
                af.pack(fill=tk.X, padx=10, pady=8)
                tk.Label(af, text=f"{title}", font=("Segoe UI", 13, "bold"), bg="#eaf6fb").pack(anchor="w", padx=8, pady=2)
                tk.Label(af, text=f"Subject: {subject}, Class: {class_} {section} | Due: {due} | Mark: {mark}", font=("Segoe UI", 11), bg="#eaf6fb").pack(anchor="w", padx=12)
                tk.Label(af, text=desc, font=("Segoe UI", 11), bg="#eaf6fb", wraplength=600, justify="left").pack(anchor="w", padx=12, pady=2)
                tk.Button(af, text="View Submissions", font=("Segoe UI", 11), bg="#90caf9",
                          command=lambda aid=aid: self.teacher_view_submissions(aid)).pack(anchor="e", padx=12, pady=3)

        tk.Button(frame, text="Back", command=self.teacher_give_assignment, font=("Segoe UI", 12), bg="#bdbdbd", fg="white").pack(pady=12)

    def student_view_assignments(self, student_id):
        import tkinter as tk
        import sqlite3

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            # Get class and section for this student
            c.execute("SELECT class, section FROM students WHERE id=?", (student_id,))
            row = c.fetchone()
            if not row:
                tk.Label(frame, text="Student not found.", font=("Segoe UI", 14), bg="#f5faff", fg="red").pack()
                return
            student_class, student_section = row
            # Normalize class/section (trim and lowercase for robust matching)
            student_class = student_class.strip().lower() if student_class else ""
            student_section = student_section.strip().lower() if student_section else ""

            print("DEBUG: student_class =", student_class, "student_section =", student_section)

            # Robust query: also normalize class/section in DB using LOWER(TRIM())
            c.execute("""
                SELECT a.id, t.name, a.subject, a.title, a.description, a.due_date, a.mark 
                FROM assignments a
                LEFT JOIN teachers t ON a.teacher_username = t.username
                WHERE LOWER(TRIM(a.class))=? AND LOWER(TRIM(a.section))=? 
                  AND a.teacher_username IS NOT NULL AND a.teacher_username != ''
                ORDER BY a.due_date
            """, (student_class, student_section))
            assignments = c.fetchall()
            print("DEBUG: assignments =", assignments)

        if not assignments:
            tk.Label(frame, text="No assignments for your class/section.", font=("Segoe UI", 14), bg="#f5faff").pack(pady=20)
        else:
            tk.Label(frame, text=f"Assignments for Class {student_class.title()} Section {student_section.title()}", font=("Segoe UI", 15, "bold"), bg="#f5faff").pack(pady=10)
            for idx, (assign_id, teacher_name, subject, title, desc, due, mark) in enumerate(assignments):
                af = tk.Frame(frame, bg="#eaf6fb", bd=2, relief='groove')
                af.pack(fill=tk.X, padx=10, pady=8)
                tk.Label(af, text=f"{idx+1}. {title}", font=("Segoe UI", 13, "bold"), bg="#eaf6fb").pack(anchor="w", padx=8, pady=2)
                tk.Label(af, text=f"Subject: {subject}   Teacher: {teacher_name}", font=("Segoe UI", 11), bg="#eaf6fb").pack(anchor="w", padx=12)
                tk.Label(af, text=f"Due: {due}   Total Mark: {mark}", font=("Segoe UI", 11), bg="#eaf6fb").pack(anchor="w", padx=12)
                tk.Label(af, text=desc, font=("Segoe UI", 11), bg="#eaf6fb", wraplength=600, justify="left").pack(anchor="w", padx=12, pady=2)
                tk.Button(
                    af,
                    text="Answer / View",
                    font=("Segoe UI", 11),
                    bg="#90caf9",
                    command=lambda aid=assign_id: self.student_answer_assignment(aid, student_id)
                ).pack(anchor="e", padx=12, pady=3)

        tk.Button(
            frame,
            text="Back",
            command=lambda: self.student_dashboard(student_id, ""),
            font=("Segoe UI", 12),
            bg="#bdbdbd",
            fg="white",
            bd=0
        ).pack(pady=12)
        
    def teacher_view_submissions(self, assignment_id):
        import tkinter as tk
        import sqlite3
        import json

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            # get questions for this assignment (for displaying student answers)
            c.execute("SELECT questions FROM assignments WHERE id=?", (assignment_id,))
            qrow = c.fetchone()
            questions = json.loads(qrow[0]) if qrow and qrow[0] else []
            # get submissions
            c.execute("""
                SELECT s.id, st.name, s.answer, s.submitted_on, s.mark_obtained, s.feedback
                FROM assignment_submissions s
                LEFT JOIN students st ON s.student_id = st.id
                WHERE s.assignment_id=?
            """, (assignment_id,))
            submissions = c.fetchall()

        tk.Label(frame, text="Assignment Submissions", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        if not submissions:
            tk.Label(frame, text="No submissions yet.", font=("Segoe UI", 14), bg="#f5faff").pack(pady=20)
        else:
            for idx, (sub_id, student_name, answer_json, submitted_on, mark, feedback) in enumerate(submissions):
                af = tk.Frame(frame, bg="#eaf6fb", bd=2, relief='groove')
                af.pack(fill=tk.X, padx=10, pady=8)
                tk.Label(af, text=f"{idx+1}. Student: {student_name}", font=("Segoe UI", 13, "bold"), bg="#eaf6fb").pack(anchor="w", padx=8, pady=2)
                tk.Label(af, text=f"Submitted: {submitted_on}", font=("Segoe UI", 11), bg="#eaf6fb").pack(anchor="w", padx=12)
                tk.Label(af, text=f"Mark: {mark if mark is not None else 'Not graded'}", font=("Segoe UI", 11), bg="#eaf6fb").pack(anchor="w", padx=12)

                student_answers = json.loads(answer_json) if answer_json else []
                if questions and isinstance(student_answers, list):
                    for qn, ans in zip(questions, student_answers):
                        tk.Label(af, text=f"Q: {qn['question']}", font=("Segoe UI", 11, "bold"), bg="#eaf6fb").pack(anchor="w", padx=16)
                        tk.Label(af, text=f"A: {ans}", font=("Segoe UI", 11), bg="#eaf6fb", wraplength=600, justify="left").pack(anchor="w", padx=32, pady=2)
                else:
                    tk.Label(af, text=f"Answers: {answer_json}", font=("Segoe UI", 11), bg="#eaf6fb", wraplength=600, justify="left").pack(anchor="w", padx=12, pady=2)

                if feedback:
                    tk.Label(af, text=f"Feedback: {feedback}", font=("Segoe UI", 11, "italic"), bg="#eaf6fb", fg="green").pack(anchor="w", padx=12, pady=2)

        tk.Button(frame, text="Back", command=self.teacher_view_given_assignments, font=("Segoe UI", 12), bg="#bdbdbd", fg="white").pack(pady=12)

    def student_answer_assignment(self, assignment_id, student_id):
        import tkinter as tk
        import sqlite3
        import json
        import datetime
        from tkinter import messagebox

        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Fetch assignment questions and title
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT title, questions FROM assignments WHERE id=?", (assignment_id,))
            row = c.fetchone()
            if not row:
                tk.Label(frame, text="Assignment not found.", font=("Segoe UI", 14), bg="#f5faff", fg="red").pack()
                return
            title, questions_json = row
            questions = json.loads(questions_json) if questions_json else []

        tk.Label(frame, text=f"Assignment: {title}", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)

        answer_vars = []
        for idx, q in enumerate(questions):
            qf = tk.Frame(frame, bg="#eaf6fb")
            qf.pack(fill=tk.X, padx=10, pady=6)
            tk.Label(qf, text=f"Q{idx+1}: {q['question']}", font=("Segoe UI", 12, "bold"), bg="#eaf6fb").pack(anchor="w", padx=4)
            a_text = tk.Text(qf, font=("Segoe UI", 12), width=60, height=3, wrap='word')
            a_text.pack(padx=8, pady=2)
            answer_vars.append(a_text)

        def submit_answers():
            answers = [a.get("1.0", tk.END).strip() for a in answer_vars]
            if any(len(ans) < 1 for ans in answers):
                messagebox.showerror("Incomplete", "Please answer all questions.")
                return
            # Save in assignment_submissions (one per assignment per student)
            with sqlite3.connect('school.db') as conn:
                c = conn.cursor()
                # Check if already submitted
                c.execute("SELECT id FROM assignment_submissions WHERE assignment_id=? AND student_id=?", (assignment_id, student_id))
                if c.fetchone():
                    messagebox.showinfo("Already submitted", "You have already submitted this assignment.")
                    return
                c.execute(
                    "INSERT INTO assignment_submissions (assignment_id, student_id, answer, submitted_on) VALUES (?, ?, ?, ?)",
                    (assignment_id, student_id, json.dumps(answers), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()
            messagebox.showinfo("Submitted", "Your answers have been submitted.")
            self.student_view_assignments(student_id)

        tk.Button(frame, text="Submit Answers", font=("Segoe UI", 12), bg=self.success, fg="white", bd=0, command=submit_answers).pack(pady=12)
        tk.Button(frame, text="Back", font=("Segoe UI", 12), bg="#bdbdbd", fg="white", command=lambda: self.student_view_assignments(student_id)).pack(pady=2)
                    

    def student_view_announcements(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Announcements", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Title', 'Message', 'Audience')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Message' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, title, message, audience FROM announcements WHERE audience='All' OR audience='Students' ORDER BY id DESC")
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

    def student_view_events(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Events", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Event Name', 'Date', 'Description')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Description' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, name, date, description FROM events ORDER BY date DESC")
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

    def student_view_resources(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Resource Center", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Title', 'Type', 'Location')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Location' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, title, type, location FROM resources ORDER BY id DESC")
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

    def student_view_fees(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Fee Notices", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Student ID', 'Amount Due', 'Due Date')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, student_id, amount_due, due_date FROM fees WHERE student_id=? ORDER BY due_date DESC", (student_id,))
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

    def student_view_transport(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Transport Info", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Route', 'Bus Number', 'Driver')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, route, bus_number, driver FROM transport ORDER BY id DESC")
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

    def student_view_cafeteria(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Cafeteria Menu", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Menu Item', 'Category', 'Price')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, item, category, price FROM cafeteria ORDER BY id DESC")
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

    def student_view_clubs(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Clubs & Activities", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Club Name', 'Supervisor', 'Description')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Description' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, name, supervisor, description FROM clubs ORDER BY id DESC")
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

    def student_view_achievements(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Achievements", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Student ID', 'Title', 'Description')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col != 'Description' else 300, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, student_id, title, description FROM achievements WHERE student_id=? ORDER BY id DESC", (student_id,))
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

    def student_view_emergency(self, student_id, student_name):
        import tkinter as tk
        from tkinter import ttk
        import sqlite3
        self.clear_options()
        frame = tk.Frame(self.options_frame.inner, bg="#f5faff")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        tk.Label(frame, text="Emergency Info", font=("Segoe UI", 16, "bold"), fg=self.primary, bg="#f5faff").pack(pady=10)
        columns = ('ID', 'Name', 'Phone', 'Role')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.W)
        tree.pack(fill=tk.BOTH, expand=True)
        with sqlite3.connect('school.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, name, phone, role FROM emergency_contacts ORDER BY id DESC")
            for row in c.fetchall():
                tree.insert('', tk.END, values=row)
        tk.Button(frame, text="Back", command=lambda: self.student_dashboard(student_id, student_name), font=("Segoe UI", 12), bg="#bdbdbd", fg="white", bd=0).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolApp(root)
    app.create_database()
    root.mainloop()
