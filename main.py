import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

TODO_FILES = {
    "يومي": "daily_tasks.json",
    "أسبوعي": "weekly_tasks.json",
    "شهري": "monthly_tasks.json",
    "سنوي": "yearly_tasks.json"
}

WEEK_DAYS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
          "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
PERIODS = ["صباحًا", "مساءً"]

def load_tasks():
    tasks = {}
    for category, filename in TODO_FILES.items():
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                tasks[category] = json.load(file)
        else:
            tasks[category] = []
    return tasks

def save_tasks(category):
    filename = TODO_FILES[category]
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(tasks[category], file, indent=4, ensure_ascii=False)

def add_task():
    task_name = entry_task.get()
    category = category_var.get()

    if not task_name:
        messagebox.showwarning("تحذير", "من فضلك أدخل اسم المهمة!")
        return

    task_data = {"name": task_name, "completed": False}

    try:
        if category == "يومي":
            hour = daily_hour.get()
            minute = daily_minute.get()
            period = daily_period.get()
            if not (hour and minute and period):
                raise ValueError("يرجى تحديد الوقت بالكامل")
            time_str = f"{hour}:{minute} {period}"
            datetime.strptime(f"{hour}:{minute}", "%I:%M")  # Validate
            task_data["time"] = time_str
        elif category == "أسبوعي":
            day = weekly_day.get()
            if not day:
                raise ValueError("يجب اختيار يوم الأسبوع")
            task_data["day"] = day
        elif category == "شهري":
            day = monthly_day.get()
            if not day:
                raise ValueError("يرجى اختيار يوم الشهر")
            task_data["day"] = int(day)
        elif category == "سنوي":
            day = yearly_day.get()
            month = yearly_month.get()
            if not day or not month:
                raise ValueError("يرجى اختيار اليوم والشهر")
            task_data["day"] = int(day)
            task_data["month"] = month
    except ValueError as e:
        messagebox.showerror("خطأ", str(e))
        return

    if hasattr(entry_task, "edit_index"):
        tasks[category][entry_task.edit_index] = task_data
        del entry_task.edit_index
        button_add.config(text="➕ إضافة")
    else:
        tasks[category].append(task_data)

    save_tasks(category)
    update_task_list()
    entry_task.delete(0, tk.END)
    clear_time_entries()

def clear_time_entries():
    daily_hour.set('')
    daily_minute.set('')
    daily_period.set('')
    weekly_day.set('')
    monthly_day.set('')
    yearly_day.set('')
    yearly_month.set('')

def update_time_frame():
    daily_frame.pack_forget()
    weekly_frame.pack_forget()
    monthly_frame.pack_forget()
    yearly_frame.pack_forget()

    category = category_var.get()
    if category == "يومي":
        daily_frame.pack(side=tk.LEFT, padx=5)
    elif category == "أسبوعي":
        weekly_frame.pack(side=tk.LEFT, padx=5)
    elif category == "شهري":
        monthly_frame.pack(side=tk.LEFT, padx=5)
    elif category == "سنوي":
        yearly_frame.pack(side=tk.LEFT, padx=5)

def update_task_list():
    for widget in list_frame.winfo_children():
        widget.destroy()

    category = category_var.get()

    for index, task in enumerate(tasks[category]):
        row = tk.Frame(list_frame, bg='white', pady=4)
        row.pack(fill=tk.X, padx=5, anchor='e')

        var = tk.BooleanVar(value=task["completed"])

        def toggle_closure(idx=index, var=var):
            tasks[category][idx]["completed"] = var.get()
            save_tasks(category)
            update_task_list()

        def delete_closure(idx=index):
            tasks[category].pop(idx)
            save_tasks(category)
            update_task_list()

        def edit_closure(idx=index):
            task = tasks[category][idx]
            entry_task.delete(0, tk.END)
            entry_task.insert(0, task["name"])
            category_var.set(category)
            update_time_frame()

            if category == "يومي":
                if "time" in task:
                    time_parts = task["time"].split()
                    hour_min = time_parts[0].split(':')
                    daily_hour.set(hour_min[0])
                    daily_minute.set(hour_min[1])
                    daily_period.set(time_parts[1])
            elif category == "أسبوعي":
                weekly_day.set(task.get("day", ''))
            elif category == "شهري":
                monthly_day.set(str(task.get("day", '')))
            elif category == "سنوي":
                yearly_day.set(str(task.get("day", '')))
                yearly_month.set(task.get("month", ''))

            entry_task.edit_index = idx
            button_add.config(text="💾 حفظ التعديل")

        edit_btn = tk.Button(row, text="✏️", fg='blue', command=edit_closure,
                             bd=0, font=('Arial', 16), bg='white')
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(row, text="❌", fg='red', command=delete_closure,
                               bd=0, font=('Arial', 16), bg='white')
        delete_btn.pack(side=tk.LEFT, padx=5)

        checkbox = tk.Checkbutton(
            row,
            variable=var,
            command=toggle_closure,
            bg='white',
            font=('Arial', 16),
            anchor='e'
        )
        checkbox.pack(side=tk.RIGHT, padx=10, fill=tk.X, expand=True)

        detail = task["name"]
        if category == "يومي" and "time" in task:
            detail += f" - الساعة {task['time']}"
        elif category == "أسبوعي" and "day" in task:
            detail += f" - يوم {task['day']}"
        elif category == "شهري" and "day" in task:
            detail += f" - اليوم {task['day']}"
        elif category == "سنوي" and "day" in task and "month" in task:
            detail += f" - {task['day']} {task['month']}"

        label = tk.Label(row, text=detail, anchor='e', bg='white', font=('Arial', 13), justify='right')
        label.pack(side=tk.RIGHT, fill=tk.X, expand=True)

# بدء الواجهة
root = tk.Tk()
root.title("🗓️ إدارة المهام")
root.geometry("800x600")
root.configure(bg='#EAF4F4')

tasks = load_tasks()

title_frame = tk.Frame(root, bg='#2C7A7B', padx=10, pady=10, bd=2, relief=tk.RIDGE)
tk.Label(title_frame, text="📌 إدارة المهام", font=('Cairo', 18, 'bold'), bg='#2C7A7B', fg='white').pack()
title_frame.pack(fill=tk.X, pady=(0, 10))

main_panel = tk.Frame(root, bg='#EAF4F4', padx=10, pady=10)
main_panel.pack(fill=tk.BOTH, expand=True)

input_panel = tk.Frame(main_panel, bg='white', padx=15, pady=15, bd=2, relief=tk.GROOVE)
input_panel.pack(side=tk.LEFT, fill=tk.Y, pady=5, padx=5)

task_frame = tk.Frame(input_panel, bg='white')
task_frame.pack(side=tk.TOP, pady=10)

tk.Label(task_frame, text="📝 مهمة جديدة", bg='white', font=('Cairo', 12, 'bold')).pack(anchor='w')
entry_task = tk.Entry(task_frame, width=30, font=('Cairo', 11), relief=tk.FLAT, highlightthickness=1, highlightbackground='#B2DFDB')
entry_task.pack(pady=5)

button_add = tk.Button(task_frame, text="➕ إضافة", command=add_task, bg='#38B2AC', fg='white',
                       font=('Cairo', 11), bd=0, relief=tk.RIDGE, padx=5, pady=3)
button_add.pack(fill=tk.X)

category_frame = tk.Frame(input_panel, bg='white')
category_frame.pack(side=tk.TOP, pady=10)

tk.Label(category_frame, text="📅 نوع المهمة", bg='white', font=('Cairo', 11, 'bold')).pack(anchor='w')
category_var = tk.StringVar(value="يومي")
categories = ["يومي", "أسبوعي", "شهري", "سنوي"]
for cat in categories:
    tk.Radiobutton(category_frame, text=cat, variable=category_var,
                   value=cat, command=lambda: [update_time_frame(), update_task_list()],
                   bg='white', anchor='w', font=('Cairo', 10)).pack(anchor='w')

time_frame = tk.Frame(input_panel, bg='white')
time_frame.pack(side=tk.TOP, pady=10)

daily_frame = tk.Frame(time_frame, bg='white')
tk.Label(daily_frame, text="الساعة", bg='white').pack(side=tk.RIGHT)
daily_hour = ttk.Combobox(daily_frame, values=[f"{i:02}" for i in range(1, 13)], width=3, state="readonly")
daily_hour.pack(side=tk.RIGHT, padx=2)
tk.Label(daily_frame, text="الدقيقة", bg='white').pack(side=tk.RIGHT)
daily_minute = ttk.Combobox(daily_frame, values=[f"{i:02}" for i in range(0, 60)], width=3, state="readonly")
daily_minute.pack(side=tk.RIGHT, padx=2)
daily_period = ttk.Combobox(daily_frame, values=PERIODS, width=6, state="readonly")
daily_period.pack(side=tk.RIGHT, padx=2)

weekly_frame = tk.Frame(time_frame, bg='white')
tk.Label(weekly_frame, text="يوم الأسبوع", bg='white').pack(side=tk.RIGHT)
weekly_day = ttk.Combobox(weekly_frame, values=WEEK_DAYS, state="readonly", width=12)
weekly_day.pack(side=tk.RIGHT)

monthly_frame = tk.Frame(time_frame, bg='white')
tk.Label(monthly_frame, text="يوم الشهر", bg='white').pack(side=tk.RIGHT)
monthly_day = ttk.Combobox(monthly_frame, values=[str(i) for i in range(1, 32)], state="readonly", width=5)
monthly_day.pack(side=tk.RIGHT)

yearly_frame = tk.Frame(time_frame, bg='white')
tk.Label(yearly_frame, text="يوم", bg='white').pack(side=tk.RIGHT)
yearly_day = ttk.Combobox(yearly_frame, values=[str(i) for i in range(1, 32)], width=5, state="readonly")
yearly_day.pack(side=tk.RIGHT)
tk.Label(yearly_frame, text="شهر", bg='white').pack(side=tk.RIGHT, padx=(5, 0))
yearly_month = ttk.Combobox(yearly_frame, values=MONTHS, state="readonly", width=10)
yearly_month.pack(side=tk.RIGHT)

tasks_frame = tk.Frame(main_panel, bg='white', padx=10, pady=10, bd=2, relief=tk.GROOVE)
tasks_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=5, padx=5)

task_label = tk.Label(tasks_frame, text="📋 قائمة المهام", bg='white',
                      font=('Cairo', 13, 'bold'), anchor='center')
task_label.pack(fill=tk.X, pady=(0, 10))

canvas = tk.Canvas(tasks_frame, bg='white', highlightthickness=0)
scrollbar = tk.Scrollbar(tasks_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = tk.Frame(canvas, bg='white')
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
scrollbar.pack(side="left", fill="y")
canvas.pack(side="right", fill="both", expand=True)
list_frame = scrollable_frame

update_time_frame()
update_task_list()
root.mainloop()
