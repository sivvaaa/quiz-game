import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz.db")

# (category, question, A, B, C, D, correct letter)
SAMPLE_QUESTIONS = [
    # ---------- Science ----------
    ("Science", "What is the chemical formula of water?", "H2O", "CO2", "O2", "NaCl", "A"),
    ("Science", "Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B"),
    ("Science", "Which gas do plants absorb for photosynthesis?", "Oxygen", "Nitrogen", "Carbon dioxide", "Helium", "C"),
    ("Science", "What is the hardest natural substance?", "Gold", "Iron", "Diamond", "Quartz", "C"),
    ("Science", "How many bones are in an adult human body?", "206", "201", "212", "198", "A"),
    ("Science", "Approximate speed of light?", "3,000 km/s", "30,000 km/s", "300,000 km/s", "3,000,000 km/s", "C"),
    ("Science", "What is the powerhouse of the cell?", "Nucleus", "Mitochondria", "Ribosome", "Golgi body", "B"),
    ("Science", "Which is the closest star to Earth?", "Sirius", "Proxima Centauri", "The Sun", "Polaris", "C"),
    ("Science", "What is the atomic number of carbon?", "6", "12", "8", "14", "A"),
    ("Science", "Which force pulls objects toward Earth?", "Friction", "Magnetism", "Gravity", "Inertia", "C"),
    # ---------- GK ----------
    ("GK", "What is the capital of France?", "Berlin", "Madrid", "Paris", "Rome", "C"),
    ("GK", "Which is the largest ocean?", "Atlantic", "Indian", "Arctic", "Pacific", "D"),
    ("GK", "Who wrote 'Romeo and Juliet'?", "Dickens", "Shakespeare", "Austen", "Twain", "B"),
    ("GK", "How many continents are there?", "5", "6", "7", "8", "C"),
    ("GK", "Which is the largest country by area?", "Canada", "China", "USA", "Russia", "D"),
    ("GK", "What is the currency of Japan?", "Yuan", "Won", "Yen", "Dollar", "C"),
    ("GK", "Which is the highest mountain above sea level?", "K2", "Everest", "Kilimanjaro", "Denali", "B"),
    ("GK", "In which year did World War II end?", "1942", "1945", "1948", "1950", "B"),
    ("GK", "Which is commonly considered the longest river?", "Amazon", "Nile", "Yangtze", "Danube", "B"),
    ("GK", "Which is the largest animal on Earth?", "Elephant", "Blue whale", "Giraffe", "Shark", "B"),
    # ---------- Tech ----------
    ("Tech", "What does HTML stand for?", "HyperText Markup Language", "High Text Machine Language", "Hyper Tool Multi Language", "Home Text Markup Language", "A"),
    ("Tech", "Who developed Python?", "Guido van Rossum", "James Gosling", "Dennis Ritchie", "Linus Torvalds", "A"),
    ("Tech", "What does CPU stand for?", "Computer Personal Unit", "Central Processing Unit", "Central Program Utility", "Core Processing Unit", "B"),
    ("Tech", "Which is volatile memory?", "ROM", "SSD", "RAM", "HDD", "C"),
    ("Tech", "What is SQL used for?", "Styling web pages", "Managing databases", "Drawing graphics", "Compiling code", "B"),
    ("Tech", "Who created the Linux kernel?", "Bill Gates", "Steve Jobs", "Linus Torvalds", "Mark Zuckerberg", "C"),
    ("Tech", "What is decimal 5 in binary?", "100", "101", "110", "111", "B"),
    ("Tech", "Which is a version control system?", "Git", "Excel", "Photoshop", "Chrome", "A"),
    ("Tech", "What is the default port for HTTP?", "21", "22", "80", "443", "C"),
    ("Tech", "Which file extension is used for Python files?", ".pt", ".py", ".python", ".pyt", "B"),
]


def get_conn():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    with get_conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            opt_a TEXT NOT NULL, opt_b TEXT NOT NULL,
            opt_c TEXT NOT NULL, opt_d TEXT NOT NULL,
            answer TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            category TEXT NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id))""")
        if c.execute("SELECT COUNT(*) FROM questions").fetchone()[0] == 0:
            c.executemany(
                "INSERT INTO questions(category,question,opt_a,opt_b,opt_c,opt_d,answer) "
                "VALUES (?,?,?,?,?,?,?)", SAMPLE_QUESTIONS)


def register_user(username, password):
    """Returns True if created, False if username already exists."""
    try:
        with get_conn() as c:
            c.execute("INSERT INTO users(username, password_hash) VALUES (?,?)",
                      (username, hash_password(password)))
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(username, password):
    """Returns (id, username) or None."""
    with get_conn() as c:
        return c.execute(
            "SELECT id, username FROM users WHERE username=? AND password_hash=?",
            (username, hash_password(password))).fetchone()


def get_categories():
    with get_conn() as c:
        return [r[0] for r in c.execute("SELECT DISTINCT category FROM questions ORDER BY category")]


def get_questions(category, limit=10):
    with get_conn() as c:
        return c.execute(
            "SELECT question, opt_a, opt_b, opt_c, opt_d, answer FROM questions "
            "WHERE category=? ORDER BY RANDOM() LIMIT ?", (category, limit)).fetchall()


def add_question(category, question, a, b, c_, d, answer):
    with get_conn() as c:
        c.execute(
            "INSERT INTO questions(category,question,opt_a,opt_b,opt_c,opt_d,answer) "
            "VALUES (?,?,?,?,?,?,?)", (category, question, a, b, c_, d, answer))


def save_score(user_id, score, category):
    with get_conn() as c:
        c.execute("INSERT INTO scores(user_id, score, category) VALUES (?,?,?)",
                  (user_id, score, category))


def top_scores(limit=10):
    with get_conn() as c:
        return c.execute(
            "SELECT u.username, s.score, s.category, s.date FROM scores s "
            "JOIN users u ON u.id = s.user_id "
            "ORDER BY s.score DESC, s.date ASC LIMIT ?", (limit,)).fetchall()
                
