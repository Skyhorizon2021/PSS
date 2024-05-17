import datetime
from Schedule import *
from Models.RecurringModel import Recurring
from Models.TransientModel import Transient
from Models.AntiTaskModel import Anti

class UpdatedChecking:

    # Returns boolean value if date is valid
    def checkDate(self, date):
        # If a date object is successfully created, return true
        try:
            day = self.separateDate(date)
            start = datetime.date(day[0], day[1], day[2])
            return True
        except:
            return False
    
    # Validates a unique name
    def checkName(self, name):       
        # Retrieves and validate schedule
        listsche = Schedule.getData()

        # Gets every task and checks if name is unique
        for task in listsche:
            if name in task['Name']:
                return False
        return True

    # Validates correct task type
    def checkType(self, type):
        taskTypes = ["Anti Task", "Recurring Task", "Transient Task"]
        if type in taskTypes:
            return True
        else:
            return False
    
    # Validates correct frequency
    def checkFreq(self, freq):
        freq = int(freq)
        return freq == 1 | freq == 7

    # Validates a correct duration
    def validDuration(self, duration):
        duration = float(duration)
        return duration >= 0.25 and duration <=23.75
    
    # Validates a correct time
    def validTime(self, time):
        time = self.convertTime(time)
        return time >= 0.25 and time <=23.75
    
    # Help in iterateDate() to get proper month formatting
    def formatMonthDay(self, num):
        if num < 10:
            return "0" + str(num)
        else:
            return str(num)
        
    # Separates date to year, month, day
    def separateDate(self, date):
        day = [0,0,0]        
        day[0] = (int(str(date)[:4]))
        day[1] = (int(str(date)[4:6]))
        day[2] = (int(str(date)[6:]))
        return day
    
    # Help create recurring tasks
    def iterateDate(self, startDate, endDate, frequency):
        dates = []

        # Set starting date
        start = self.separateDate(startDate)
        start = datetime.date(start[0], start[1], start[2])

        # Set ending date
        end = self.separateDate(endDate)
        end = datetime.date(end[0], end[1], end[2])

        frequency = int(frequency)

        # Get the dates dependent on its frequency
        res_date = start
        while res_date <= end:
            dates.append(int(str(res_date.year) + self.formatMonthDay(res_date.month) + self.formatMonthDay(res_date.day)))
            res_date += datetime.timedelta(days=frequency)
        
        return dates
    
    # Converts time to float value
    def convertTime(self, time):
        newtime = []
        start = time.split(':')
        newtime.append(int(start[0]))
        newtime.append(int(start[1]) / 15 / 4)
        newtime[1] += round(int(start[1]) % 15)/4
        return newtime[0]+newtime[1]
    
    # Returns the proper date if the day exceeds the month's max day
    def formatDate(self, date):
        day = self.separateDate(date)

        # Checks for dates extensive of their max dates and changes it accordingly
        if day[1] == 1 | 3 | 5 | 7 | 8 | 10 | 12 and day[2] > 31:
            if day[1] == 12:
                day[1] = 1
                day[2] -= 31
            else:
                day[1] += 1
                day[2] -= 31
        elif day[1] == 4 | 6 | 9 | 11 and day[2] > 30:
            day[1] += 1
            day[2] -= 30
            
        elif day[1] == 2 and day[2] > 28:
            day[1] += 1
            day[2] -= 28
        else:
            pass

        # Returns proper iterated month
        if day[1] < 10 and day[2] < 10:
            return int(str(day[0]) + "0"+str(day[1]) + "0" + str(day[2]))
        elif day[1] < 10:
            return int(str(day[0]) + "0"+str(day[1]) + str(day[2]))
        elif day[2] < 10:
            return int(str(day[0]) + str(day[1]) + "0" + str(day[2]))
        else:
            return int(str(day[0]) + str(day[1])+str(day[2]))

    # Check if tasks overlap
    def noOverlapAdd(self, task):
        listsche = Schedule.getData()
        
        # Retrieve Task's start date, start time,  and duration, and calculates its end time
        start = task.date
        taskStart = task.startTime
        taskDuration = task.duration
        taskEnd = taskStart + taskDuration

        # Checks if recurring type to get start and end dates, and frequency
        if issubclass(type(task), Recurring):
            end = task.endDate
            frequency = task.frequency
        else:
            end = start
            frequency = 1

        # Should get every date that a task is recurring on and dates around it
        dates = self.iterateDate(start, end, frequency)

        # Gets all tasks for the days
        for days in range(len(dates)):
            try:
                for task in listsche:
                    # Get times for each tasks
                    time = task['StartTime']
                    duration = task['Duration']

                    # End Time
                    total = time  + duration
                    
                    # Checks if the tasks start during another task
                    if taskStart > time and taskStart < total and taskEnd > total:
                        return False
                    # Checks if the task ends during another task
                    elif taskStart < time and taskEnd < total and taskEnd > time:
                        return False
                    # Checks if the task envelopes another task
                    elif taskStart < time and taskEnd > total:
                        return False
                    # Checks if the task is enveloped by another task
                    elif taskStart > time and taskEnd < total:
                        return False
                    # Checks if task is the exact time slot as another task
                    elif taskStart == time and taskEnd == total:
                        return False
            except:
                pass

        # Validates if all checks fail
        return True

    # Check if antitasks deletion overlap
    def noOverlapAdd(self, task):
        listsche = Schedule.getData()
        
        # Retrieve Task's start date, start time,  and duration, and calculates its end time
        start = task['Date']
        taskStart = task['StartTime']
        taskDuration = task['Duration']
        taskEnd = taskStart + taskDuration

        # Gets all tasks for the days
        try:
                for ntask in listsche:
                    # Checks if recurring type to get start and end dates, and frequency
                    if issubclass(type(ntask), Recurring):
                        end = ntask['EndDate']
                        frequency = ntask['Frequency']
                    else:
                        end = start
                        frequency = 1

                        # Should get every date that a task is recurring on and dates around it
                        dates = self.iterateDate(start, end, frequency)

                        # Get times for each tasks
                        time = ntask['StartTime']
                        duration = ntask['Duration']

                        # End Time
                        total = time  + duration
                        
                        # Checks if the tasks start during another task
                        if taskStart > time and taskStart < total and taskEnd > total:
                            return False
                        # Checks if the task ends during another task
                        elif taskStart < time and taskEnd < total and taskEnd > time:
                            return False
                        # Checks if the task envelopes another task
                        elif taskStart < time and taskEnd > total:
                            return False
                        # Checks if the task is enveloped by another task
                        elif taskStart > time and taskEnd < total:
                            return False
                        # Checks if current task matches Anti with Recurring
                        elif issubclass(type(task), Anti) and taskStart == time and taskEnd == total and detail['Task Type'] != "Recurring Task":
                            return False

        except:
                pass

        # Validates if all checks fail
        return True

    # Checks if any recurring tasks have an antitask (for deleting recurring task)
    def checkAnti(self, antitask):
        listSche = Schedule.getData()

        date = antitask['Date']

        for task in listSche:
            if task['StartTime'] == antitask['StartTime'] and antitask['Duration'] == task['Duration']:
                return task['Name']

        return ""
    
    # Check if there is a recurring task to match antitask (for creating anti tasks)
    def checkRecurring(self, task):
        listSche = Schedule.getData()
        
        date = task.date
        
        # Checks if the checked task is an antitask in order to continue
        if not issubclass(type(task), Anti):
            return False

        # Iterates through the data to search for the matching recurring task
        for task in listSche:
            if task['StartDate'] == date[i] and task.startTime == task['StartTime'] and task.duration == task['Duration'] and isRecurring(task):
                return True
        return False

    # Validates Tasks attributes are appropriate    
    def checkAll(self, task):
        taskType = task.type

        if self.checkDate(task.date) and self.checkName(task.name) and self.checkType(taskType) and self.validDuration(task.duration) and self.validTime(task.startTime):
            if taskType == "Recurring Task":
                if self.checkFreq(task.frequency) and self.checkDate(task.endDate):
                    return True
            return True
        else:
            return False

    # For viewing task
    def hideAnti(self, date):
        listSche = Schedule.getData()

        for task in listSche:
            # Checking for antitask in schedule
            if UpdatedChecking.isAnti(task) and task['Date'] == date:
                taskStart = task['StartTime']
                taskDura = task['Duration']
                tempSche.remove(task)
                # Search for recurring to match
                for matchtask in tempSche:
                    if matchtask['StartTime'] == taskStart and matchtask['Duration'] == taskDura and UpdatedChecking.isRecurring(matchtask):
                        # Get recurring dates
                        datesRE = self.iterateDate(matchtask['StartDate'], matchtask['EndDate'], matchtask['Frequency'])
                        for days in datesRE:
                            # Removes anti and recurring from displayed schedule if an instance of the recurring day matches with antitask date
                            if days == date:
                                listSche.remove(task)
                                listSche.remove(matchtask)
                                break
                        break
        return listSche
        

    def isRecurring(task):
        if task['Type'] in ["Study", "Class", "Sleep", "Exercise", "Work", "Meal"]:
            return True
        else:
            return False

    def isAnti(task):
        if task['Type'] == "Cancellation":
            return True
        else:
            return False

    def isTran(task):
        if task['Type'] in ["Visit", "Shopping", "Appointment"]:
            return True
        else:
            return False
    