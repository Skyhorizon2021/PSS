import datetime
from email.utils import formatdate
import Schedule
class Checking:

    def noOverlap(startdate, enddate, frequency):
        listsche = Schedule.getData()

        for dates in listsche:
            pass

    # Returns boolean value if date is valid
    def checkDate(date):
        month = str(date)[4:6]
        day = str(date)[6:]
        # Checks if month's and their days are valid
        match month:
            case "01" | "03" | "05" | "07" | "08" | "10" | "12": 
                if day < 1 or day > 31:
                    return False
            case "04" | "06" | "09" | "11": 
                if day < 1 or day > 30:
                    return False
            case "02":
                if day < 1 or day > 28:
                    return False
            case _:
                return False
            
        # Should return true if fails all false cases
        return True
    
    # Help in iterateDate() to get proper month formatting
    def formatDate(num):
        if num < 10:
            return "0" + str(num)
        else:
            return str(num)
        
    # Help create recurring tasks
    def interateDate(startDate, endDate, frequency):
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
            
            dates.append(int(str(res_date.year) + formatdate(res_date.month) + formatdate(res_date.day)))

        return dates

    