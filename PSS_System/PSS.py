import sqlite3
from Schedule import *
from Models.RecurringModel import Recurring
from Models.TransientModel import Transient
from Models.AntiTaskModel import Anti
import datetime
from Checking import *
import pymongo

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
                if Checking.noOverlap(reTask):
                    return reTask
                else:
                    print("Task creation failed...")
            
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
        name = input("Enter the task name: ")
        
        # Gets the schedule
        listSche = Schedule.getData()

        for days in listSche:
            task = listSche[days]
            for detail in task:
                if name == task[detail]['Name']:
                    print("Name: ", task[detail]['Name'])
                    print("Type: ", task[detail]['Task Type'])
                    print("Date: ", days)
                    print("Time: ", task[detail]['Time'])
                    print("Duration: ", task[detail]['Duration'])
                    if task[detail]["Task Type"] == "Recurring":
                        print("End Date: ", task[detail]['EndDate'])
                        print('Frequency: ', task[detail]['Frequency'])
                break

    def deleteTask():
        #name = input("Enter the task name: ")
        name = "A"
        # Gets the schedule
        listSche = Schedule.getData()

        # Search for task name
        for days in listSche:
            task = listSche[days]
            for detail in task:
                if name == task[detail]['Name']:
                    key_list = list(listSche[days].keys())
                    value_list = list(listSche[days].values())
                    date = days
                    taskType = task[detail]["Task Type"]
                    match taskType:
                        case "Recurring Task":
                            pass
                        case "Anti Task":
                            pass
                        case "Transient Task":
                            pass
                    matchTask = task[detail]
                
                    value = value_list.index(matchTask)
        x = key_list[value]
        del listSche[date][x]

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        database = myclient["schedule"]

        database.

        print(listSche)
                    #del key_list[value]
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
        #
        #  Checks for file name

        # Checks for start of the month

        # Check for antitasks (no display purposes)

        # Loop for 30 days, write day schedule to file
        pass
# Just written down the required methods from our PSS diagrams

PSS.deleteTask()