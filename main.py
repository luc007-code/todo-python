import platform
import os
import shutil
import time
import sys, getopt
file="tasks.db"


# check the system in use to clean the screen
OS = platform.system()


def CleanScreen():
    # clean the screen
    if OS == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def MakeHeaders(Msg, Char):
    import shutil
    terminal = shutil.get_terminal_size()
    width = terminal.columns
    Msg_len = len(Msg)
    Total_Char = width - (Msg_len + 2)
    return str(Char * int(Total_Char/2) + " " + Msg + " " + Char * int(Total_Char/2))


def MakeLines(Char):
    terminal = shutil.get_terminal_size()
    width = terminal.columns
    return str(Char * int(width))


def MakeMenuHeader(Menu, char):
    CleanScreen()
    print(MakeHeaders(str(Menu),str(char)))
    print(MakeLines(str(char)))


def MainMenu():
    MakeMenuHeader("Get things DONE!","*")
    print(" 1- Add a task\n 2- Delete a task\n 3- List task\n q- Quit")
    print(MakeLines("-"))
    opt=input("Choose an option: ")
    return opt 


def ListTasks(CMD):
    with open(file, "r") as f:
        FileSplitted = f.readlines()
    if (len(FileSplitted) -1) == 0:
        print("Nice! you have no tasks to do!")
    else:
        for x in range(len(FileSplitted)-1):
            print(str(x) + " - " + FileSplitted[x])
        if not CMD == True:
            input("Hit enter to exit to main menu")


def WriteTask(task):
    try:
        with open(file,"a+") as db:
            db.write(task)
        print("Saved!")
    except (IOError, FileNotFoundError) as e:
        print(f"Failed to write to the file {file}")
        raise e


def AddTask():
    MakeMenuHeader("Add tasks","-")
    task = str(input("Type a task to be added to the list: "))
    date = str(input("Type a deadline date mm-dd-yy: "))
    print(f"Task: {task}")

    ret = str(input("Is this task right? (y/n): "))
    if ret in ('y','Y','yes','Yes','YES'):
        WriteTask(task)


def RemoveTasks():
    MakeMenuHeader("Remove a task","-")
    with open(file,"r") as f:
        FileSplitted = f.readlines()
    if (len(FileSplitted) -1) == 0:
        print("Nice! you have no tasks to do!")
    else:
        for x in range(len(FileSplitted)-1):
            print(str(x) + " - " + FileSplitted[x])
        ret=int(input("Wich one do you want to remove? [numbers]: "))
        if ret > (len(FileSplitted)-2):
            print(f"Choose a number from 0 to {len(FileSplitted)-2}")
        else:
            try:
                # cleanup the file
                with open(file, 'w'): pass
                FileSplitted.pop(ret)
                with open(file, 'w') as f:
                    for x in range(len(FileSplitted)-1):
                        f.write(FileSplitted[x])
                print(f"task {ret} removed")
            except ValueError:
                print("Only numbers are accepted")


def ScreenManual():
    while True:
       opt=MainMenu()
       if opt == "1":
           print("Create function add task")
           AddTask()
       elif opt == "2":
           print("Create function Delete task")
           RemoveTasks()
       elif opt == "3":
           print("create function list tasks")
           ListTasks(False)
       elif opt == "q":
           quit()
           break
       else:
           print("Invalid Option, try again")
   
       time.sleep(1)


def ShowHelp():
       MakeMenuHeader("Help!","*")
       print("The following options are available in the command line mode: \n -t or --task  : adds a task using the argument as a name \
                                                   \n -d or --date  : adds dead line for this added task dateformat MM-DD-YY\
                                                   \n -l or --list  : lists all tasks\
                                                   \n -h or --help  : show this help\
                                                   \n\n\
             Examples:\n\
             Add a task:\n\
             " + sys.argv[0] + " -t Task1 -d 07-30-18\n\n\
             IMPORTANT:\n\
             if you whant to use this program in a screen mode, just use it without arguments! ;)")


def WithArgs():
    try:
       opts, args = getopt.getopt(sys.argv[1:],"d:hlt:",["task=","date=","help","list"])
    except getopt.GetoptError:
        ShowHelp()
    date, task = '',''
    for opt, arg in opts:
       if opt in ('-t', 'task'):
           task = arg
       if opt in ('-d', 'date'):
           date = arg
       if opt in ('-h', 'help'):
           ShowHelp()
           quit()
       if opt in ('-l', 'list'):
           ListTasks(True)
           quit()
    print(task,date)
    WriteTask(task)

if len(sys.argv[1:]) > 0:
    WithArgs()
else:
    print("manual")
    ScreenManual()
