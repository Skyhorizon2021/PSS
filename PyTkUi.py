import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

class Task:
    def __init__(self, name="", task_type="", start_time="", duration="", day=None, month=None, year=None, start_day=None, start_month=None, start_year=None, end_day=None, end_month=None, end_year=None, frequency=None):
        self.name = name
        self.task_type = task_type
        self.start_time = start_time
        self.duration = duration
        self.day = day
        self.month = month
        self.year = year
        self.start_day = start_day
        self.start_month = start_month
        self.start_year = start_year
        self.end_day = end_day
        self.end_month = end_month
        self.end_year = end_year
        self.frequency = frequency

class MenuBar():
    def __init__(self, window):
        #Menu
        window = window
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
        file.add_command(label="Open JSON File", command=self.upload_file)
        file.add_command(label="Save to JSON File", command=self.donothing)
        self.menubar.add_cascade(label="File", menu=file)

        #Edit Menu
        edit = tk.Menu(self.menubar, tearoff=0)
        edit.add_command(label="Create Recurring Task", command=self.create_recurring_task)
        edit.add_command(label="Create Transient Task", command=self.create_transient_task)
        edit.add_command(label="Create Anti-Task", command=self.create_anti_task)
        edit.add_command(label="Edit Task", command=self.donothing)
        edit.add_separator()
        edit.add_command(label="Delete Task", command=self.donothing)
        self.menubar.add_cascade(label="Edit", menu=edit)

    def create_recurring_task(self):
        newWindow = RecurringTaskWindow()

    def create_transient_task(self):
        newWindow = TransientTaskWindow()

    def create_anti_task(self):
        newWindow = AntiTaskWindow()


    def donothing(self):
        print()

    def upload_file(self):
        newWindow = FileWindow()

    def create_task(self):
        newWindow = CreateWindow()

class CreateWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Task")
        self.geometry("400x250")  # Increased height to accommodate new fields

        frame = Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Labels
        self.label_task_name = tk.Label(frame, text="Task Name:")
        self.label_task_type = tk.Label(frame, text="Task Type:")
        self.label_start_time = tk.Label(frame, text="Start Time (HH:MM):")
        self.label_duration = tk.Label(frame, text="Duration (minutes):")

        # New labels for date fields
        self.label_day = tk.Label(frame, text="Day (DD):")
        self.label_month = tk.Label(frame, text="Month (MM):")
        self.label_year = tk.Label(frame, text="Year (YYYY):")

        # Entries
        self.entry_task_name = tk.Entry(frame)
        self.entry_task_type = tk.Entry(frame)
        self.entry_start_time = tk.Entry(frame)
        self.entry_duration = tk.Entry(frame)

        # New entries for date fields
        self.entry_day = tk.Entry(frame)
        self.entry_month = tk.Entry(frame)
        self.entry_year = tk.Entry(frame)

        # Buttons
        self.button_submit = tk.Button(frame, text="Submit", command=self.submit_task)

        # Layout
        self.label_task_name.grid(row=0, column=0, sticky="e", pady=5)
        self.label_start_time.grid(row=1, column=0, sticky="e", pady=5)
        self.label_duration.grid(row=2, column=0, sticky="e", pady=5)

        # New labels layout
        self.label_day.grid(row=3, column=0, sticky="e", pady=5)
        self.label_month.grid(row=4, column=0, sticky="e", pady=5)
        self.label_year.grid(row=5, column=0, sticky="e", pady=5)

        self.entry_task_name.grid(row=0, column=1)
        self.entry_start_time.grid(row=1, column=1)
        self.entry_duration.grid(row=2, column=1)

        # New entries layout
        self.entry_day.grid(row=3, column=1)
        self.entry_month.grid(row=4, column=1)
        self.entry_year.grid(row=5, column=1)

        self.button_submit.grid(row=6, columnspan=2, pady=8)

    def submit_task(self):
        # Retrieve task details from entries
        task_name = self.entry_task_name.get()
        task_type = self.entry_task_type.get()
        start_time = self.entry_start_time.get()
        duration = self.entry_duration.get()

        # Retrieve date fields
        day = self.entry_day.get()
        month = self.entry_month.get()
        year = self.entry_year.get()

        task = Task(task_name, task_type, start_time, duration, day, month, year)
        # Message box confirming task submission
        messagebox.showinfo("Task Submitted", f"Task '{task_name}' submitted successfully!")

class FileWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("File Upload")
        self.geometry("400x200")

        #button to upload a file
        self.label = tk.Label(self, text="Add Tasks Through JSON File")
        self.button = tk.Button(self, text='Upload your file', command=self.upload)
        self.label.place(relx=.5, rely=.38, anchor = CENTER)
        self.button.place(relx=.5, rely=.5, anchor = CENTER)

    def upload(self):
        filename = filedialog.askopenfilename(title="Choose a file", filetypes= [("JSON files", "*.json")])
        self.file_name = tk.Label(self, text="File name: " + filename)
        print('Selected: ', filename)

class DayFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class WeekFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class MonthFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


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

class TransientTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Transient Task")
        self.geometry("400x300")

    def submit_task(self):
        super().submit_task()
        task = Task(self.entry_task_name.get(), self.entry_task_type.get(), self.entry_start_time.get(), self.entry_duration.get())
        messagebox.showinfo("Task Details", f"Transient Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_task_type.get()}\nStart Time: {self.entry_start_time.get()}\nDuration: {self.entry_duration.get()}")

class AntiTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Anti Task")
        self.geometry("400x300")


    def submit_task(self):
        super().submit_task()
        task = Task(self.entry_task_name.get(), self.entry_task_type.get(), self.entry_start_time.get(), self.entry_duration.get())
        messagebox.showinfo("Task Details", f"Anti Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_task_type.get()}\nStart Time: {self.entry_start_time.get()}\nDuration: {self.entry_duration.get()}")


class RecurringTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Recurring Task")
        self.geometry("400x300")

          # Remove CreateWindow date labels and entry fields
        self.label_day.grid_remove()
        self.label_month.grid_remove()
        self.label_year.grid_remove()
        self.entry_day.grid_remove()
        self.entry_month.grid_remove()
        self.entry_year.grid_remove()


        self.label_start_day = tk.Label(self, text="Start Day:")
        self.label_start_month = tk.Label(self, text="Start Month:")
        self.label_start_year = tk.Label(self, text="Start Year:")
        self.label_end_day = tk.Label(self, text="End Day:")
        self.label_end_month = tk.Label(self, text="End Month:")
        self.label_end_year = tk.Label(self, text="End Year:")
        self.label_frequency = tk.Label(self, text="Frequency (1: Daily, 7: Weekly):")

        self.entry_start_day = tk.Entry(self)
        self.entry_start_month = tk.Entry(self)
        self.entry_start_year = tk.Entry(self)
        self.entry_end_day = tk.Entry(self)
        self.entry_end_month = tk.Entry(self)
        self.entry_end_year = tk.Entry(self)
        self.entry_frequency = tk.Entry(self)

        self.label_start_day.grid(row=3, column=0, sticky="e", pady=5)
        self.label_start_month.grid(row=4, column=0, sticky="e", pady=5)
        self.label_start_year.grid(row=5, column=0, sticky="e", pady=5)
        self.label_end_day.grid(row=6, column=0, sticky="e", pady=5)
        self.label_end_month.grid(row=7, column=0, sticky="e", pady=5)
        self.label_end_year.grid(row=8, column=0, sticky="e", pady=5)
        self.label_frequency.grid(row=9, column=0, sticky="e", pady=5)

        self.entry_start_day.grid(row=3, column=1)
        self.entry_start_month.grid(row=4, column=1)
        self.entry_start_year.grid(row=5, column=1)
        self.entry_end_day.grid(row=6, column=1)
        self.entry_end_month.grid(row=7, column=1)
        self.entry_end_year.grid(row=8, column=1)
        self.entry_frequency.grid(row=9, column=1)

    def submit_task(self):
        super().submit_task()
        start_day = self.entry_start_day.get()
        start_month = self.entry_start_month.get()
        start_year = self.entry_start_year.get()
        end_day = self.entry_end_day.get()
        end_month = self.entry_end_month.get()
        end_year = self.entry_end_year.get()
        frequency = self.entry_frequency.get()
        task = Task(self.entry_task_name.get(), self.entry_task_type.get(), self.entry_start_time.get(), self.entry_duration.get(), start_day, start_month, start_year, end_day, end_month, end_year, frequency)
        messagebox.showinfo("Task Details", f"Recurring Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_task_type.get()}\nStart Date: {start_day}/{start_month}/{start_year}\nEnd Date: {end_day}/{end_month}/{end_year}\nFrequency: {frequency}")

if __name__ == "__main__":
    app=MainWindow()
    app.mainloop()
