from Schedule import *
from Models.RecurringModel import Recurring
from Models.TransientModel import Transient
from Models.AntiTaskModel import Anti
from Checking import *
import pymongo
from bson.json_util import dumps

class PSS:

    def createTask(self, task):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        mod = Checking()
        if not mod.checkAll(task):
            print("Invalid Attributes")
            return False

        newSche = Schedule.getData()

        taskType = task.type
        date = str(task.date)

        # Task creation
        match taskType:
            case "Recurring Task":
                # Get dates for recurring objects to be placed in
                dates = mod.iterateDate(task.date, task.endDate, task.frequency)
                if mod.noOverlapAdd(task):
                    for days in dates:
                        newIndex = mod.getTaskIndex(days)
                        newdict = {"Task Type":task.type, "Name":task.name, "Time":task.startTime, "Duration":task.duration,
                                "EndDate":task.endDate, "Frequency":task.frequency}
                        try: # Adds Recurring to Existing day
                            newSche[str(days)][newIndex] = newdict
                        except: # Creates a new day to add a recurring task
                            newSche[str(days)] = {newIndex : {}}
                            newSche[str(days)][newIndex] = newdict
                        task.date = days
                    mycol.replace_one({}, newSche)   
                else:
                    print("A task exists during this period")

            case "Transient Task":
                if mod.noOverlapAdd(task):
                    newIndex = mod.getTaskIndex(task.date)
                    newdict = {"Task Type":task.type, "Name":task.name, "Time":task.startTime, "Duration":task.duration}
                    try:
                        newSche[date][newIndex] = newdict
                    except:
                        newSche[date] = {newIndex : {}}
                        newSche[date][newIndex] = newdict
                    mycol.replace_one({}, newSche)
                else:
                    print("Task exists during this period")

            case "Anti Task":
                if mod.checkRecurring(task):
                    newIndex = mod.getTaskIndex(task.date)
                    newdict = {"Task Type":task.type, "Name":task.name, "Time":task.startTime, "Duration":task.duration}
                    newSche[date][newIndex] = newdict
                    mycol.replace_one({}, newSche)
                else:
                    print("Recurring Task does not exist")
        return True

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
                if mod.noOverlapAnti(checkingTask):
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

    def editTask(self, oldtask, newtask):
        mod = Checking()
               
        taskType = newtask.type
        name = newtask.name
        date = newtask.date
        time = mod.convertTime(newtask.time)
        duration = newtask.duration
        if taskType == "Recurring":
            end = newtask.endDate
            freq = newtask.frequency

        # Remove old task for checking
        self.deleteTask(oldtask.name)

        # Checks all values for validity 
        if mod.checkName(name) and mod.checkDate(date) and mod.checkDate(end) and mod.validDuration(duration) and mod.validTime(time) and mod.checkFreq(freq) and mod.checkType(taskType):
            match taskType:
                # Checks all types of tasks for overlap and (re)creates tasks if no overlap
                case "Transient Task":
                    checkingtask = Transient(name, time, duration, date, taskType)
                    if mod.noOverlapAdd(checkingtask):
                        self.createTask(newtask)
                    else:
                        self.createTask(oldtask)
                case "Recurring Task":
                    checkingtask = Recurring(name, time, duration, date, taskType, end, freq)
                    if mod.noOverlapAdd(checkingtask):
                        self.createTask(newtask)
                    else:
                        self.createTask(oldtask)
                case "Anti Task":
                    checkingtask = Anti(name, time, duration, date, taskType)
                    if mod.noOverlapAdd(checkingtask):
                        self.createTask(newtask)
                    else:
                        self.createTask(oldtask)
        else:
            # Unspecified Task Error
            print("Error in task's value")

    def writeToFile(filename):
        # Connects to database to retrieve data
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]
        cur = mycol.find_one()

        # Print to file
        try:
            with open(filename, 'w') as jsonfile:
                json.dump(json.load(dumps(cur)), jsonfile)
        except FileNotFoundError:
            print("File does not exist")

    def readFromFile(filename):
        Schedule.loadData(filename)

    def viewDaySchedule(date):
        mod = Checking()

        listSche = mod.hideAnti(date)
        tempSche = mod.hideAnti(date)
        
        sortedTasks = []
        sortedSchedule = []
        try:
            while listSche[date] != {}:
                minTime = 24
                for tasks in listSche[date]:
                    start = mod.convertTime(listSche[date][tasks]['Time'])
                    # Gets the earliest start time
                    if start < minTime:
                        minTime = start
                        selectTask = tasks
                # Deletes the earliest task for iteration
                del listSche[date][selectTask]
                # Appends if task's time is the earliest
                for tasks in tempSche[date]:
                        if mod.convertTime(tempSche[date][tasks]['Time']) == minTime:
                            sortedTasks.append(tasks)
                            break
            
            # Returns the task objects in a sorted array
            i = 0
            for tasks in sortedTasks:
                if tasks == sortedTasks[i]:
                    sortedSchedule.append(tempSche[date][tasks])
                i += 1
        except:
            # Day does not exists
            print("Day Schedule does not exist")
        print(sortedSchedule)
        return sortedSchedule

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

    def writeDaySchedule(filename):
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

#checkingTask = Anti("Cancellation 2", "11:15:00", ".75", "20240217", "Anti Task")
#x = PSS()
#x.createTask(checkingTask)
PSS.viewDaySchedule("20240217")