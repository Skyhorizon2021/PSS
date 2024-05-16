import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

from PSS import *

class MenuBar():
    def __init__(self, window):
        #Menu
        self.window = window
        menubar = tk.Menu(window)
        window.config(menu=menubar)

        #Display Menu
        display = tk.Menu(menubar, tearoff=0)
        display.add_command(label="Show Day", command=lambda: self.show(0))
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
        edit.add_command(label="Create Recurring Task", command=lambda: self.create_recur())
        edit.add_command(label="Create Transient Task", command=self.donothing)
        edit.add_command(label="Create Anti-Task", command=self.donothing)
        edit.add_command(label="Edit Task", command=self.donothing)
        edit.add_separator()
        edit.add_command(label="Delete Task", command=self.donothing)
        menubar.add_cascade(label="Edit", menu=edit)

    def donothing(self):
        print()

    def upload_file(self):
        self.new_window = FileWindow()

    def create_recur(self):
        self.new_window = CreateWindow()
    
    def show(self, type):
        self.new_window = DisplayWindow(self.window, type)
        

class CreateWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Task")
        self.geometry("400x200")

        frame=Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Labels
        self.label_task_name = tk.Label(frame, text="Task Name:")
        self.label_task_type = tk.Label(frame, text="Task Type:")
        self.label_start_time = tk.Label(frame, text="Start Time (HH:MM):")
        self.label_duration = tk.Label(frame, text="Duration (minutes):")
        self.label_start_date = tk.Label(frame, text="Start Date (YYYYMMDD):")
        self.label_end_date = tk.Label(frame, text="End Date (YYYYMMDD):")
        
        # Entries
        self.entry_task_name = tk.Entry(frame)
        self.entry_task_type = tk.Entry(frame)
        self.entry_start_time = tk.Entry(frame)
        self.entry_duration = tk.Entry(frame)
        self.entry_start_date = tk.Entry(frame)
        self.entry_end_date = tk.Entry(frame)
        
        # Buttons
        self.button_submit = tk.Button(frame, text="Submit", command=self.submit_task)
        
        # Layout
        self.label_task_name.grid(row=0, column=0, sticky="e", pady=5)
        self.label_start_time.grid(row=2, column=0, sticky="e", pady=5)
        self.label_duration.grid(row=3, column=0, sticky="e", pady=5)
        self.label_start_date.grid(row=4, column=0, sticky="e", pady=5)
        self.label_end_date.grid(row=5, column=0, sticky="e", pady=5)
        
        self.entry_task_name.grid(row=0, column=1)
        self.entry_start_time.grid(row=2, column=1)
        self.entry_duration.grid(row=3, column=1)
        self.entry_start_date.grid(row=4, column=1)
        self.entry_end_date.grid(row=5, column=1)
        
        self.button_submit.grid(row=6, columnspan=2, pady=8)
        
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

class DisplayWindow(Toplevel):
    def __init__(self, parent, type, master=None):
        super().__init__(master=master)
        self.title("Schedule Display")
        self.geometry("400x200")
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
