import json

def menu():
    # Asks if they want to load a schedule
    loadsch = input("Do you have a schedule to load?").lower()
    if loadsch[0] == 'y':
        while True:
            filename = input("Enter file name:\n(e.g. \'sample.json\')")
            # Loads the json file into as a dictionary named 'schedule'
            try:
                jsonfile = open(filename)
                schedule = json.load(jsonfile)
                break
            except FileNotFoundError:
                print("There is no file of that name.\nPlease try again...")

    print("1. Tasks\n2. Schedule\n3. End Program")
    userinput = input(int("Select an option:"))

    match userinput:
        case 1:
            print("\n1. Create\n2. Delete\n3. Edit\n4. View")
            choice = input(int("Option: "))
            # Insert nested switch state to account for all task modification options
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
                    
        case 3:
            continue
