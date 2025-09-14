import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, font
import datetime
import json
import os

DATA_FILE = "tasks_data.json"

class TaskManagerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.root.geometry("650x560")
        self.root.configure(bg="#f0f4f8")

        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.btn_font = font.Font(family="Arial", size=11, weight="bold")

        self.banner = tk.Label(
            self.root,
            text="Welcome! Stay productive today.",
            bg="#4f8cff",
            fg="white",
            font=self.title_font,
            pady=12,
            padx=10
        )
        self.banner.pack(fill=tk.X, pady=(18, 10))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Daily Tab
        self.daily_frame = tk.Frame(self.notebook, bg="#f0f4f8")
        self.notebook.add(self.daily_frame, text="Daily Tasks")
        self.setup_daily_tab()

        # Weekly Tab
        self.weekly_frame = tk.Frame(self.notebook, bg="#f0f4f8")
        self.notebook.add(self.weekly_frame, text="Weekly Tasks")
        self.setup_weekly_tab()

        # Monthly Tab
        self.monthly_frame = tk.Frame(self.notebook, bg="#f0f4f8")
        self.notebook.add(self.monthly_frame, text="Monthly Tasks")
        self.setup_monthly_tab()

        # Casual Tab
        self.casual_frame = tk.Frame(self.notebook, bg="#f0f4f8")
        self.notebook.add(self.casual_frame, text="Casual Reminders")
        self.setup_casual_tab()

        self.footer = tk.Label(
            self.root,
            text="Tip: Stay hydrated and active!",
            bg="#f0f4f8",
            fg="#888",
            font=("Arial", 10)
        )
        self.footer.pack(side=tk.BOTTOM, pady=10)

        self.load_data()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # Daily Tab
    def setup_daily_tab(self):
        tk.Label(self.daily_frame, text="Drink 5L Water", bg="#f0f4f8", font=self.btn_font).pack(pady=(10,0))
        self.water_var = tk.DoubleVar(value=0)
        self.water_bar = ttk.Progressbar(self.daily_frame, maximum=5, variable=self.water_var, length=400)
        self.water_bar.pack(pady=5)
        tk.Button(self.daily_frame, text="Add 0.5L", command=self.add_water, font=self.btn_font, bg="#4f8cff", fg="white").pack(pady=5)

        tk.Label(self.daily_frame, text="Walk 10,000 Steps", bg="#f0f4f8", font=self.btn_font).pack(pady=(20,0))
        self.steps_var = tk.IntVar(value=0)
        self.steps_bar = ttk.Progressbar(self.daily_frame, maximum=10000, variable=self.steps_var, length=400)
        self.steps_bar.pack(pady=5)
        tk.Button(self.daily_frame, text="Add 500 Steps", command=self.add_steps, font=self.btn_font, bg="#43d19e", fg="white").pack(pady=5)

    def add_water(self):
        if self.water_var.get() < 5:
            self.water_var.set(round(self.water_var.get() + 0.5, 1))
            if self.water_var.get() >= 5:
                messagebox.showinfo("Congratulations!", "You completed your water goal for today!")
        self.save_data()

    def add_steps(self):
        if self.steps_var.get() < 10000:
            self.steps_var.set(self.steps_var.get() + 500)
            if self.steps_var.get() >= 10000:
                messagebox.showinfo("Congratulations!", "You completed your steps goal for today!")
        self.save_data()

    # Weekly Tab
    def setup_weekly_tab(self):
        tk.Label(self.weekly_frame, text="Assignments", bg="#f0f4f8", font=self.btn_font).pack(pady=(10,0))
        self.weekly_listbox = tk.Listbox(self.weekly_frame, width=50, height=8, font=("Arial", 12), bg="#eaf0fa")
        self.weekly_listbox.pack(pady=10)
        tk.Button(self.weekly_frame, text="Add Assignment", command=self.add_weekly_task, font=self.btn_font, bg="#4f8cff", fg="white").pack(pady=5)
        tk.Button(self.weekly_frame, text="Remove Assignment", command=self.remove_weekly_task, font=self.btn_font, bg="#ff6f61", fg="white").pack(pady=5)
        self.weekly_progress_var = tk.IntVar(value=0)
        self.weekly_progress_bar = ttk.Progressbar(self.weekly_frame, maximum=5, variable=self.weekly_progress_var, length=400)
        self.weekly_progress_bar.pack(pady=10)
        tk.Button(self.weekly_frame, text="Mark Assignment Done", command=self.mark_weekly_done, font=self.btn_font, bg="#43d19e", fg="white").pack(pady=5)

    def add_weekly_task(self):
        task = simpledialog.askstring("Add Assignment", "Enter assignment description:")
        if task:
            due_day = simpledialog.askstring("Due Day", "Enter due day (1-31):")
            try:
                now = datetime.datetime.now()
                due = datetime.datetime(now.year, now.month, int(due_day), 0, 0)
                self.weekly_listbox.insert(
                    tk.END,
                    f"{task} (Due: {due.strftime('%Y-%m-%d %H:%M')}, Added: {now.strftime('%Y-%m-%d %H:%M')})"
                )
                self.save_data()
            except Exception:
                messagebox.showerror("Error", "Invalid day.")

    def remove_weekly_task(self):
        selected = self.weekly_listbox.curselection()
        if selected:
            self.weekly_listbox.delete(selected)
            self.weekly_progress_var.set(self.weekly_progress_var.get() + 1)
            if self.weekly_progress_var.get() >= 5:
                messagebox.showinfo("Congratulations!", "You completed all weekly assignments!")
            self.save_data()

    def mark_weekly_done(self):
        if self.weekly_progress_var.get() < 5:
            self.weekly_progress_var.set(self.weekly_progress_var.get() + 1)
            if self.weekly_progress_var.get() >= 5:
                messagebox.showinfo("Congratulations!", "You completed all weekly assignments!")
            self.save_data()

    # Monthly Tab
    def setup_monthly_tab(self):
        tk.Label(self.monthly_frame, text="Exams & Important Dates", bg="#f0f4f8", font=self.btn_font).pack(pady=(10,0))
        self.monthly_listbox = tk.Listbox(self.monthly_frame, width=50, height=8, font=("Arial", 12), bg="#eaf0fa")
        self.monthly_listbox.pack(pady=10)
        tk.Button(self.monthly_frame, text="Add Exam/Date", command=self.add_monthly_task, font=self.btn_font, bg="#4f8cff", fg="white").pack(pady=5)
        tk.Button(self.monthly_frame, text="Remove Exam/Date", command=self.remove_monthly_task, font=self.btn_font, bg="#ff6f61", fg="white").pack(pady=5)
        self.monthly_progress_var = tk.IntVar(value=0)
        self.monthly_progress_bar = ttk.Progressbar(self.monthly_frame, maximum=3, variable=self.monthly_progress_var, length=400)
        self.monthly_progress_bar.pack(pady=10)
        tk.Button(self.monthly_frame, text="Mark Exam/Date Done", command=self.mark_monthly_done, font=self.btn_font, bg="#43d19e", fg="white").pack(pady=5)

    def add_monthly_task(self):
        task = simpledialog.askstring("Add Exam/Date", "Enter event description:")
        if task:
            due_day = simpledialog.askstring("Event Day", "Enter day (1-31):")
            try:
                now = datetime.datetime.now()
                due = datetime.datetime(now.year, now.month, int(due_day), 0, 0)
                self.monthly_listbox.insert(
                    tk.END,
                    f"{task} (On: {due.strftime('%Y-%m-%d %H:%M')}, Added: {now.strftime('%Y-%m-%d %H:%M')})"
                )
                self.save_data()
            except Exception:
                messagebox.showerror("Error", "Invalid day.")

    def remove_monthly_task(self):
        selected = self.monthly_listbox.curselection()
        if selected:
            self.monthly_listbox.delete(selected)
            self.monthly_progress_var.set(self.monthly_progress_var.get() + 1)
            if self.monthly_progress_var.get() >= 3:
                messagebox.showinfo("Congratulations!", "You completed all monthly tasks!")
            self.save_data()

    def mark_monthly_done(self):
        if self.monthly_progress_var.get() < 3:
            self.monthly_progress_var.set(self.monthly_progress_var.get() + 1)
            if self.monthly_progress_var.get() >= 3:
                messagebox.showinfo("Congratulations!", "You completed all monthly tasks!")
            self.save_data()

    # Casual Tab
    def setup_casual_tab(self):
        tk.Label(self.casual_frame, text="Casual Reminders (Birthdays, etc.)", bg="#f0f4f8", font=self.btn_font).pack(pady=(10,0))
        self.casual_listbox = tk.Listbox(self.casual_frame, width=50, height=8, font=("Arial", 12), bg="#eaf0fa")
        self.casual_listbox.pack(pady=10)
        tk.Button(self.casual_frame, text="Add Reminder", command=self.add_casual_task, font=self.btn_font, bg="#4f8cff", fg="white").pack(pady=5)
        tk.Button(self.casual_frame, text="Remove Reminder", command=self.remove_casual_task, font=self.btn_font, bg="#ff6f61", fg="white").pack(pady=5)
        self.casual_progress_var = tk.IntVar(value=0)
        self.casual_progress_bar = ttk.Progressbar(self.casual_frame, maximum=2, variable=self.casual_progress_var, length=400)
        self.casual_progress_bar.pack(pady=10)
        tk.Button(self.casual_frame, text="Mark Reminder Done", command=self.mark_casual_done, font=self.btn_font, bg="#43d19e", fg="white").pack(pady=5)

    def add_casual_task(self):
        task = simpledialog.askstring("Add Reminder", "Enter reminder (e.g., Birthday):")
        if task:
            due_day = simpledialog.askstring("Event Day", "Enter day (1-31):")
            try:
                now = datetime.datetime.now()
                due = datetime.datetime(now.year, now.month, int(due_day), 0, 0)
                self.casual_listbox.insert(
                    tk.END,
                    f"{task} (On: {due.strftime('%Y-%m-%d %H:%M')}, Added: {now.strftime('%Y-%m-%d %H:%M')})"
                )
                self.save_data()
            except Exception:
                messagebox.showerror("Error", "Invalid day.")

    def remove_casual_task(self):
        selected = self.casual_listbox.curselection()
        if selected:
            self.casual_listbox.delete(selected)
            self.casual_progress_var.set(self.casual_progress_var.get() + 1)
            if self.casual_progress_var.get() >= 2:
                messagebox.showinfo("Congratulations!", "You completed all casual reminders!")
            self.save_data()

    def mark_casual_done(self):
        if self.casual_progress_var.get() < 2:
            self.casual_progress_var.set(self.casual_progress_var.get() + 1)
            if self.casual_progress_var.get() >= 2:
                messagebox.showinfo("Congratulations!", "You completed all casual reminders!")
            self.save_data()

    def save_data(self):
        data = {
            "water": self.water_var.get(),
            "steps": self.steps_var.get(),
            "weekly_tasks": list(self.weekly_listbox.get(0, tk.END)),
            "weekly_progress": self.weekly_progress_var.get(),
            "monthly_tasks": list(self.monthly_listbox.get(0, tk.END)),
            "monthly_progress": self.monthly_progress_var.get(),
            "casual_tasks": list(self.casual_listbox.get(0, tk.END)),
            "casual_progress": self.casual_progress_var.get()
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            self.water_var.set(data.get("water", 0))
            self.steps_var.set(data.get("steps", 0))
            self.weekly_listbox.delete(0, tk.END)
            for item in data.get("weekly_tasks", []):
                self.weekly_listbox.insert(tk.END, item)
            self.weekly_progress_var.set(data.get("weekly_progress", 0))
            self.monthly_listbox.delete(0, tk.END)
            for item in data.get("monthly_tasks", []):
                self.monthly_listbox.insert(tk.END, item)
            self.monthly_progress_var.set(data.get("monthly_progress", 0))
            self.casual_listbox.delete(0, tk.END)
            for item in data.get("casual_tasks", []):
                self.casual_listbox.insert(tk.END, item)
            self.casual_progress_var.set(data.get("casual_progress", 0))

    def on_close(self):
        self.save_data()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TaskManagerUI()
    app.run()