import tkinter as tk
from tkinter import messagebox, simpledialog
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
Path('logs').mkdir(exist_ok=True)

logger.info("Starting Focus Buddy application")

# These are the values we use for the timing.
work_time_minutes = 60
break_time_minutes = 5
remaining_seconds = 0
break_window = None
timer_label = None
extend_button = None
remind_again_minutes = 10

PALETTE = {
    "bg": "#FFF8F2",
    "surface": "#FFFFFF",
    "header": "#FFB8D1",
    "accent": "#FF7BA3",
    "accent_dark": "#E95B86",
    "mint": "#B8F2E6",
    "sky": "#B9E6FF",
    "sun": "#FFE08A",
    "text": "#3B2F36",
    "muted": "#7D6A74",
    "border": "#F4D9E3",
}


def ask_number(title, question, default):
    """Ask the user for a number. If they cancel, return the default."""
    try:
        value = simpledialog.askinteger(title, question, initialvalue=default, minvalue=1)
        if value is None:
            return default
        logger.info(f"User set {title.lower()}: {value} minutes")
        return value
    except Exception as e:
        logger.error(f"Error in ask_number: {e}")
        return default


def start_app():
    """Start the application and ask for the work/break times."""
    global work_time_minutes, break_time_minutes
    
    try:
        root = tk.Tk()
        root.title("Focus Buddy ✿")
        root.configure(bg=PALETTE["bg"])
        root.geometry("420x320")
        root.resizable(False, False)

        canvas = tk.Canvas(root, width=420, height=320, bg=PALETTE["bg"], highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_oval(-40, -40, 130, 130, fill=PALETTE["mint"], outline=PALETTE["mint"])
        canvas.create_oval(310, -10, 470, 150, fill=PALETTE["sky"], outline=PALETTE["sky"])
        canvas.create_oval(285, 225, 455, 395, fill=PALETTE["sun"], outline=PALETTE["sun"])

    card = tk.Frame(
        root,
        bg=PALETTE["surface"],
        highlightbackground=PALETTE["border"],
        highlightthickness=2,
        bd=0,
    )
    card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=250)

    top_strip = tk.Frame(card, bg=PALETTE["header"], height=14)
    top_strip.pack(fill="x")

    content = tk.Frame(card, bg=PALETTE["surface"])
    content.pack(fill="both", expand=True, padx=22, pady=18)

    tk.Label(
        content,
        text="Focus Buddy ✿",
        bg=PALETTE["surface"],
        fg=PALETTE["accent_dark"],
        font=("Segoe UI", 22, "bold"),
    ).pack(pady=(0, 8))

    tk.Label(
        content,
        text="｡･:*:･ﾟ✧ ｡･:*:･ﾟ✧",
        bg=PALETTE["surface"],
        fg=PALETTE["header"],
        font=("Segoe UI", 10, "bold"),
    ).pack(pady=(0, 4))

    tk.Label(
        content,
        text="A tiny, cheerful break reminder for soft focus sessions and cozy little wins.",
        bg=PALETTE["surface"],
        fg=PALETTE["muted"],
        font=("Segoe UI", 10),
        wraplength=300,
        justify="center",
    ).pack(pady=(0, 16))

    accent_row = tk.Frame(content, bg=PALETTE["surface"])
    accent_row.pack(fill="x", pady=(0, 18))
    for color in (PALETTE["mint"], PALETTE["sky"], PALETTE["sun"]):
        dot = tk.Canvas(accent_row, width=22, height=22, bg=PALETTE["surface"], highlightthickness=0)
        dot.create_oval(2, 2, 20, 20, fill=color, outline=color)
        dot.pack(side="left", expand=True)

    work_time_minutes = ask_number(
        "Work time",
        "How many minutes should you work before the reminder?",
        60,
    )
    break_time_minutes = ask_number(
        "Break time",
        "How many minutes should the break last?",
        5,
    )

        root.after(100, lambda: start_work_timer(root))
        root.mainloop()
        logger.info("Application closed")
    except tk.TclError as e:
        logger.error(f"Tkinter error: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in start_app: {e}", exc_info=True)
        raise


def start_work_timer(root):
    """Set the timer for the work interval and show a notice."""
    messagebox.showinfo("Timer started", f"Your pastel focus timer is ready. The reminder will appear after {work_time_minutes} minutes.")
    root.after(work_time_minutes * 60 * 1000, lambda: show_break_popup(root))


def show_break_popup(root):
    """Show the break reminder popup window."""
    global break_window, timer_label, extend_button, remaining_seconds

    if break_window is not None:
        return

    remaining_seconds = break_time_minutes * 60

    break_window = tk.Toplevel(root)
    break_window.title("Please take a little break now ✿")
    break_window.configure(bg=PALETTE["bg"])
    break_window.geometry("460x360")
    break_window.attributes("-topmost", True)
    break_window.resizable(False, False)
    break_window.protocol("WM_DELETE_WINDOW", lambda: None)

    shadow = tk.Frame(break_window, bg="#E6C8D4")
    shadow.place(x=12, y=12, width=436, height=336)

    shell = tk.Frame(
        break_window,
        bg=PALETTE["surface"],
        highlightbackground=PALETTE["border"],
        highlightthickness=2,
        bd=0,
    )
    shell.place(x=8, y=8, width=436, height=336)

    header = tk.Frame(shell, bg=PALETTE["header"], height=48, relief="raised", bd=1)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Please take a little break now ✿",
        bg=PALETTE["header"],
        fg="#FFFFFF",
        font=("Segoe UI", 13, "bold"),
    ).pack(pady=10)

    message = (
        "Please take a little break now.\n\n"
        "If you are not ready yet, choose how many more minutes you want to work."
    )
    label = tk.Label(
        shell,
        text=message,
        wraplength=370,
        justify="center",
        bg=PALETTE["surface"],
        fg=PALETTE["text"],
        font=("Segoe UI", 12),
    )
    label.pack(padx=24, pady=(22, 14))

    bubble_row = tk.Frame(shell, bg=PALETTE["surface"])
    bubble_row.pack(pady=(0, 12))
    for color in (PALETTE["mint"], PALETTE["sky"], PALETTE["sun"], PALETTE["header"]):
        bubble = tk.Canvas(bubble_row, width=18, height=18, bg=PALETTE["surface"], highlightthickness=0)
        bubble.create_oval(2, 2, 16, 16, fill=color, outline=color)
        bubble.pack(side="left", padx=6)

    button_frame = tk.Frame(shell, bg=PALETTE["surface"])
    button_frame.pack(pady=10)

    yes_break = tk.Button(
        button_frame,
        text="yes, break time",
        command=lambda: start_break(break_window),
        bg=PALETTE["mint"],
        fg=PALETTE["text"],
        activebackground="#9EE8D8",
        activeforeground=PALETTE["text"],
        relief="raised",
        bd=2,
        font=("Segoe UI", 10, "bold"),
        padx=14,
        pady=8,
    )
    yes_break.pack(side="left", padx=6)

    no_break = tk.Button(
        button_frame,
        text="remind me later",
        command=lambda: remind_me_later(root),
        bg=PALETTE["sky"],
        fg=PALETTE["text"],
        activebackground="#9DD6F5",
        activeforeground=PALETTE["text"],
        relief="raised",
        bd=2,
        font=("Segoe UI", 10, "bold"),
        padx=14,
        pady=8,
    )
    no_break.pack(side="left", padx=6)

    sparkles = tk.Label(
        shell,
        text="✿ ｡･:*:･ﾟ★,｡･:*:･ﾟ☆  ✿",
        bg=PALETTE["surface"],
        fg=PALETTE["accent_dark"],
        font=("Segoe UI", 10, "bold"),
    )
    sparkles.pack(pady=(0, 8))

    timer_label = tk.Label(
        shell,
        text="",
        font=("Segoe UI", 16, "bold"),
        bg=PALETTE["surface"],
        fg=PALETTE["accent_dark"],
    )
    timer_label.pack(pady=(10, 6))

    extend_button = tk.Button(
        shell,
        text="Extend Break",
        command=extend_break,
        state="disabled",
        bg=PALETTE["header"],
        fg="#FFFFFF",
        activebackground=PALETTE["accent_dark"],
        activeforeground="#FFFFFF",
        relief="raised",
        bd=2,
        font=("Segoe UI", 10, "bold"),
        padx=14,
        pady=8,
    )
    extend_button.pack(pady=(2, 12))


def remind_me_later(root):
    """Ask how many more minutes to work before showing the reminder again."""
    global break_window, remind_again_minutes
    if break_window is not None:
        break_window.destroy()
        break_window = None

    extra_minutes = simpledialog.askinteger(
        "More work time",
        "How many more minutes would you like before I show the reminder again?",
        initialvalue=remind_again_minutes,
        minvalue=1,
    )

    if extra_minutes is None:
        extra_minutes = remind_again_minutes

    remind_again_minutes = extra_minutes

    root.after(extra_minutes * 60 * 1000, lambda: show_break_popup(root))


def postpone_break(root):
    """Keep backward compatibility with the earlier flow."""
    remind_me_later(root)


def start_break(parent):
    """Start the break countdown timer."""
    global extend_button
    extend_button.config(state="normal")
    update_timer(parent)


def update_timer(parent):
    """Update the timer label every second."""
    global remaining_seconds, timer_label

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60
    timer_label.config(text=f"Break time remaining: {minutes:02d}:{seconds:02d}")

    if remaining_seconds <= 0:
        finish_break(parent)
        return

    remaining_seconds -= 1
    parent.after(1000, lambda: update_timer(parent))


def extend_break():
    """Allow the user to add more minutes to the current break."""
    global remaining_seconds

    extra = simpledialog.askinteger(
        "Extra break",
        "Add a few more minutes to your break:",
        initialvalue=1,
        minvalue=1,
    )

    if extra is not None:
        remaining_seconds += extra * 60
        timer_label.config(
            text=f"Break time remaining: {remaining_seconds // 60:02d}:{remaining_seconds % 60:02d}"
        )
        messagebox.showinfo("Extended", f"Break extended by {extra} minutes.")


def finish_break(parent):
    """Close the break window and end the program."""
    global break_window
    try:
        if break_window is not None:
            break_window.destroy()
            break_window = None

        messagebox.showinfo("Break finished", "Your break is over. You can return to work now.")
        parent.quit()
    except Exception as e:
        logger.error(f"Error finishing break: {e}")
        parent.quit()


if __name__ == "__main__":
    try:
        start_app()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        messagebox.showerror("Error", f"An error occurred: {e}")
        sys.exit(1)
