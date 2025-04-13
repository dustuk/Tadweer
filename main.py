import tkinter as tk
from tkinter import messagebox
import json
import os

# ملف لحفظ المهام
TODO_FILE = "tasks.json"

# تحميل المهام من الملف
def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    return []

# حفظ المهام في الملف
def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# إضافة مهمة جديدة
def add_task():
    task_name = entry_task.get()
    if task_name:
        tasks.append({"name": task_name, "completed": False})
        save_tasks(tasks)
        update_task_list()
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("تحذير", "من فضلك أدخل اسم المهمة!")

# تحديث قائمة المهام المعروضة
def update_task_list():
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        status = "✔" if task["completed"] else "❌"
        listbox_tasks.insert(tk.END, f"{task['name']} - {status}")

# تحديد مهمة كمكتملة
def complete_task():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = selected_task_index[0]
        tasks[task_index]["completed"] = True
        save_tasks(tasks)
        update_task_list()
    else:
        messagebox.showwarning("تحذير", "من فضلك اختر مهمة!")

# حذف مهمة
def delete_task():
    selected_task_index = listbox_tasks.curselection()
    if selected_task_index:
        task_index = selected_task_index[0]
        tasks.pop(task_index)
        save_tasks(tasks)
        update_task_list()
    else:
        messagebox.showwarning("تحذير", "من فضلك اختر مهمة!")

# واجهة المستخدم
root = tk.Tk()
root.title("تطبيق إدارة المهام")

# إطار لإدخال المهام
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

entry_task = tk.Entry(frame_input, width=40)
entry_task.pack(side=tk.LEFT, padx=5)

button_add = tk.Button(frame_input, text="إضافة مهمة", command=add_task)
button_add.pack(side=tk.LEFT)

# قائمة المهام
listbox_tasks = tk.Listbox(root, width=50, height=10)
listbox_tasks.pack(pady=10)

# أزرار التحكم
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

button_complete = tk.Button(frame_buttons, text="تحديد كمكتملة", command=complete_task)
button_complete.pack(side=tk.LEFT, padx=5)

button_delete = tk.Button(frame_buttons, text="حذف المهمة", command=delete_task)
button_delete.pack(side=tk.LEFT, padx=5)

# تحميل المهام عند بدء التشغيل
tasks = load_tasks()
update_task_list()

# تشغيل التطبيق
root.mainloop()