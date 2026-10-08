import tkinter as tk
from tkinter import messagebox, ttk
import database as db
from quiz import QuizScreen
from leaderboard import LeaderboardScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Game")
        self.geometry("540x480")
        self.user = None  # (id, username) after login
        db.init_db()
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.show_login()

    # ---------- helpers ----------
    def clear(self):
        for w in self.container.winfo_children():
            w.destroy()

    def show_frame(self, frame):
        self.clear()
        frame.pack(fill="both", expand=True)

    # ---------- login / register ----------
    def show_login(self):
        self.clear()
        f = tk.Frame(self.container)
        f.pack(expand=True)
        tk.Label(f, text="Quiz Game", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(f, text="Username").pack()
        user_e = tk.Entry(f, width=28)
        user_e.pack(pady=3)
        tk.Label(f, text="Password").pack()
        pass_e = tk.Entry(f, width=28, show="*")
        pass_e.pack(pady=3)

        def do_login():
            u, p = user_e.get().strip(), pass_e.get()
            if not u or not p:
                return messagebox.showwarning("Missing", "Enter username and password.")
            row = db.login_user(u, p)
            if row:
                self.user = row
                self.show_menu()
            else:
                messagebox.showerror("Failed", "Wrong username or password.")

        def do_register():
            u, p = user_e.get().strip(), pass_e.get()
            if not u or not p:
                return messagebox.showwarning("Missing", "Enter username and password.")
            if len(p) < 4:
                return messagebox.showwarning("Weak", "Password must be at least 4 characters.")
            if db.register_user(u, p):
                messagebox.showinfo("Success", "Account created. You can log in now.")
            else:
                messagebox.showerror("Taken", "Username already exists.")

        tk.Button(f, text="Login", width=15, command=do_login).pack(pady=(15, 5))
        tk.Button(f, text="Register", width=15, command=do_register).pack()

    # ---------- main menu ----------
    def show_menu(self):
        self.clear()
        f = tk.Frame(self.container)
        f.pack(expand=True)
        tk.Label(f, text=f"Welcome, {self.user[1]}!", font=("Arial", 18, "bold")).pack(pady=15)
        tk.Label(f, text="Choose a category:", font=("Arial", 12)).pack(pady=5)
        for cat in db.get_categories():
            tk.Button(f, text=cat, width=22, command=lambda c=cat: self.start_quiz(c)).pack(pady=3)
        tk.Button(f, text="Leaderboard", width=22, command=self.show_leaderboard).pack(pady=(15, 3))
        if self.user[1].lower() == "admin":
            tk.Button(f, text="Add Questions (Admin)", width=22, command=self.show_admin).pack(pady=3)
        tk.Button(f, text="Logout", width=22, command=self.logout).pack(pady=3)

    def logout(self):
        self.user = None
        self.show_login()

    # ---------- quiz / leaderboard ----------
    def start_quiz(self, category):
        if not db.get_questions(category, 1):
            return messagebox.showinfo("Empty", "No questions in this category.")
        self.show_frame(QuizScreen(self.container, self, category))

    def show_leaderboard(self):
        self.show_frame(LeaderboardScreen(self.container, self))

    # ---------- admin: add questions ----------
    def show_admin(self):
        self.clear()
        f = tk.Frame(self.container)
        f.pack(expand=True)
        tk.Label(f, text="Add a Question", font=("Arial", 16, "bold")).pack(pady=10)

        entries = {}
        for label in ("Category", "Question", "Option A", "Option B", "Option C", "Option D"):
            tk.Label(f, text=label).pack()
            e = tk.Entry(f, width=45)
            e.pack(pady=2)
            entries[label] = e

        tk.Label(f, text="Correct answer").pack()
        ans = ttk.Combobox(f, values=["A", "B", "C", "D"], width=5, state="readonly")
        ans.current(0)
        ans.pack(pady=3)

        def save():
            vals = [entries[k].get().strip() for k in entries]
            if not all(vals):
                return messagebox.showwarning("Missing", "Fill in every field.")
            db.add_question(*vals, ans.get())
            messagebox.showinfo("Saved", "Question added.")
            for e in entries.values():
                e.delete(0, "end")

        tk.Button(f, text="Save Question", width=18, command=save).pack(pady=8)
        tk.Button(f, text="Back", width=18, command=self.show_menu).pack()


if __name__ == "__main__":
    App().mainloop()
  
