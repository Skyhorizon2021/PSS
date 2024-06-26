import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog

from PSS import *
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
        file.add_command(label="Save to JSON File", command=lambda: self.save_file())
        menubar.add_cascade(label="File", menu=file)

        #Edit Menu
        edit = tk.Menu(menubar, tearoff=0)
        edit.add_command(label="Create Recurring Task", command=lambda: self.create_recurring_task())
        edit.add_command(label="Create Transient Task", command=lambda: self.create_transient_task())
        edit.add_command(label="Create Anti-Task", command=lambda: self.create_anti_task())
        edit.add_command(label="Edit Task", command=lambda: self.edit_task())
        edit.add_command(label="Find Task", command=lambda: self.find_task())
        edit.add_separator()
        edit.add_command(label="Delete Task", command=lambda: self.del_task())
        menubar.add_cascade(label="Edit", menu=edit)

    def donothing(self):
        print()

    def upload_file(self):
        self.new_window = FileWindow()

    def save_file(self):
        self.new_window = SaveWindow()
    
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
        self.new_window = DeleteWindow()

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
        #use PSS to call readFromFile function
        filename = filedialog.askopenfilename(title="Choose a file", filetypes= [("JSON files", "*.json")])
        PSS.readFromFile(filename)
        self.file_name = tk.Label(self, text="File name: " + filename)
        print('Selected: ', filename)

class SaveWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Save to File")
        self.geometry("400x300")

        #button to upload a file
        self.label = tk.Label(self, text="Find Existing JSON File")
        self.button = tk.Button(self, text='Upload your file', command=self.upload)
        self.label.place(relx=.5, rely=.38, anchor = CENTER)
        self.button.place(relx=.5, rely=.5, anchor = CENTER)

    def upload(self):
        #use PSS to call writeToFile function
        filename = filedialog.askopenfilename(title="Choose a file", filetypes= [("JSON files", "*.json")])
        PSS.writeToFile(filename)
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
    
        self.frame=tk.Frame(self)
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
        new_frame = ScheduleFrame(self.parent, self.type, day)

        self.parent.place_frame(new_frame)
        self.destroy()

class ScheduleFrame(tk.Frame):
    def __init__(self, parent, type, day):        
        tk.Frame.__init__(self, parent)
        self.PSS_instance = PSS()
        #use PSS to display using viewDaySchedule, viewWeekSchedule, viewMonthSchedule

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        output = ""
        if type == 0:
            schedule = self.PSS_instance.viewDaySchedule(day)
            print(schedule)
            for task in schedule:
                output = output + "Name: " + task['Name'] + "\nType: " + task['Type'] + "\nDate: " + str(task['Date']) + "\nStart Time: " + str(task['StartTime']) + "\nDuration: " + str(task['Duration']) + "\n\n"
            self.frame.label = Label(self.frame, text="This will show day\n" + output)
        elif type == 1:
            schedule = self.PSS_instance.viewWeekSchedule(day)
            for i in range(len(schedule)):
                for task in schedule[i]:
                    output = output + "Name: " + task['Name'] + "\nType: " + task['Type'] + "\nDate: " + str(task['Date']) + "\nStart Time: " + str(task['StartTime']) + "\nDuration: " + str(task['Duration']) + "\n\n"
            self.frame.label = Label(self.frame, text="This will show week " + output)
        elif type == 2:
            schedule = self.PSS_instance.viewMonthSchedule(day)
            for i in range(len(schedule)):
                for task in schedule[i]:
                    output = output + "Name: " + task['Name'] + "\nType: " + task['Type'] + "\nDate: " + str(task['Date']) + "\nStart Time: " + str(task['StartTime']) + "\nDuration: " + str(task['Duration']) + "\n\n"
            self.frame.label = Label(self.frame, text="This will show month " + output)
        else:
            self.frame.label = Label(self.frame, text='')
        self.frame.label.pack()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class CreateWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Task")
        self.geometry("400x300")

        self.frame = tk.Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Labels
        self.label_task_name = tk.Label(self.frame, text="Task Name:")
        self.label_start_time = tk.Label(self.frame, text="Start Time :")
        self.label_duration = tk.Label(self.frame, text="Duration (minutes):")
        self.label_date = tk.Label(self.frame, text="Date (YYYYMMDD):")
        self.label_type = tk.Label(self.frame, text="Type:")

        # Entries
        self.entry_task_name = tk.Entry(self.frame)
        self.entry_start_time = tk.Entry(self.frame)
        self.entry_duration = tk.Entry(self.frame)
        self.entry_date = tk.Entry(self.frame)
        self.entry_type = tk.Entry(self.frame)

        # Buttons
        self.button_submit = tk.Button(self.frame, text="Submit", command=self.submit_task)

        # Layout
        self.label_task_name.grid(row=0, column=0, sticky="e", pady=5)
        self.label_start_time.grid(row=1, column=0, sticky="e", pady=5)
        self.label_duration.grid(row=2, column=0, sticky="e", pady=5)
        self.label_date.grid(row=3, column=0, sticky="e", pady=5)
        self.label_type.grid(row=4, column=0, sticky="e", pady=5)

        self.entry_task_name.grid(row=0, column=1)
        self.entry_start_time.grid(row=1, column=1)
        self.entry_duration.grid(row=2, column=1)
        self.entry_date.grid(row=3, column=1)
        self.entry_type.grid(row=4, column=1)

        self.button_submit.grid(row=5, columnspan=2, pady=8)

    def submit_task(self):
        # Retrieve task details from entries
        task_name = self.entry_task_name.get()
        start_time = self.entry_start_time.get()
        duration = self.entry_duration.get()

        # Retrieve date fields
        date = self.entry_date.get()


        # Message box confirming task submission
        messagebox.showinfo("Task Submitted", f"Task '{task_name}' submitted successfully!")

class TransientTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Transient Task")
        self.PSS_instance = PSS()
        
    def submit_task(self):
        super().submit_task()
        task = Transient(self.entry_task_name.get(), self.entry_start_time.get(), self.entry_duration.get(), self.entry_date.get(), self.entry_type.get())
        self.PSS_instance.createTask(task)
        messagebox.showinfo("Task Details", f"Transient Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_type.get()}\nStart Time: {self.entry_start_time.get()}\nDuration: {self.entry_duration.get()}")

class AntiTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Anti Task")
        self.PSS_instance = PSS()
        
    def submit_task(self):
        self.task_type = "Anti Task"
        super().submit_task()
        task = Anti(self.entry_task_name.get(), self.entry_start_time.get(), self.entry_duration.get(), self.entry_date.get(), self.entry_type.get())
        self.PSS_instance.createTask(task)
        messagebox.showinfo("Task Details", f"Anti Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_type.get()}\nStart Time: {self.entry_start_time.get()}\nDuration: {self.entry_duration.get()}")

class RecurringTaskWindow(CreateWindow):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Recurring Task")
        self.PSS_instance = PSS()
        # Add additional fields specific to Recurring Tasks
        self.label_end_date = tk.Label(self.frame, text="End Date (YYYYMMDD):")
        self.label_frequency = tk.Label(self.frame, text="Frequency:")

        self.entry_end_date = tk.Entry(self.frame)
        self.entry_frequency = tk.Entry(self.frame)

        self.label_end_date.grid(row=6, column=0, sticky="e", pady=5)
        self.entry_end_date.grid(row=6, column=1)
        self.label_frequency.grid(row=7, column=0, sticky="e", pady=5)
        self.entry_frequency.grid(row=7, column=1)
        self.button_submit.grid(row=8, columnspan=2, pady=8)

    def submit_task(self):
        self.task_type = "Recurring Task"
        super().submit_task()
        task = Recurring(self.entry_task_name.get(), self.entry_start_time.get(), self.entry_duration.get(), self.entry_type.get(), self.entry_end_date.get(), self.entry_frequency.get())
        self.PSS_instance.createTask(task)
        messagebox.showinfo("Task Details", f"Recurring Task:\nName: {self.entry_task_name.get()}\nType: {self.entry_type.get()}\nStart Time: {self.entry_start_time.get()}\nDuration: {self.entry_duration.get()}\nEnd Date: {self.entry_end_date.get()}\nFrequency: {self.entry_frequency.get()}")

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
        task = PSS.viewTask(self.entry.get())
        #turn task into a string, assign to output, else give error
        #task = ""
        output = "Name: " + task.name + "\nType: " + task.type + "\nDate: " + str(task.date) + "\nStart Time: " + str(task.startTime) + "\nDuration: " + str(task.duration) + "\n\n"
        print(self.entry.get())

        #self.label = Label(self, text=output)
        self.entry.destroy()
        self.label.destroy()
        self.button.destroy()
        self.label = Label(self, text=output)
        self.label.place(relx=.5, rely=.2, anchor = CENTER)

        self.next = Label(self, text="What type of task would you like to create?")
        self.recur_button = Button(self, text="Recurring Task", command=lambda: self.create_recurring_task(task))
        self.tran_button = Button(self, text="Transient Task", command=lambda: self.create_transient_task(task))
        self.anti_button = Button(self, text="Anti Task", command=lambda: self.create_anti_task(task))

        self.next.place(relx=.5, rely=.4, anchor = CENTER)
        self.recur_button.place(relx=.5, rely=.6, anchor = CENTER)
        self.tran_button.place(relx=.5, rely=.7, anchor = CENTER)
        self.anti_button.place(relx=.5, rely=.8, anchor = CENTER)
    
    def create_recurring_task(self, task):
        self.new_window = RecurringTaskWindow()
        #call delete function for the searched task
        #PSS.delete(task)
        #self.destroy() destroys EditWindow

    def create_transient_task(self, task):
        self.new_window = TransientTaskWindow()

    def create_anti_task(self, task):
        self.new_window = AntiTaskWindow()

class DeleteWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Delete Task")
        self.geometry("300x150")
        self.PSS_instance = PSS()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill=tk.BOTH)

        self.label_task_name = tk.Label(frame, text="Task Name:")
        self.entry_task_name = tk.Entry(frame)

        self.button_delete = tk.Button(frame, text="Delete", command=self.delete_task)

        self.label_task_name.pack(pady=5)
        self.entry_task_name.pack(pady=5)
        self.button_delete.pack(pady=10)

    def delete_task(self):
        task_name = self.entry_task_name.get()
        # Call deleteTasks function with the task_name
        self.PSS_instance.deleteTask(task_name)
        messagebox.showinfo("Task Deleted", f"Task '{task_name}' has been deleted.")
    
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
        task = PSS.viewTask(self.entry.get())
        #turn task into a string, assign to output, else give error
        output = "Name: " + task.name + "\nType: " + task.type + "\nDate: " + str(task.date) + "\nStart Time: " + str(task.startTime) + "\nDuration: " + str(task.duration) + "\n\n"
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

        self.frame = Frame(self)
        self.frame.pack()
        label = Label(self.frame, text="Default Screen")
        label.pack()

    def place_frame(self, frame):
        self.frame.destroy()
        self.frame = frame
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.tkraise()
        

if __name__ == "__main__":
    app=MainWindow()
    app.mainloop()
