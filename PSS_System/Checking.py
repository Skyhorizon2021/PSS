import datetime
from Schedule import *
from Models.RecurringModel import Recurring
from Models.TransientModel import Transient

class Checking:

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
    def checkName(name):
        names = []
        
        # Retrieves and validate schedule
        listsche = Schedule.getData()

        # Gets every task and checks if name is unique
        for dict in listsche.values():
            for detail in dict.values():
                if name in detail.values():
                    return False
        return True

    # Validates a correct duration
    def validDuration(duration):
        return duration >= 0.25 and duration <=23.75
    
    # Validates a correct time
    def validTime(time):
        return time >= 0.25 and time <=23.75
    
    # Help in iterateDate() to get proper month formatting
    def formatMonthDay(self, num):
        if num < 10:
            return "0" + str(num)
        else:
            return str(num)
        
    # Separates date to year, month, day
    def separateDate(self, date):
        day = []        
        day.append(int(str(date)[:4]))
        day.append(int(str(date)[4:6]))
        day.append(int(str(date)[6:]))
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

        while True:
            # Checks for dates extensive of their max dates and changes it accordingly
            if day[1] == 1 | 3 | 5 | 7 | 8 | 10 | 12 and day[2] > 31:
                if day[1] == 12:
                    day[1] = 1
                    day[2] -= 31
                    break
                else:
                    day[1] += 1
                    day[2] -= 31
                    break
            elif day[1] == 4 | 6 | 9 | 11 and day[2] > 30:
                day[1] += 1
                day[2] -= 30
                break
            elif day[1] == 2 and day[2] > 28:
                day[1] += 1
                day[2] -= 28
                break
        
        # Returns proper iterated date
        return int(str(day[0])+str(day[1])+str(day[2]))

    # Check if tasks overlap
    def noOverlap(self, task):
        listsche = Schedule.getData()
        old = 0
        new = 24.00
        
        # Retrieve Task's start date, start time,  and duration, and calculates its end time
        start = task.date
        taskStart = self.convertTime(task.startTime)
        taskDuration = task.duration
        taskEnd = taskStart + taskDuration

        # Checks if recurring type to get start and end dates, and frequency
        if issubclass(type(task), Recurring):
            end = task.endDate
            frequency = task.frequency

        # Should get every date that a task is recurring on and dates around it
        dates = self.iterateDate(start, end, frequency)
        yesterday = self.iterateDate(self.formatDate(start-1),self.formaDate(end-1), frequency)
        tomorrow = self.iterateDate(self.formatDate(start+1),self.formaDate(end+1), frequency)

        # Converts dates to string to match
        for i in range(len(dates)):
            dates[i] = str(dates[i])
            yesterday[i] = str(yesterday[i])
            tomorrow[i] = str(tomorrow[i])
        
        # Gets the end time of yesterday's last task
        for days in range(len(yesterday)):
            tasks = listsche[dates[days]].values()
            for detail in tasks:
                time = self.convertTime(detail['Time'])
                duration = float(detail['Duration'])
                # Calculates a task's end time
                endtime = time + duration
                # Gets the latest task's end time
                if endtime > old:
                    old = endtime

        # Get the start time of the next day's first task
        for days in range(len(tomorrow)):
            tasks = listsche[dates[days]].values()
            for detail in tasks:
                starttime = self.convertTime(detail['Time'])
                # Gets the earliest time a task starts for the next day as upper boundx
                if starttime < new:
                    new = starttime
                
        # Gets all tasks for the days
        for days in range(len(dates)):
            tasks = listsche[dates[days]].values()
            # Access each tasks details
            for detail in tasks:
                # Get times for each tasks
                time = self.convertTime(detail['Time'])
                duration = float(detail['Duration'])
                total = time  + duration
                
                # Checks if the tasks start during another task
                if taskStart > time and taskStart < total:
                    return False
                # Checks if the task ends before during another task
                elif taskStart < time and taskEnd < total:
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

        # Set the latest end time as lower bound if exceeds next day
        if old > 24.00:
            old -= 24.00
            # Will check if the task starts before yesterday's task ended
            return old > taskStart
        
        # Will check if the task will end before the next day's first task
        if taskEnd > 23.75:
            new += 24.00
            return new < taskEnd

        # Validates if all checks fail
        return True