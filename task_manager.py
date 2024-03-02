
# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

# ============================================================== Importing libraries =================================================================

import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# ================================================================ Login =============================================================================
    
'''
This code reads usernames and password from the user.txt file to allow a user to login.
'''

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:
    print(''' 
___________________________________________________________________________________________________________________________________________________________________

                                                                      Login
___________________________________________________________________________________________________________________________________________________________________
          
''')
    curr_user = input("Please enter your username: ")
    curr_pass = input("Please enter your password: ")

    if curr_user not in username_password.keys():
        print("User does not exist")
        continue

    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue

    else:
        print()
        print("Login Successful!")
        logged_in = True

# ============================================================ Register new user =======================================================================

# Register new user function         

def reg_user(menu):

    if menu == 'r':
        # - Request input of a new username
        new_username = input("Please enter new username: ")
        # Checking if username already exists in textfile then show message to user to avoid username duplication.
        if new_username in username_password.keys():
            print("Username already exit, please enter new username.")

        else:
            # - Request input of a new password.
            new_password = input("Please enter new password: ")
            # - Request input of password confirmation.
            confirm_password = input("Please confirm password: ")
            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                username_password[new_username] = new_password
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data)) # writing user detail into user.txt file.
                    print("New user added")

            else:
                print("Passwords do no match") # if password not match, printing message.

# =============================================================== Add new task ==========================================================================

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Reading data from tasks.txt file.
with open("tasks.txt", 'r') as task_file:
    task_overview_data = task_file.read().split("\n")
    task_overview_data = [t for t in task_overview_data if t != ""]


task_list = []
for t_str in task_overview_data:
    current_task = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    current_task['username'] = task_components[0]
    current_task['title'] = task_components[1]
    current_task['description'] = task_components[2]
    current_task['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    current_task['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    current_task['completed'] = True if task_components[5] == "Yes" else False
    task_list.append(current_task)

def add_task(menu):

    '''
    Allow a user to add a new task to tasks.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.
    '''
    if menu == "a":
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
          
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")

        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Then get the current date.
        curr_date = date.today()

        ''' 
        Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.
        '''        
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

# =============================================================== View all task ==========================================================================        
                
def view_all(menu):
    '''
    Reads the tasks from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''
    if menu == "va":
        print('''
___________________________________________________________________________________________________________________________________________________________________

                                                                     All Tasks
___________________________________________________________________________________________________________________________________________________________________ 
              
''')
        for t in task_list:
            print()
            disp_str = f"Task:              \t {t['title']}\n"
            disp_str += f"Assigned to:      \t {t['username']}\n"
            disp_str += f"Date Assigned:    \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date:         \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Task Completed:   \t {t['completed']}\n"
            print(disp_str)
            print("_________________________________________________________________________________________________________")

# ============================================================== View my task ============================================================================

def view_mine(menu):
    '''
    Reads the task from task.txt file and check if task username match with current user
    then print task on the console with proper labeling.
    '''
    if menu == "vm":
        print('''
___________________________________________________________________________________________________________________________________________________________________

                                                                    Your Tasks
___________________________________________________________________________________________________________________________________________________________________        
              
''')
        print()    
        for index, t in enumerate(task_list):
            if t['username'] == curr_user:
                disp_str = f"{index}\tTask title:     \t {t['title']}\n"
                disp_str += f"        Assigned to:    \t {t['username']}\n"
                disp_str += f"        Date assigned:  \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"        Due date:       \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"        Task Completed: \t {t['completed']}\n"
                print(disp_str)
                
                print("____________________________________________________________________________________________________")
                print()

        '''
        if user want to select the task, user can select it by entering the task 
        corresponding number or go to main menu by entering -1.
        '''        
        task_num = input('''

Please enter the task number you want to select or enter -1 to return to main menu.
: ''')
        
        if task_num == "-1":
            print()
        else:
            # - Calling select task function on the base of user input.    
            select_task(int(task_num))        

def select_task(indx):
    '''
    Saving user selected task, 
    task index title
    task index description 
    task index username
    task index assigned_date 
    task index due_date 
    '''
    title = task_list[indx]['title']
    description = task_list[indx]['description']
    username = task_list[indx]['username']
    assigned_date = task_list[indx]['assigned_date'].strftime(DATETIME_STRING_FORMAT) 
    due_date = task_list[indx]['due_date'].strftime(DATETIME_STRING_FORMAT) 

    for t in task_list:
        # - checking if user selected task title match with task title in task_list.
        if title == t['title']: 
            # - if match then show message to user that user want to mark as complete to task or edit the task.
            mark = input('''
Choose option:       
m - Mark as complete.
ed - Edit the task.
: ''')
            # - If user select to mark as complete the task, then show two option yes / no.
            if mark == "m":
                mark_answer = input('''
Mark as complete, please select the option:          
y - yes
n - no
: ''')
                # - If user select yes.
                if mark_answer == "y":
                    with open('tasks.txt', 'r', encoding='utf-8') as file: 
                        data = file.readlines() 
                    data[indx] = f"{username};{title};{description};{due_date};{assigned_date};Yes\n"
                    with open('tasks.txt', 'w', encoding='utf-8') as file: 
                        file.writelines(data) 
                    print("Task successfully marked as completed.")

                # - If user select no.
                if mark_answer == "n":
                    with open('tasks.txt', 'r', encoding='utf-8') as file: 
                        data = file.readlines() 
                    data[indx] = f"{username};{title};{description};{due_date};{assigned_date};No\n"
                    with open('tasks.txt', 'w', encoding='utf-8') as file: 
                        file.writelines(data)
                    print("Task successfully marked as not completed.")

            # # - If user select to edit the task.
            elif mark == "ed":
                # - Checking user selected task is completed or not, if task is completed user can't update it.
                # - If task is not completed.
                if t['completed'] == False:
                    # - Asking user to enter the username, user want to assign the task.
                    updated_name = input("Please enter the name you want to assign the task: ")
                    # - Asking user to enter the updated_due_date of the task. 
                    updated_due_date = input("Please enter the new due date of task (YYYY-MM-DD): ")
                    with open('tasks.txt', 'r', encoding='utf-8') as file: 
                        data = file.readlines() 
                    data[indx] = f"{updated_name};{title};{description};{updated_due_date};{assigned_date};No\n"
                    with open('tasks.txt', 'w', encoding='utf-8') as file: 
                        file.writelines(data)
                    print("Task successfully updated.")

                # - If task is completed, then print message on console.
                elif t['completed'] == True:
                    print("Task is completed and it cannot be updated.")

            else:
                print("Invalid option")

# =============================================================== Generate reports ==========================================================================

# - Create task_overview.txt file, if it doesn't exist
if not os.path.exists("task_overview.txt"):
    with open("task_overview.txt", "w") as default_file:
        pass

# - Create user_overview.txt file, if it doesn't exist
if not os.path.exists("user_overview.txt"):
    with open("user_overview.txt", "w") as default_file:
        pass

# Reading data from task_overview file.
with open("task_overview.txt", 'r') as task_file:
    task_overview_data = task_file.read().split("\n")
    task_overview_data = [t for t in task_overview_data if t != ""]

task_overview_dict = []
for t_str in task_overview_data:
    current_task = {}
    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    current_task['total_tasks'] = task_components[0]
    current_task['completed_tasks'] = task_components[1]
    current_task['incompleted_tasks'] = task_components[2]
    current_task['overdue'] = task_components[3],
    current_task['completed_percentage'] = task_components[4],
    current_task['incompleted_percentage'] = task_components[5],
    current_task['report_generated_date'] = task_components[6]
    task_overview_dict.append(current_task)  
    
def task_overview():
    '''
    This method reads data from tasks.txt file and check
    how many total tasks,
    how many tasks are overdue,
    how many tasks are completed,
    how many tasks are incompleted
    then calculate the percentages of overdue and 
    incompleted tasks.
    then print 
    Total number of task,
    Total number of completed tasks.
    Total number of uncompleted tasks.
    Total number of tasks that haven't been completed and that are overdue.
    Percentage of tasks that are incomplete.
    Percentage of tasks that are overdue.
    '''
    incompleted = 0
    completed = 0
    overdue = 0
 
    for t in task_list:
        # - Checking tasks that are overdue.
        if date.today().strftime(DATETIME_STRING_FORMAT) > t['due_date'].strftime(DATETIME_STRING_FORMAT):
            overdue += 1 
        # - Checking tasks that are incompleted.
        elif t["completed"] == False:
            incompleted += 1
        # - Checking tasks that are completed.
        elif t["completed"] == True:   
            completed += 1
    # - Incompleted tasks percentage.
    incompleted_tasks_percentage = len(task_list) * incompleted / 100
    # - Completed tasks percentage.
    completed_tasks_percentage = len(task_list) * completed / 100 
    task_overview = {
            "total_tasks": str(len(task_list)),
            "completed_tasks": str(completed),
            "incompleted_tasks": str(incompleted),
            "overdue": str(overdue),
            "incompleted_percentage": str(incompleted_tasks_percentage),
            "completed_percentage": str(completed_tasks_percentage),
            "report_generated_date": datetime.today().strftime('%Y-%m-%d')
    }
    task_overview_dict.append(task_overview)

    # Writing tasks overview data into task_overview_file.
    with open("task_overview.txt", "w") as task_overview_file:
        task_list_to_write = []
        for t in task_overview_dict:
            str_attrs = [
                t['total_tasks'],
                t['completed_tasks'],
                t['incompleted_tasks'],
                t['overdue'],
                t['incompleted_percentage'],
                t['completed_percentage'],
                t['report_generated_date']
                ]
            task_list_to_write.append(";".join(str_attrs))
        task_overview_file.write("\n".join(task_list_to_write))
    print("""
___________________________________________________________________________________________________________________________________________________________________

                                                                   Task Overview Report
___________________________________________________________________________________________________________________________________________________________________
          
    """)
    for t in task_overview_dict:
           
        disp_str  = f"Report Generate Date:                      \t {t['report_generated_date']}\n\n"
        disp_str += f"Total number of tasks:                     \t {t['total_tasks']}\n"
        disp_str += f"Total number of completed tasks:           \t {t['completed_tasks']}\n"
        disp_str += f"Total number of incompleted:               \t {t['incompleted_tasks']}\n"
        disp_str += f"Total number of tasks that are overdue:    \t {t['overdue']}\n"
        disp_str += f"Percentage of tasks that are incompleted:  \t {t['incompleted_percentage']}%\n"
        disp_str += f"percentage of tasks that are completed:    \t {t['completed_percentage']}%\n"
        print(disp_str)

def user_overview():
    '''
    This method get record of 
    total users
    total tasks
    Name of user
    Total number of task assign to that user
    Percentage of total number of task assign to that user
    Percentage of total number of completed task assign to that user
    Percentage of total number of incompleted task assign to that user
    Percentage of total number of task that are overdue but must be commpleted assign to that user
    '''
    # Total users
    total_users = len(username_password.keys())
    # Total tasks
    total_tasks = len(task_list)
    print("""
___________________________________________________________________________________________________________________________________________________________________

                                                                   User Overview Report
___________________________________________________________________________________________________________________________________________________________________
                              
    """)
    print(f"Total User: {total_users}\n")
    print(f"Total Task: {total_tasks}\n")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    tasks_completed = 0
    tasks_must_be_completed = 0
    tasks_overdue = 0

    freq = {}
    for t in task_list:

        if t['username'] in freq:
            freq[t['username']] += 1
        
        else:
            freq[t['username']] = 1

    for key,value in freq.items():
        print()
        tasks_must_be_completed = 0
        tasks_completed = 0
        tasks_overdue = 0
        print(f"Name: {key}\n\nTotal Tasks: {value}\n")
        print(f"Percentage Total Task User: {len(task_list) * value / 100} %\n")
        
        for t in task_list:
            if t['username'] == key:
                
                # - Checking tasks that are overdue.
                if date.today().strftime(DATETIME_STRING_FORMAT) > t['due_date'].strftime(DATETIME_STRING_FORMAT):
                    tasks_overdue += 1

                # - Checking tasks that are incompleted.
                elif t["completed"] == False:
                    tasks_must_be_completed += 1

                # - Checking tasks that are completed.
                elif t["completed"] == True:   
                    tasks_completed += 1

        # - Calculating Percentage and printing on console.
        print(f"Percentage must be Task completed: {tasks_must_be_completed * value / 100} %\n") 
        print(f"Parcentage Task over due: {tasks_overdue * value / 100} %\n")
        print(f"Percentage task completed: {tasks_completed * value / 100} %\n")
        print('''
___________________________________________________________________________________________________________________________________________________________________
                      
''')  

def generate_reports(menu):
    '''
    This method call task_overview() and userover_view() 
    methods in one generate_report method.
    '''
    if menu == "gr":
        task_overview()
        user_overview()
        print("Reports generated successfully.")
        print()

# =============================================================== Display statistics ==========================================================================                      

def display_statistics(menu, curr_user):
    '''
    If the user is an admin they can display statistics about number of users
    and tasks.
    '''
    if menu == 'ds' and curr_user == 'admin':  
        num_users = len(username_password.keys())
        num_tasks = len(task_list)
        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------") 

# ===================================================================== Menu =================================================================================
            
while True:
    '''
    Check if user is admin, then display this menu to admin user.
    '''
    if curr_user == 'admin':
        menu = input('''
___________________________________________________________________________________________________________________________________________________________________

                                                                    Main Menu
___________________________________________________________________________________________________________________________________________________________________
                                                               
Please select one of the following Options:
                     
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports                     
ds - display statistics
e - Exit

: ''').lower()
    else:
        print()
        '''
        Check if user is normal user, then display this menu to user.
        '''
        menu = input('''
___________________________________________________________________________________________________________________________________________________________________

                                                                    Main Menu
___________________________________________________________________________________________________________________________________________________________________
                                          
Please select one of the following Options:
                     
a - Adding a task
va - View all tasks
vm - view my task
e - Exit

: ''').lower()

    if menu == 'r':
        reg_user(menu)

    elif menu == 'a':
        add_task(menu)

    elif menu == 'va':
        view_all(menu)

    elif menu == 'vm':
        view_mine(menu)        
    
    elif menu == "gr":
        generate_reports(menu)

    elif menu == 'ds' and curr_user == 'admin': 
       display_statistics(menu,curr_user)

    elif menu == 'e':
        print('''
___________________________________________________________________________________________________________________________________________________________________

                                                                    Good Bye
___________________________________________________________________________________________________________________________________________________________________
               
''')
    else:
        print("You have made a wrong choice, Please Try again")
