from search import *


def menu_loop(): 
    flag = True
    while (flag):
        cmd = input("Welcome to UoG Course Search. Please Enter Number of Option from the menu to continue...\n"
                    "1 - Search By Course Code\n"
                    "2 - Search By Course Name\n"
                    "3 - Search By Course Section\n"
                    "4 - Search By Department\n"
                    "5 - Help\n"
                    "6 - Exit\n"
                    )

        # Handle different command options
        if(cmd == "1" or cmd == "One" or cmd == "one"):
            # Call searchFunction
            print("Search by Course Code")
            name = input("Please enter the course code: ")
            v_course_list = searchByCourseCode(name)
            if (len(v_course_list["sections"])!=0):
                for rec in v_course_list["sections"]:
                    printCourse(rec)
            else:
                print("Cannot find it, try again!")
        elif(cmd == "2" or cmd == "Two" or cmd == "two"):
            print("Search by Course Name")
            name = input("Please enter the course name: ")
            # Call searchFunction
            v_course_list = searchByCourseName(name)
            if (len(v_course_list["sections"])!=0):
                for rec in v_course_list["sections"]:
                    printCourse(rec)
            else:
                print("Cannot find it, try again!")
            
        elif(cmd == "3" or cmd == "Three" or cmd == "three"):
            print("Search by Course Section")
            name = input("Please enter course code and section: ")
            v_course_list = searchByCourseSection(name)
           # Call searchFunction
            if (len(v_course_list["sections"])!=0):
                for rec in v_course_list["sections"]:
                    printCourse(rec)
            else:
                print("Cannot find it, try again!")
            
            # Call searchFunction
        elif(cmd == "4" or cmd == "Four" or cmd == "four"):
            print("Search by Course Department")
            name = input("Please enter the course department code: ")
            v_course_list = searchByCourseDepartment(name)
           # Call searchFunction
            if (len(v_course_list["sections"])!=0):
                for rec in v_course_list["sections"]:
                    printCourse(rec)
            else:
                print("Cannot find it, try again!")
            
            # Call searchFunction
        elif(cmd == "5" or cmd == "Help" or cmd == "help"):
            # Print help menu
            print("Help Menu\n")
            print("Select how you would like to search for courses and enter selection into main menu when prompted.\n"
                  "Once you have selected how you would like to search, you will be prompted to enter a search term.\n"
                  "When you have entered your input, press ENTER to find all occurences of your search term and print them to the screen.\n"
                  "Example input for search 1: CIS*3760\n"
                  "Example input for search 2: Software Engineering\n"
                  "Example input for search 3: CIS*3760 0101\n"
                  "Example input for search 4: CIS\n")
                  
       
        elif(cmd == "exit" or cmd == "Exit" or cmd == "6"):
            print("Thank you for using UoG Course Search.\nExiting Now.\n")
            flag = False
        else:
            print("Error with input, Please enter help to see proper format")
