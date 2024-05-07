import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog


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
        edit.add_command(label="Create Recurring Task", command=self.create_task)
        edit.add_command(label="Create Transient Task", command=self.donothing)
        edit.add_command(label="Create Anti-Task", command=self.donothing)
        edit.add_command(label="Edit Task", command=self.donothing)
        edit.add_separator()
        edit.add_command(label="Delete Task", command=self.donothing)
        self.menubar.add_cascade(label="Edit", menu=edit)

    def donothing(self):
        print()

    def upload_file(self):
        newWindow = FileWindow()

    def create_task(self):
        newWindow = CreateWindow()

class CreateWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Create Task")
        self.geometry("500x350")
        
        # Labels
        self.label_task_name = tk.Label(self, text="Task Name:")
        self.label_task_type = tk.Label(self, text="Task Type:")
        self.label_start_time = tk.Label(self, text="Start Time (HH:MM):")
        self.label_duration = tk.Label(self, text="Duration (minutes):")
        self.label_start_date = tk.Label(self, text="Start Date (YYYY-MM-DD):")
        self.label_end_date = tk.Label(self, text="End Date (YYYY-MM-DD):")
        
        # Entries
        self.entry_task_name = tk.Entry(self)
        self.entry_task_type = tk.Entry(self)
        self.entry_start_time = tk.Entry(self)
        self.entry_duration = tk.Entry(self)
        self.entry_start_date = tk.Entry(self)
        self.entry_end_date = tk.Entry(self)
        
        # Buttons
        self.button_submit = tk.Button(self, text="Submit", command=self.submit_task)
        
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

class FileWindow(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("File Upload")
        self.geometry("500x350")

        #button to upload a file
        self.button = tk.Button(self, text='Open', command=self.upload)
        self.button.pack()

    def upload(self):
        filename = filedialog.askopenfilename(title="Choose a file", filetypes= (("JSON files", "*.json")))
        self.file_name = tk.Label(self, text="File name: " + filename)
        print('Selected: ', filename)



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
