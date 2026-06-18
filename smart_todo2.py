import customtkinter as ctk
from tkinter import messagebox
import random

# -----------------------------
# APP SETTINGS
# -----------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart Productivity Tracker")
app.geometry("850x650")

# -----------------------------
# DATA STORAGE
# -----------------------------

tasks = []
xp = 0

# -----------------------------
# LEVEL FUNCTION
# -----------------------------

def get_level(xp):
    if xp < 50:
        return 1
    elif xp < 100:
        return 2
    elif xp < 150:
        return 3
    elif xp < 200:
        return 4
    else:
        return 5

# -----------------------------
# UPDATE DISPLAY
# -----------------------------

def update_tasks():

    task_box.delete("0.0", "end")

    if len(tasks) == 0:
        task_box.insert("end", "No Tasks Available")
        return

    for i, task in enumerate(tasks, start=1):

        task_box.insert(
            "end",
            f"{i}. {task['title']} | {task['status']}\n"
        )

# -----------------------------
# UPDATE STATS
# -----------------------------

def update_stats():

    level = get_level(xp)

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["status"] == "Completed"
    )

    stats_label.configure(
        text=f"""
XP : {xp}
Level : {level}
Total Tasks : {total}
Completed : {completed}
"""
    )

# -----------------------------
# ADD TASK
# -----------------------------

def add_task():

    task_name = task_entry.get()

    if task_name.strip() == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a task"
        )
        return

    task = {
        "title": task_name,
        "status": "Pending"
    }

    tasks.append(task)

    task_entry.delete(0, "end")

    update_tasks()
    update_stats()

    messagebox.showinfo(
        "Success",
        "Task Added Successfully!"
    )

# -----------------------------
# DELETE TASK
# -----------------------------

def delete_task():

    try:

        index = int(task_number.get()) - 1

        if 0 <= index < len(tasks):

            deleted = tasks.pop(index)

            update_tasks()
            update_stats()

            messagebox.showinfo(
                "Deleted",
                f"{deleted['title']} deleted"
            )

        else:
            messagebox.showerror(
                "Error",
                "Invalid task number"
            )

    except:
        messagebox.showerror(
            "Error",
            "Enter valid task number"
        )

# -----------------------------
# COMPLETE TASK
# -----------------------------

def complete_task():

    global xp

    try:

        index = int(task_number.get()) - 1

        if not (0 <= index < len(tasks)):
            messagebox.showerror(
                "Error",
                "Invalid task number"
            )
            return

        if tasks[index]["status"] == "Completed":

            messagebox.showinfo(
                "Info",
                "Task already completed"
            )
            return

        # -----------------
        # MATH CHALLENGE
        # -----------------

        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)

        dialog = ctk.CTkInputDialog(
            text=f"Solve this to complete task:\n\n{num1} + {num2} = ?",
            title="Task Verification"
        )

        answer = dialog.get_input()

        if answer is None:
            return

        if int(answer) == (num1 + num2):

            tasks[index]["status"] = "Completed"

            xp += 10

            update_tasks()
            update_stats()

            messagebox.showinfo(
                "Success",
                "Challenge Passed!\nTask Completed!\n+10 XP"
            )

        else:

            messagebox.showerror(
                "Failed",
                "Wrong Answer!\nTask remains pending."
            )

    except:
        messagebox.showerror(
            "Error",
            "Please enter valid numbers."
        )

# -----------------------------
# SUMMARY
# -----------------------------

def show_summary():

    total = len(tasks)

    completed = sum(
        1 for task in tasks
        if task["status"] == "Completed"
    )

    pending = total - completed

    level = get_level(xp)

    messagebox.showinfo(
        "Productivity Summary",
        f"""
Total Tasks : {total}

Completed : {completed}

Pending : {pending}

XP : {xp}

Level : {level}
"""
    )

# -----------------------------
# TITLE
# -----------------------------

title = ctk.CTkLabel(
    app,
    text="🚀 SMART PRODUCTIVITY TRACKER",
    font=("Arial", 28, "bold")
)

title.pack(pady=15)

# -----------------------------
# TASK ENTRY
# -----------------------------

task_entry = ctk.CTkEntry(
    app,
    width=500,
    placeholder_text="Enter your task..."
)

task_entry.pack(pady=10)

add_btn = ctk.CTkButton(
    app,
    text="➕ Add Task",
    command=add_task,
    width=200
)

add_btn.pack(pady=5)

# -----------------------------
# TASK BOX
# -----------------------------

task_box = ctk.CTkTextbox(
    app,
    width=700,
    height=250
)

task_box.pack(pady=20)

# -----------------------------
# TASK NUMBER
# -----------------------------

task_number = ctk.CTkEntry(
    app,
    width=250,
    placeholder_text="Enter Task Number"
)

task_number.pack(pady=10)

# -----------------------------
# BUTTON FRAME
# -----------------------------

button_frame = ctk.CTkFrame(app)

button_frame.pack(pady=10)

complete_btn = ctk.CTkButton(
    button_frame,
    text="✅ Complete Task",
    command=complete_task
)

complete_btn.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

delete_btn = ctk.CTkButton(
    button_frame,
    text="🗑 Delete Task",
    command=delete_task
)

delete_btn.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)

summary_btn = ctk.CTkButton(
    button_frame,
    text="📊 Summary",
    command=show_summary
)

summary_btn.grid(
    row=0,
    column=2,
    padx=10,
    pady=10
)

# -----------------------------
# STATS PANEL
# -----------------------------

stats_label = ctk.CTkLabel(
    app,
    text="",
    font=("Arial", 18)
)

stats_label.pack(pady=20)

update_stats()

# -----------------------------
# RUN APP
# -----------------------------

app.mainloop()