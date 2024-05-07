import sqlite3
import schedule
from PSS_System.Models.RecurringModel import Recurring
from PSS_System.Models.TransientModel import Transient
from PSS_System.Models.AntiTaskModel import Anti
import datetime

class PSS:

    @staticmethod
    def createTask():
        print("Select the type of task:\n1. Recurring\n2. Transcient\n3. Recurring")
        selection = input(int())
        match selection:
            case 1:
                # Entering parameters
                name = input("Enter the name of the task: ")
                taskType = "Recurring Task"
                start = input(float("Enter the task's start time: "))
                duration = input(float("Enter the task's duration: "))
                startDate = input(float("Enter the task's start date: "))
                endDate = input(int("Enter the task's end date: "))
                frequency = input(int("Enter the task's frequency: "))
                
                # Creating recurring task
                reTask = Recurring(name, start, duration, startDate, taskType,
                endDate, frequency)
                return reTask
            case 2:
                # Entering parameters
                name = input("Enter the name of the task: ")
                taskType = "Transcient Task"
                start = input(float("Enter the task's start time: "))
                duration = input(float("Enter the task's duration: "))
                date = input(int("Enter the task's date: "))

                # Creating transient task
                trTask = Transient(name, start, duration, date, taskType)
                return trTask
            case 3:
                # Entering parameters
                name = input("Enter the name of the task: ")
                taskType = "Anti Task"
                start = input(float("Enter the task's start time: "))
                duration = input(float("Enter the task's duration: "))
                date = input(int("Enter the task's date: "))

                # Creating anti task
                anTask = Anti(name, start, duration, date, taskType)
                return anTask


    def viewTask():
        name = input("Enter the task name: ") # can also do 'def viewTask(name)' instead
        # Connect to database
        con = sqlite3.connect('schedule.db')
        cur = con.cursor()

        # Select Name to match the search
        cur = con.execute("SELECT Name from schedule")
        for row in cur:
            # Display the match
            if row[0] == name:
                # Format display later
                print(row)
                break
        con.close()
        
    def deleteTask():
        name = input("Enter the task name: ") # can also do 'def viewTask(name)' instead
        
        # Connect to database
        con = sqlite3.connect('schedule.db')
        cur = con.cursor()
        # Search for task name

        # Search for task type

        #If recurring, check for anti task to delete with

        # If antitask, check if delete it will cause an overlap
        # and causing conflict between two tasks
        # Generate an error message if it is not deleted
        pass
    def editTask():
        # Check for task name

        # Display current attributes

        # Make changes to attributes

        # Verify that there is not overlap nor invalid changes

        # Confirm edits
        pass

    def writeToFile():
        filename = input("Enter a file name: ")
        # Validate file name (either create new or exisiting)

        # Print to file

    def readFromFile():
        # Search for file name

        # Validate format and no overlap

        # Load task from JSON to schedule
        pass

    def viewDaySchedule():
        # Checks for file name

        # Checks for start date

        # Check for antitasks (no display purposes)

        # Print out the day schedule

        pass

    def viewWeekSchedule():
        # Checks for file name

        # Checks for start date

        # Check for antitasks (no display purposes)

        # Loop for 7 days, print out day schedule
        pass

    def viewMonthSchedule():
        # Checks for file name

        # Checks for start of the month

        # Check for antitasks (no display purposes)

        # Loop for 30 days, print out day schedule
        pass

    def writeDaySchedule():
        # Checks for file name

        # Checks for start date

        # Check for antitasks (no display purposes)

        # Write day schedule to file
        pass

    def writeWeekSchedule():
        # Checks for file name

        # Checks for start date

        # Check for antitasks (no display purposes)

        # Loop for 7 days, write day schedule to file
        pass

    def writeMonthSchedule():
        # Checks for file name

        # Checks for start of the month

        # Check for antitasks (no display purposes)

        # Loop for 30 days, write day schedule to file
        pass
# Just written down the required methods from our PSS diagrams

    
    
    
