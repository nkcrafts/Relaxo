# Focus Forge

A beginner-friendly focus planner for a first GitHub project. The app helps you add a small set of goals, choose one active task, and run a timed focus session in the browser.

## Features

- Add and remove goals for the day
- Mark goals as complete or select one as the active task
- Run a focus timer with start, pause, and reset controls
- Save progress in the browser with localStorage
- Works on desktop and mobile

## Requirements

- Python 3.x

## Run

```bash
python server.py
```

Then open `http://localhost:8000` in your browser.

## Usage

1. Add a few goals for the day.
2. Pick one goal to make it active.
3. Set your session length and press `Start`.
4. Use `Pause` or `Reset` if you need to stop the timer.
5. Mark goals complete as you finish them.

## GitHub Push Instructions

1. Install Git on your machine if needed: https://git-scm.com/downloads
2. Open a terminal in this folder: `c:\Users\NKailasam\Desktop\Projects`
3. Initialize Git and commit:

```bash
git init
git add .
git commit -m "Initial commit"
```

4. Add your GitHub remote and push:

```bash
git remote add origin https://github.com/your-username/your-repo.git
git branch -M main
git push -u origin main
```

Replace `your-username` and `your-repo` with your repository details.
