class PSS:

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
                anTask = AntiTask(name, start, duration, date, taskType)
                return anTask


    def viewTask():
        pass
        
    def deleteTask():
        pass
    def editTask():
        pass
    def writeToFile():
        pass
    def readFromFile():
        pass
    def viewDaySchedule():
        pass
    def viewWeekSchedule():
        pass
    def viewMonthSchedule():
        pass
    def writeDaySchedule():
        pass
    def writeWeekSchedule():
        pass
    def writeMonthSchedule():
        pass
# Just written down the required methods from our PSS diagrams