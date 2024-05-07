import tkinter as tk
from tkinter import messagebox
from tkinter import *


class MenuBar():
    def __init__(self, window):
        #Menu
        self.window = window
        
        self.menubar = tk.Menu(self.window)
        self.window.config(menu=self.menubar)

        #Display Menu
        display = tk.Menu(self.menubar, tearoff=0)
        display.add_command(label="Show Day", command=self.donothing)
        display.add_command(label="Show Week", command=self.donothing)
        display.add_command(label="Show Month", command=self.donothing)
        self.menubar.add_cascade(label="Display", menu=display)

        #File Menu
        file = tk.Menu(self.menubar, tearoff=0)
        file.add_command(label="Open JSON File", command=self.donothing)
        file.add_command(label="Save to JSON File", command=self.donothing)
        self.menubar.add_cascade(label="File", menu=file)

        #Edit Menu
        edit = tk.Menu(self.menubar, tearoff=0)
        edit.add_command(label="Create Recurring Task", command=self.create_task)
        edit.add_command(label="Create Transient Task", command=self.donothing)
        edit.add_command(label="Create Anti-Task", command=self.donothing)
        edit.add_command(label="Edit Task", command=self.donothing)
        edit.add_separator()
        edit.add_command(label="Delete Task", command=self.donothing)
        self.menubar.add_cascade(label="Edit", menu=edit)

    def donothing():
        print()

    def create_task():
        newWindow = CreateWindow

class CreateWindow(tk.Tk):
    def __init__(self, master):
        self.master = master
        self.title("Create Task")
        self.geometry("700x500")
        
        # Labels
        self.label_task_name = tk.Label(master, text="Task Name:")
        self.label_task_type = tk.Label(master, text="Task Type:")
        self.label_start_time = tk.Label(master, text="Start Time (HH:MM):")
        self.label_duration = tk.Label(master, text="Duration (minutes):")
        self.label_start_date = tk.Label(master, text="Start Date (YYYY-MM-DD):")
        self.label_end_date = tk.Label(master, text="End Date (YYYY-MM-DD):")
        
        # Entries
        self.entry_task_name = tk.Entry(master)
        self.entry_task_type = tk.Entry(master)
        self.entry_start_time = tk.Entry(master)
        self.entry_duration = tk.Entry(master)
        self.entry_start_date = tk.Entry(master)
        self.entry_end_date = tk.Entry(master)
        
        # Buttons
        self.button_submit = tk.Button(master, text="Submit", command=self.submit_task)
        
        # Layout
        self.label_task_name.grid(row=0, column=0, sticky="e")
        self.label_task_type.grid(row=1, column=0, sticky="e")
        self.label_start_time.grid(row=2, column=0, sticky="e")
        self.label_duration.grid(row=3, column=0, sticky="e")
        self.label_start_date.grid(row=4, column=0, sticky="e")
        self.label_end_date.grid(row=5, column=0, sticky="e")
        
        self.entry_task_name.grid(row=0, column=1)
        self.entry_task_type.grid(row=1, column=1)
        self.entry_start_time.grid(row=2, column=1)
        self.entry_duration.grid(row=3, column=1)
        self.entry_start_date.grid(row=4, column=1)
        self.entry_end_date.grid(row=5, column=1)
        
        self.button_submit.grid(row=6, columnspan=2)
        
    def submit_task(self):
        # Retrieve task details from entries
        task_name = self.entry_task_name.get()
        task_type = self.entry_task_type.get()
        start_time = self.entry_start_time.get()
        duration = self.entry_duration.get()
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        
        
        # message box confirming task submission
        messagebox.showinfo("Task Submitted", "Task '{}' submitted successfully!".format(task_name))

#def main():
#    root = tk.Tk()
#    app = MenuWindow(root)
#    root.mainloop()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Scheduling System (PSS)")
        self.geometry("700x500")

        menubar = MenuBar(self)
        

if __name__ == "__main__":
    app=MainWindow()
    app.mainloop()
