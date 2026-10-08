# Quiz Game

A desktop quiz game built with **Python, Tkinter and SQLite**. Players register, log in, pick a category, answer timed multiple-choice questions, and compete on a leaderboard.

## Features
- User registration and login (passwords stored as SHA-256 hashes)
- 3 categories: Science, GK, Tech (30 sample questions)
- 10 random questions per round
- 15-second timer per question
- Score with speed bonus and streak bonus
- Top 10 leaderboard
- Admin screen to add new questions (log in with a user named `admin`)

## Tech Used
- Python 3
- Tkinter (GUI)
- SQLite (database)

## How to Run
1. Install Python 3.8+
2. Download or clone this repository
3. Run:
   ```
   python main.py
   ```
The database (`quiz.db`) is created automatically on first run.

## Project Structure
```
quiz-game/
├── main.py          # App window, login, menu, admin
├── database.py      # SQLite tables and queries
├── quiz.py          # Quiz screen with timer and scoring
├── leaderboard.py   # Top 10 leaderboard
├── requirements.txt
└── README.md
```

## Scoring
- Correct answer: 10 points
- Speed bonus: up to +5 (time left / 3)
- Streak bonus: +2 for 3 or more correct in a row

## Author
SIVANESAN T
