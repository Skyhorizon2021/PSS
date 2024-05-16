import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

#from PSS import *
from Models.RecurringModel import Recurring
from Models.TransientModel import Transient
from Models.AntiTaskModel import Anti

class MenuBar():
    def __init__(self, window):
        #Menu
        self.window = window
        menubar = tk.Menu(window)
        window.config(menu=menubar)

        #Display Menu
        display = tk.Menu(menubar, tearoff=0)
        display.add_command(label="Show Day", command=lambda: self.show(0)) #lambda makes the command not call right away on start up so we can pass parameters to these functions
        display.add_command(label="Show Week", command=lambda: self.show(1))
        display.add_command(label="Show Month", command=lambda: self.show(2))
        menubar.add_cascade(label="Display", menu=display)

        #File Menu
        file = tk.Menu(menubar, tearoff=0)
        file.add_command(label="Open JSON File", command=lambda: self.upload_file())
        file.add_command(label="Save to JSON File", command=self.donothing)
        menubar.add_cascade(label="File", menu=file)

        #Edit Menu
        edit = tk.Menu(menubar, tearoff=0)
        edit.add_command(label="Create Recurring Task", command=lambda: self.create_recurring_task())
        edit.add_command(label="Create Transient Task", command=lambda: self.create_transient_task())
        edit.add_command(label="Create Anti-Task", command=lambda: self.create_anti_task())
        edit.add_command(label="Edit Task", command=lambda: self.edit_task())
        edit.add_command(label="Find Task", command=self.find_task)
        edit.add_separator()
        edit.add_command(label="Delete Task", command=self.del_task)
        menubar.add_cascade(label="Edit", menu=edit)

    def donothing(self):
        print()

    def upload_file(self):
        self.new_window = FileWindow()
    
    def show(self, type):
        self.new_window = DisplayWindow(self.window, type)

    def create_recurring_task(self):
        self.new_window = RecurringTaskWindow()

    def create_transient_task(self):
        self.new_window = TransientTaskWindow()

    def create_anti_task(self):
        self.new_window = AntiTaskWindow()

    def edit_task(self):
        self.new_window = EditWindow()
    
    def find_task(self):
        self.new_window = FindWindow()

    def del_task(self):
        self.new_window = ""

class FileWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("File Upload")
        self.geometry("400x300")

        #button to upload a file
        self.label = tk.Label(self, text="Add Tasks Through JSON File")
        self.button = tk.Button(self, text='Upload your file', command=self.upload)
        self.label.place(relx=.5, rely=.38, anchor = CENTER)
        self.button.place(relx=.5, rely=.5, anchor = CENTER)

    def upload(self):
        filename = filedialog.askopenfilename(title="Choose a file", filetypes= [("JSON files", "*.json")])
        self.file_name = tk.Label(self, text="File name: " + filename)
        print('Selected: ', filename)

class DisplayWindow(Toplevel):
    def __init__(self, parent, type, master=None):
        super().__init__(master=master)
        self.title("Schedule Display")
        self.geometry("400x300")
        self.date = ""
        self.parent = parent
        self.type = type
    
        self.frame=Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
        if type == 0:
            self.label = Label(self.frame, text="Day to Display (YYYYMMDD):")
        elif type == 1:
            self.label = Label(self.frame, text="Starting Date for Week to Display (YYYYMMDD):")
        elif type == 2:
            self.label = Label(self.frame, text="Starting Date for Month to Display (YYYYMMDD):")
        else:
            self.label = Label(self.frame, text='')
        self.entry = tk.Entry(self.frame)

        self.label.pack()
        self.entry.pack()

        self.button = tk.Button(self.frame, text="Submit", command=self.submit)
        self.button.pack()

    def submit(self):
        day = self.entry.get()
        #schedule = PSS.viewDaySchedule(date)
        new_frame = ScheduleFrame(self.parent, self.type, day)
        self.parent.place_frame(new_frame)
        self.destroy()

class ScheduleFrame(tk.Frame):
    def __init__(self, parent, type, day):        
        tk.Frame.__init__(self, parent)
        if type == 0:
            self.label = Label(self, text="This will show day " + day)
        elif type == 1:
            self.label = Label(self, text="This will show week " + day)
        elif type == 2:
            self.label = Label(self, text="This will show month " + day)
        else:
            self.label = Label(self.frame, text='')
        self.label.pack()

class CreateWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Task")
        self.geometry("400x300")  # Increased height to accommodate new fields

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
        day = int(self.entry_day.get())
        month = int(self.entry_month.get())
        year = int(self.entry_year.get())

        # Message box confirming task submission
        messagebox.showinfo("Task Submitted", f"Task '{task_name}' submitted successfully!")

class TransientTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Transient Task")

    def submit_task(self):
        super().submit_task()
        task = Transient(self.entry_task_name.get(), self.entry_task_type.get(), self.entry_start_time.get(), self.entry_duration.get())
        messagebox.showinfo("Task Details", f"Transient Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_task_type.get()}\nStart Time: {self.entry_start_time.get()}\nDuration: {self.entry_duration.get()}")

class AntiTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Anti Task")

    def submit_task(self):
        super().submit_task()
        task = Anti(self.entry_task_name.get(), self.entry_task_type.get(), self.entry_start_time.get(), self.entry_duration.get())
        messagebox.showinfo("Task Details", f"Anti Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_task_type.get()}\nStart Time: {self.entry_start_time.get()}\nDuration: {self.entry_duration.get()}")

class RecurringTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Recurring Task")

        #Remove CreateWindow date labels and entry fields
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
        start_day = int(self.entry_start_day.get())
        start_month = int(self.entry_start_month.get())
        start_year = int(self.entry_start_year.get())
        end_day = int(self.entry_end_day.get())
        end_month = int(self.entry_end_month.get())
        end_year = int(self.entry_end_year.get())
        frequency = int(self.entry_frequency.get())
        task = Recurring(self.entry_task_name.get(), self.entry_task_type.get(), self.entry_start_time.get(), self.entry_duration.get(), start_day, start_month, start_year, end_day, end_month, end_year, frequency)
        messagebox.showinfo("Task Details", f"Recurring Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_task_type.get()}\nStart Date: {start_day}/{start_month}/{start_year}\nEnd Date: {end_day}/{end_month}/{end_year}\nFrequency: {frequency}")

class EditWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Edit Task")
        self.geometry("400x300")

        self.label = Label(self, text="Enter name of task: ")
        self.button = Button(self, text='Search', command=self.search)
        self.entry = tk.Entry(self)

        self.label.place(relx=.5, rely=.3, anchor = CENTER)
        self.entry.place(relx=.5, rely=.4, anchor = CENTER)
        self.button.place(relx=.5, rely=.5, anchor = CENTER)

    def search(self):
        #task = PSS.viewTask(self.entry.get())
        #turn task into a string, assign to output, else give error
        output = ""
        print(self.entry.get())

        self.label = Label(self, text=output)
        self.entry.destroy()
        self.label.destroy()

        self.next = Label(self, text="What type of task would you like to create?")
        self.recur_button = Button(self, text="Recurring Task", command=self.create_recurring_task)
        self.tran_button = Button(self, text="Transient Task", command=self.create_transient_task)
        self.anti_button = Button(self, text="Anti Task", command=self.create_anti_task)

        self.label.place(relx=.5, rely=.3, anchor = CENTER)
        self.next.place(relx=.5, rely=.4, anchor = CENTER)
        self.recur_button.place(relx=.5, rely=.5, anchor = CENTER)
        self.tran_button.place(relx=.5, rely=.6, anchor = CENTER)
        self.anti_button.place(relx=.5, rely=.7, anchor = CENTER)
    
    def create_recurring_task(self):
        self.new_window = RecurringTaskWindow()
        #call delete function for the searched task

    def create_transient_task(self):
        self.new_window = TransientTaskWindow()

    def create_anti_task(self):
        self.new_window = AntiTaskWindow()

class FindWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Find Task")
        self.geometry("400x300")

        self.label = Label(self, text="Enter name of task: ")
        self.button = Button(self, text='Search', command=self.search)
        self.entry = tk.Entry(self)

        self.label.place(relx=.5, rely=.3, anchor = CENTER)
        self.entry.place(relx=.5, rely=.4, anchor = CENTER)
        self.button.place(relx=.5, rely=.5, anchor = CENTER)

    def search(self):
        #task = PSS.viewTask(self.entry.get())
        #turn task into a string, assign to output, else give error
        output = ""
        self.show = Label(self, text=output)
        self.label.destroy()
        self.entry.destroy()
        self.button.destroy()
        self.show.place(relx=.5, rely=.3, anchor = CENTER)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Scheduling System (PSS)")
        self.geometry("700x500")

        menubar = MenuBar(self)

        default = Frame(self)
        self.place_frame(default)
        label = Label(default, text="Default Screen")
        label.pack()

    def place_frame(self, frame):
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        

if __name__ == "__main__":
    app=MainWindow()
    app.mainloop()
