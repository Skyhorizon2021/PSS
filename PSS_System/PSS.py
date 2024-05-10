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

    def deleteTask(self, name):
        
        # Gets the schedule
        listSche = Schedule.getData()
        tempSche = Schedule.getData()

        # Search for task name
        for days in listSche:
            task = listSche[days]
            for detail in task:
                # Matching task name
                if name == task[detail]['Name']:
                    key_list = list(listSche[days].keys())
                    value_list = list(listSche[days].values())
                    date = days
                    taskDet = task
                    # Matching task type 
                    taskType = task[detail]["Task Type"]
                    start = task[detail]["Time"]
                    dur = task[detail]["Duration"]
                    if taskType == "Recurring Task":
                        end = task[detail]["EndDate"]
                        freq = task[detail]["Frequency"]

                    matchTask = task[detail]
                
                    value = value_list.index(matchTask)
        # Gets the key value for the task
        x = key_list[value]
        
        # Searching inside database
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        query = {date : taskDet}
        mod = Checking()

        match taskType:
            case "Recurring Task":
                try:
                    checkingTask = Recurring(name, start, dur, date, taskType, end, freq)
                    antiName = mod.checkAnti(checkingTask)
                    if antiName != "":
                        self.deleteTask(antiName)
                    del tempSche[date][x]
                    # Deletes the day from schedule if no tasks are stored
                    if tempSche[date] == {}:
                        del tempSche[date]
                    # Replaces the day with the new day schedule
                    mycol.replace_one(query, tempSche)
                    # Continue to delete all instances of the task with its name
                    self.deleteTask(name)
                except:
                    print("Deleted all occurances of {}".format(name))
                    pass
            case "Anti Task":
                checkingTask = Anti(name, start, dur, date, taskType)
                # Checks if deleting antitask will not cause conflict
                if mod.noOverlapAntiDelete(checkingTask):
                    del tempSche[date][x]
                    if tempSche[date] == {}:
                        del tempSche[date]
                    # Replaces the day with the new day schedule
                    mycol.replace_one(query, tempSche)
                else:
                    print("Conflicting tasks upon deletion. Operation terminated...")
            # Just deletes the task, no checking required
            case "Transient Task":
                del tempSche[date][x]
                if tempSche[date] == {}:
                    del tempSche[date]
                mycol.replace_one(query, tempSche)

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

sched = PSS()
sched.deleteTask("C")