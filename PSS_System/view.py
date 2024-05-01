def menu():
    print("1. Tasks\n2. Schedule\n3. End Program")
    userinput = input(int("Select an option:"))

    switch(userinput){
        case 1:
            print("1. Create\n2. Delete\n3. Edit\n4. View")
            choice = input(int("Option: "))
            # Insert nested switch state to account for all task modification options
            break;
        case 2:
            print("1. View Schedule\n2. Write Schedule")
            choice = input(int("Option: "))
            switch(choice){
                case 1:
                    print("1. View Day Schedule\n2. View Week Schedule\n3. View Month Schedule ")
                    viewer = input(int("Option: "))
                    # Take in date and display scheduled option
                    break;
                case 2: 
                    print("1. Write Day Schedule\n2. Write Week Schedule\n3. Write Month Schedule ")
                    viewer = input(int("Option: "))
                    break;
                default:
                    break;
            }
            break;
        case 3:

            break;
    }