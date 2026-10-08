import tkinter as tk
from tkinter import ttk
import database as db


class LeaderboardScreen(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        tk.Label(self, text="Top 10 Leaderboard", font=("Arial", 18, "bold")).pack(pady=15)

        cols = ("Rank", "Player", "Score", "Category", "Date")
        tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        widths = (50, 110, 60, 90, 150)
        for col, w in zip(cols, widths):
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")
        tree.pack(padx=10)

        for rank, (user, score, cat, date) in enumerate(db.top_scores(10), start=1):
            tree.insert("", "end", values=(rank, user, score, cat, date))

        tk.Button(self, text="Back", width=15, command=app.show_menu).pack(pady=15)
      
