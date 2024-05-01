class PSS:

    def createTask():
        print("Select the type of task:\n1. Recurring\n2. Transcient\n3. Recurring")
        selecttion = input(int())
        switch(type){
            case 1:
                name = input("Enter the name of the task: ")
                taskType = "Recurring Task"
                start = input(float("Enter the task's start time: "))
                duration = input(float("Enter the task's duration: "))
                startDate = input(float("Enter the task's start date: "))
                endDate = input(int("Enter the task's end date: "))
                frequency = input(int("Enter the task's frequency: "))
                break;
            case 2:
                name = input("Enter the name of the task: ")
                taskType = "Transcient Task"
                start = input(float("Enter the task's start time: "))
                duration = input(float("Enter the task's duration: "))
                date = input(int("Enter the task's date: "))
                break;
            case 3:
                name = input("Enter the name of the task: ")
                taskType = "Anti Task"
                start = input(float("Enter the task's start time: "))
                duration = input(float("Enter the task's duration: "))
                date = input(int("Enter the task's date: "))
                break;
        }


    def viewTask():
        print()
        
    def deleteTask():

    def editTask():

    def writeToFile():
        
    def readFromFile():

    def viewDaySchedule():

    def viewWeekSchedule():

    def viewMonthSchedule():

    def writeDaySchedule():

    def writeWeekSchedule():

    def writeMonthSchedule():

# Just written down the required methods from our PSS diagrams