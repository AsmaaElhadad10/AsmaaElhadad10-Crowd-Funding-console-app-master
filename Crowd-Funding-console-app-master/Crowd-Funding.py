import re
import json
import datetime
from prettytable import PrettyTable

# Regular expressions for data validation
mail_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
phone_regex = re.compile(r'^(?:\+?01)?[09]\d{10,10}$')

# File paths for data storage
USERS_FILE = "files/users.json"
PROJECTS_FILE = "files/projects.json"

'''<<--------------------- Load -------------------->>'''
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file '{file_path}'.")
        return None

'''<<--------------------- Save -------------------->>'''
def save_json(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file '{file_path}'.")

'''<<--------------------- Valid Date -------------------->>'''
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False

'''<<--------------------- Edit Project -------------------->>'''
def edit_project(usr_id):
    project_id = input("Enter the ID of the project you want to edit: ")
    projects = load_json(PROJECTS_FILE)

    if projects:
        for project in projects:
            if str(project['id']) == project_id and str(project['owner_id']) == str(usr_id):
                print(f"Current project data: {project}")
                project['title'] = input("Enter new project title: ")
                project['details'] = input("Enter new project details: ")
                project['target'] = input("Enter new project total target: ")
                project['start_date'] = input("Enter new project start date (date format DD-MM-YYYY): ")
                project['end_date'] = input("Enter new project end date (date format DD-MM-YYYY): ")

                save_json(PROJECTS_FILE, projects)
                print("Project edited successfully!")
                return
        print("Project not found or you're not the owner of the project.")
    else:
        print("No projects found.")

'''<<--------------------- Search Project -------------------->>'''
def search_project():
    project_id = input("Enter the project ID you want to search for: ")
    projects = load_json(PROJECTS_FILE)

    if projects:
        t = PrettyTable(['ID', 'Title', 'Description', 'Total Target', 'Start', 'End', 'Owner ID'])
        for project in projects:
            if str(project['id']) == project_id:
                t.add_row([project['id'], project['title'], project['details'], project['target'],
                           project['start_date'], project['end_date'], project['owner_id']])
                print("Project found:")
                print(t)
                return
        print("No project found with the given ID.")
    else:
        print("No projects found.")

'''<<--------------------- Delete Project -------------------->>'''
def delete_project(usr_id):
    project_id = input("Enter the ID of the project you want to delete: ")
    projects = load_json(PROJECTS_FILE)

    if projects:
        filtered_projects = [project for project in projects
                             if not (str(project['id']) == project_id and str(project['owner_id']) == str(usr_id))]
        if len(filtered_projects) < len(projects):
            save_json(PROJECTS_FILE, filtered_projects)
            print("Project deleted successfully!")
        else:
            print("Project not found or you're not the owner of the project.")
    else:
        print("No projects found.")

'''<<--------------------- Display Projects -------------------->>'''
def display_projects():
    projects = load_json(PROJECTS_FILE)

    if projects:
        t = PrettyTable(['ID', 'Title', 'Description', 'Total Target', 'Start', 'End', 'Owner ID'])
        for project in projects:
            t.add_row([project['id'], project['title'], project['details'], project['target'],
                       project['start_date'], project['end_date'], project['owner_id']])
        print(t)
    else:
        print("No projects found.")

'''<<--------------------- Create Project -------------------->>'''
def create_project(usr_id):
    projects = load_json(PROJECTS_FILE) or []
    next_id = max((project['id'] for project in projects), default=0) + 1

    title = input("Enter Project title: ")
    details = input("Enter Project details: ")
    target = input("Enter Project total target: ")

    start_date_str = input("Enter Project start date (date format DD-MM-YYYY): ")
    while not is_valid_date(start_date_str):
        print("Invalid date format! Please use the format DD-MM-YYYY.")
        start_date_str = input("Enter Project start date (date format DD-MM-YYYY): ")
    start_date = datetime.datetime.strptime(start_date_str, '%d-%m-%Y').date()

    end_date_str = input("Enter Project end date (date format DD-MM-YYYY): ")
    while not is_valid_date(end_date_str):
        print("Invalid date format! Please use the format DD-MM-YYYY.")
        end_date_str = input("Enter Project end date (date format DD-MM-YYYY): ")
    end_date = datetime.datetime.strptime(end_date_str, '%d-%m-%Y').date()

    new_project = {
        "id": next_id,
        "title": title,
        "details": details,
        "target": target,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "owner_id": usr_id
    }

    projects.append(new_project)
    save_json(PROJECTS_FILE, projects)
    print("Project created successfully!")
    print(f"Your data: {new_project}")

'''<<--------------------- Login Menu -------------------->>'''
def login_menu(usr_id):
    print(f'Welcome! You are now logged in with user ID: {usr_id}')
    print('1. View All projects')
    print('2. Create New Project')
    print('3. Delete a Project')
    print('4. Search for a Project by ID')
    print('5. Edit a Project')
    print('6. Go to the Main Menu')
    print('0. Exit')

    while True:
        user_input = input('Enter Your selection: ')
        try:
            user_input = int(user_input)
            if user_input == 1:
                display_projects()
            elif user_input == 2:
                create_project(usr_id)
            elif user_input == 3:
                delete_project(usr_id)
            elif user_input == 4:
                search_project()
            elif user_input == 5:
                edit_project(usr_id)
            elif user_input == 6:
                return
            elif user_input == 0:
                print("Exiting...")
                exit()
            else:
                print("Invalid choice! Please choose again.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

'''<<--------------------- Register User -------------------->>'''
def register_user():
    first_name = input("Enter Your First Name: ")
    last_name = input("Enter Your Last Name: ")

    email = input("Enter your email: ")
    while not re.match(mail_regex, email):
        print("Invalid email format. Please enter a valid email address.")
        email = input("Enter your email: ")

    password = input("Enter Your Password: ")
    confirm_password = input("Confirm Your Password: ")
    while password != confirm_password:
        print("Passwords do not match. Please try again.")
        password = input("Enter Your Password: ")
        confirm_password = input("Confirm Your Password: ")

    phone = input("Enter your phone number: ")
    while not re.match(phone_regex, phone):
        print("Invalid phone number format. Please enter a valid phone number (Egyptian format).")
        phone = input("Enter your phone number: ")

    try:
        users = load_json(USERS_FILE) or []

        if not users:
            usr_id = 1
        else:
            last_user_id = int(users[-1]["id"])
            usr_id = last_user_id + 1

        new_user = {
            "id": str(usr_id),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "phone": phone
        }

        users.append(new_user)
        save_json(USERS_FILE, users)
        print("You have registered successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

'''<<--------------------- Login -------------------->>'''
def isUser():
    mail = input("Enter Your Email: ")
    passwd = input("Enter Your Password: ")

    users = load_json(USERS_FILE) or []

    for user in users:
        if mail == user['email'] and passwd == user['password']:
            usr_id = user['id']
            login_menu(usr_id)
            return

    print("Wrong Email or Password! Please register first!!")
    isUser()

'''<<--------------------- Main Menu -------------------->>'''
def main_menu():
    print('Welcome to the Crowd Funding Program')
    print('1. Registration')
    print('2. Login')
    print('0. Exit')

    while True:
        user_input = input('Enter Your selection: ')
        try:
            user_input = int(user_input)
            if user_input == 1:
                register_user()
                main_menu()
            elif user_input == 2:
                isUser()
                main_menu()
            elif user_input == 0:
                print("Exiting...")
                exit()
            else:
                print("Invalid choice! Please choose again.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")

if __name__ == "__main__":
    main_menu()
