import tkinter as tk
import database as db

TIME_PER_QUESTION = 15
QUESTIONS_PER_ROUND = 10


class QuizScreen(tk.Frame):
    def __init__(self, master, app, category):
        super().__init__(master)
        self.app = app
        self.category = category
        self.questions = db.get_questions(category, QUESTIONS_PER_ROUND)
        self.index = 0
        self.score = 0
        self.streak = 0
        self.time_left = TIME_PER_QUESTION
        self.job = None
        self.correct = None

        self.info = tk.Label(self, font=("Arial", 11))
        self.info.pack(pady=(15, 5))
        self.timer_label = tk.Label(self, font=("Arial", 16, "bold"))
        self.timer_label.pack()
        self.q_label = tk.Label(self, font=("Arial", 14), wraplength=460, justify="center")
        self.q_label.pack(pady=20)

        self.buttons = []
        for letter in "ABCD":
            b = tk.Button(self, font=("Arial", 12), width=40, anchor="w",
                          command=lambda l=letter: self.check(l))
            b.pack(pady=4)
            self.buttons.append(b)
        self.default_bg = self.buttons[0].cget("bg")

        self.show_question()

    def show_question(self):
        if self.index >= len(self.questions):
            return self.finish()
        q, a, b, c, d, ans = self.questions[self.index]
        self.correct = ans
        self.info.config(
            text=f"Question {self.index + 1}/{len(self.questions)}    "
                 f"Score: {self.score}    Streak: {self.streak}")
        self.q_label.config(text=q)
        for btn, letter, text in zip(self.buttons, "ABCD", (a, b, c, d)):
            btn.config(text=f"{letter}. {text}", state="normal", bg=self.default_bg)
        self.countdown(TIME_PER_QUESTION)

    def countdown(self, t):
        self.time_left = t
        self.timer_label.config(text=f"Time: {t}", fg="red" if t <= 5 else "black")
        if t > 0:
            self.job = self.after(1000, self.countdown, t - 1)
        else:
            self.check(None)  # time ran out

    def check(self, choice):
        if self.job:
            self.after_cancel(self.job)
            self.job = None
        for btn, letter in zip(self.buttons, "ABCD"):
            btn.config(state="disabled")
            if letter == self.correct:
                btn.config(bg="#8be28b")
            elif letter == choice:
                btn.config(bg="#f28b82")

        if choice == self.correct:
            self.streak += 1
            bonus = self.time_left // 3            # faster answer = bigger bonus
            self.score += 10 + bonus + (2 if self.streak >= 3 else 0)
        else:
            self.streak = 0
        self.after(1200, self.next_question)

    def next_question(self):
        self.index += 1
        self.show_question()

    def finish(self):
        db.save_score(self.app.user[0], self.score, self.category)
        for w in self.winfo_children():
            w.destroy()
        tk.Label(self, text="Quiz Complete!", font=("Arial", 20, "bold")).pack(pady=30)
        tk.Label(self, text=f"Your score: {self.score}", font=("Arial", 16)).pack(pady=10)
        tk.Button(self, text="Play Again", width=20,
                  command=lambda: self.app.start_quiz(self.category)).pack(pady=5)
        tk.Button(self, text="Leaderboard", width=20,
                  command=self.app.show_leaderboard).pack(pady=5)
        tk.Button(self, text="Main Menu", width=20,
                  command=self.app.show_menu).pack(pady=5)
  
