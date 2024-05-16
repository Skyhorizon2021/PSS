from Schedule import *
from Models.RecurringModel import Recurring
from Models.TransientModel import Transient
from Models.AntiTaskModel import Anti
import Checking
import pymongo
from bson.json_util import dumps
import calendar

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

        # Task Creation
        if mod.noOverlapAdd(task):
            if UpdatedChecking.isRecurring(task):
                newdict = {"Task Type":task.type, "Name":task.name, "Time":task.startTime, "Duration":task.duration,
                                "EndDate":task.endDate, "Frequency":task.frequency}
            elif UpdatedChecking.isTran(task):
                newdict = {"Task Type":task.type, "Name":task.name, "Time":task.startTime, "Duration":task.duration}
            elif UpdatedChecking.isAnti(task) and mod.checkRecurring(task):
                newdict = {"Task Type":task.type, "Name":task.name, "Time":task.startTime, "Duration":task.duration}
            mycol.insert_one(newdict)
        else:
            print("Task overlaps another task/recurring DNE")

        return True

    def viewTask(name):
     
        listSche = Schedule.getData()
        
        for task in listSche:
            if task['Name'] == name:
                taskname = name
                taskType = task['Type']
                taskDate = task['StartDate']
                taskTime = task['StartTime']
                taskDur = task['Duration']
                if UpdatedChecking.isRecurring(task):
                    end = task['EndDate']
                    freq = task['Frequency']
                    return Recurring(taskname, taskTime, taskDur, taskDate, taskType, end, freq)
                return Transient(taskname, taskTime, taskDur, taskDate, taskType)

    def deleteTask(self, name):
        
        # Gets the schedule
        listSche = Schedule.getData()
        tempSche = Schedule.getData()

        mod = Checking()

        # Searching inside database
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = myclient["schedule"]
        mycol = mydb["tasks"]

        # Search for task name
        for task in listSche:
            if task['Name'] == name:
                if UpdatedChecking.isRecurring(task):
                    antiName = mod.checkAnti(task)
                    if antiName != "":
                        self.deleteTask(antiName)
                    query = {'Name':name}
                elif UpdatedChecking.isTran(task):
                    query = {'Name':name}
                elif UpdatedChecking.isAnti(task) and mod.noOverlapAnti(task):
                    query = {'Name':name}
                mycol.delete_one(query)

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

    def viewDaySchedule(self, date):
        mod = Checking()
        mod2 = UpdatedChecking()
        listSche = mod.hideAnti(date)
        
        daySche = []
        sortedSchedule = []
        
        mod2.iterateDate()

        for task in listSche:
            if UpdatedChecking.isRecurring(task):
                if task['StartDate'] == date:
                    daySche.append({"Name":task['Name'], "Type":task['Type'], "StartDate":task['StartDate'], "StartTime":task['StartTime'], "Duration":task['Duration']})
            elif task['Date'] == date:
                daySche.append({"Name":task['Name'], "Type":task['Type'], "Date":task['Date'], "StartTime":task['StartTime'], "Duration":task['Duration']})

        tasknum = len(daySche)
        
        while True:
            minTime = 24
            # Get the earliest time
            for i in range(len(daySche)):
                if daySche[i]['StartTime'] < minTime:
                    minTime = daySche[i]['StartTime']
            # Append to sorted schedule for earliest time
            for i in range(len(daySche)):
                if daySche[i]['StartTime']==minTime:
                    sortedSchedule.append(daySche[i])
                    daySche.remove(daySche[i])
                    break
            # Breaks when all tasks are sorted in the schedule
            if daySche == []:
                break
            
            return sortedSchedule

    def viewWeekSchedule(self, date):
        mod = Checking()
        sortedWeek = []

        # Appends a day's schedule to the week schedule
        # Will not load days without tasks
        for i in range(7):
            nextday =mod.formatDate(str(date+i))
            sortedDay = self.viewDaySchedule(nextday)
            if sortedDay != []:
                sortedWeek.append(sortedDay)

        return sortedWeek

    def viewMonthSchedule(self, date):
        mod = Checking()
        sortedMonth = []
        day = mod.separateDate(date)

        endOfMonth = calendar.monthrange(day[0], day[1])[1]
        # Formats month if less than 10 and returns them to the start of the month for iteration
        if day[1] < 10:
            newDate = str(day[0]) + "0" + str(day[1]) + "01"
        else:
            newDate = str(day[0]) + str(day[1]) + "01"

        # Appends a day's schedule to the week schedule
        # Will not load days without tasks
        for i in range(endOfMonth):
            nextday =mod.formatDate(str(newDate)+i)
            sortedDay = self.viewDaySchedule(nextday)
            if sortedDay != []:
                sortedMonth.append(sortedDay)
        
        return sortedMonth

    def writeDaySchedule(self, filename, date):
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
                    #if listSche[date][tasks]['Task Type'] == "Recurring Task":
                        #mycol.replace_one()
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
            
            for detail in sortedSchedule:
                del detail['EndDate']
                del detail['Frequency']

        except:
            # Day does not exists and will not add to added
            pass
        
        # Print to file
        try:
            with open(filename, 'w') as jsonfile:
                json.dump({date : sortedSchedule}, jsonfile)
        except FileNotFoundError:
            print("File does not exist")

    def writeWeekSchedule(self, filename, date):
        mod = Checking()

        # Appends a day's schedule to the week schedule
        # Will not load days without tasks
        for i in range(7):
            nextday =str(mod.formatDate(str(int(date)+i)))
            self.writeDaySchedule(filename, nextday)

    def writeMonthSchedule(self, filename, date):
        mod = Checking()

        day = mod.separateDate(date)

        endOfMonth = calendar.monthrange(day[0], day[1])[1]
        # Formats month if less than 10 and returns them to the start of the month for iteration
        if day[1] < 10:
            newDate = str(day[0]) + "0" + str(day[1]) + "01"
        else:
            newDate = str(day[0]) + str(day[1]) + "01"

        # Appends a day's schedule to the week schedule
        # Will not load days without tasks
        for i in range(endOfMonth):
            nextday =str(mod.formatDate(str(int(newDate)+i)))
            self.writeDaySchedule(filename, nextday)

PSS.viewTask("A")

