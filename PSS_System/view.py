import json
import sqlite3
import PSS

def menu():
    # Ask to load file
    loadFile()

    while(userinput != 3):
        print("Menu\n1. Tasks\n2. Schedule\n3. End Program")
        userinput = input(int("Select an option:"))

        match userinput:
            # Task Menu
            case 1:
                print("\n1. Create\n2. Delete\n3. Edit\n4. View")
                choice = input(int("Option: "))
                match choice:
                    case 1:
                        PSS.createTask()
                    case 2:
                        PSS.deleteTask()
                    case 3:
                        PSS.editTask()
                    case 4:
                        PSS.viewTask()
                    case _:
                        print("Invalid choice...")
            # Schedule Menu
            case 2:
                print("1. View Schedule\n2. Write Schedule")
                choice = input(int("Option: "))
                match choice:
                    case 1:
                        print("1. View Day Schedule\n2. View Week Schedule\n3. View Month Schedule ")
                        viewer = input(int("Option: "))
                        # Take in date and display scheduled option
                        
                    case 2: 
                        print("1. Write Day Schedule\n2. Write Week Schedule\n3. Write Month Schedule ")
                        viewer = input(int("Option: "))
                    case _:
                        continue # Replace
            # Ending Program
            case 3:
                continue # Replace
            # Default case
            case _:
                print("Invalid choice...")
        

def loadFile():
    # Asks if they want to load a schedule
        loadsch = input("Do you have a schedule to load?").lower()
        if loadsch[0] == 'y':
            while True:
                filename = input("Enter file name:\n(e.g. \'sample.json\')\n")
                # Loads the json file into as a database named 'schedule'
                try:
                    schedule = pd.read_json(filename)
                    # Keys organized by row
                    names = schedule.keys()
                    schedule = schedule.transpose()

                    connection = sqlite3.connect('schedule.db')
                    cursor = connection.cursor()
                    # Creating a table for the database
                    # Data types may need to be fixed in accordance to project requirements
                    cursor.execute('''CREATE TABLE IF NOT EXISTS schedule(Date INT, 
                    Name TEXT, Start INT, Duration INT, Type TEXT, EndDate INT, 
                    Frequency INT)''')
                    # Entering data into the table
                    for i in range(len(schedule)):
                        cursor.execute("INSERT INTO schedule(Date, Name, Start, Duration, Type, EndDate, Frequency) VALUES(?, ?, ?, ?, ?, ?, ?)",
                        (names[i], schedule['Name'][i], schedule['Start'][i], schedule['Duration'][i], schedule['Type'][i], schedule['EndDate'][i],
                        schedule['Frequency'][i]))
                    connection.commit()
                    connection.close()
                except FileNotFoundError:
                    print("There is no file of that name.\nPlease try again...")
                    # Will ask if they want to reenter again (also used to quit if 
                    # accidentally confirmed with 'y'.)
                    loadsch = input("Do you want to reenter a file name?").lower()
                    if loadsch[0] == 'n':
                        break