import datetime
from Schedule import *

class Checking:

    def noOverlap(startdate, enddate, frequency):
        listsche = Schedule.getData()

        for dates in listsche:
            pass

    # Returns boolean value if date is valid
    def checkDate(date):
        # If a date object is successfully created, return true
        try:
            year = str(date)[:4]
            month = str(date)[4:6]
            day = str(date)[6:]
            start = datetime.date(int(year), int(month), int(day))
            return True
        except:
            return False
    
    # Validates a unique name
    def checkName(name):
        names = []
        
        # Retrieves and validate schedule
        listsche = Schedule.getData()
        del listsche['_id']

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
    def formatDate(self, num):
        if num < 10:
            return "0" + str(num)
        else:
            return str(num)
        
    # Help create recurring tasks
    def interateDate(self, startDate, endDate, frequency):
        dates = []

        # Set starting date
        year = str(startDate)[:4]
        month = str(startDate)[4:6]
        day = str(startDate)[6:]
        start = datetime.date(int(year), int(month), int(day))

        # Set ending date
        year = str(endDate)[:4]
        month = str(endDate)[4:6]
        day = str(startDate)[6:]
        end = datetime.date(int(year), int(month), int(day))

        # Get the dates dependent on its frequency
        res_date = start
        while res_date <= end:
            res_date += datetime.timedelta(days=frequency)
            
            dates.append(int(str(res_date.year) + self.formatDate(res_date.month) + self.formatDate(res_date.day)))

        return dates