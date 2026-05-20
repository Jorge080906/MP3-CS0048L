import datetime

global_teachers = {}       
global_students = {}    
global_history = {}     
current_teacher = ""       

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def is_valid_number(val_str):
    parts = val_str.split('.')
    if len(parts) == 1:
        return parts[0].isdigit()
    elif len(parts) == 2:
        return parts[0].isdigit() and parts[1].isdigit()
    return False

def register():
    global global_teachers, global_students, global_history
    print("\n--- Register / Create Teacher Profile First ---") 
    
    username = input("Enter new username: ")

    if username in global_teachers:
        print("Error: Username already exists.")
        return
        
    password = input("Enter new password: ")
    
    global_teachers[username] = password
    global_students[username] = {}
    global_history[username] = []
    
    print("Registration successful! You can now log in.")

def login():
    global current_teacher, global_teachers
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if username in global_teachers and global_teachers[username] == password:
        current_teacher = username
        print(f"Login successful. Welcome, {current_teacher}!")
    else:
        print("Error: Invalid username or password. (Note: Inputs are Case Sensitive) ")

def logout():
    global current_teacher
    print(f"\nLogging out {current_teacher}... Redirecting to the main menu. ")
    current_teacher =    ""

def add_student():
    global current_teacher, global_students, global_history
    print("\n--- Add Student ---")
    student_name = input("Enter student name to add to your roster: ")
    
    if student_name in global_students[current_teacher]:
        print("Error: The same student cannot be created twice. ")
    else:
        # Initialize student with an empty list of grades
        global_students[current_teacher][student_name] = []
        
        log_msg = f"[{get_timestamp()}] Added new student: {student_name}."
        global_history[current_teacher].append(log_msg)
        print(f"Success! {student_name} is now in your roster.")

def add_grade():
    global current_teacher, global_students, global_history
    print("\n--- Add Grade ---")
    student_name = input("Enter student name to grade: ")
    
    if student_name not in global_students[current_teacher]:
        print("Error: Student does not exist. Please check your spelling (Case Sensitive).")
        return
        
    grade_str = input("Enter grade (e.g., 95.5): ")
    
    if is_valid_number(grade_str):
        grade = float(grade_str)
        global_students[current_teacher][student_name].append(grade)
        
        log_msg = f"[{get_timestamp()}] Added grade {grade} to {student_name}."
        global_history[current_teacher].append(log_msg)
        print(f"Successfully added a grade of {grade} to {student_name}.")
    else:
        print("Error: Invalid grade entered. Please use digits only. ")

def remove_grade():
    global current_teacher, global_students, global_history
    print("\n--- Remove Grade ---")
    student_name = input("Enter student name to remove a grade from: ")
    
    if student_name not in global_students[current_teacher]:
        print("Error: Student does not exist.")
        return
        
    grade_str = input("Enter exact grade amount to remove: ")
    
    if is_valid_number(grade_str):
        grade = float(grade_str)
        
        if grade in global_students[current_teacher][student_name]:
            global_students[current_teacher][student_name].remove(grade)
            
            log_msg = f"[{get_timestamp()}] Removed grade {grade} from {student_name}."
            global_history[current_teacher].append(log_msg)
            print(f"Successfully removed the grade {grade} from {student_name}.")
        else:
            print("Error: Grade not found for this student.")
    else:
        print("Error: Invalid amount entered. ")

def transfer_grade():
    global current_teacher, global_students, global_history
    print("\n--- Transfer Grade (Fix Misassigned Grades) ---")
    from_student = input("Enter student who currently has the grade: ")
    
    if from_student not in global_students[current_teacher]:
        print("Error: Source student does not exist.")
        return
        
    to_student = input("Enter student who SHOULD receive the grade: ")
    if to_student not in global_students[current_teacher]:
        print("Error: Destination student does not exist.")
        return
        
    grade_str = input("Enter exact grade amount to transfer: ")
    
    if is_valid_number(grade_str):
        grade = float(grade_str)
        if grade in global_students[current_teacher][from_student]:
            global_students[current_teacher][from_student].remove(grade)
            global_students[current_teacher][to_student].append(grade)
            
            log_msg = f"[{get_timestamp()}] Transferred grade {grade} from {from_student} to {to_student}."
            global_history[current_teacher].append(log_msg)
            print(f"Successfully transferred grade {grade} from {from_student} to {to_student}.")
        else:
            print("Error: Grade not found in the source student's record.")
    else:
        print("Error: Invalid amount entered.")

def calculate_average():
    global current_teacher, global_students
    print("\n--- Calculate Student Average ---")
    student_name = input("Enter student name: ")
    
    if student_name in global_students[current_teacher]:
        grades = global_students[current_teacher][student_name]
        
        if len(grades) > 0:
            average = sum(grades) / len(grades)
            print(f"\n-- Grade Report --")
            print(f"Student: {student_name}")
            print(f"Total Grades Entered: {len(grades)}")
            print(f"Current Average: {average:.2f}")
        else:
            print(f"{student_name} currently has no grades on record.")
    else:
        print("Error: Student does not exist.")

def enforce_passing_grade():
    global current_teacher, global_students, global_history
    print("\n--- Enforce Passing Grade Audit ---")
    min_passing = 65.0
    
    print(f"Rule: Students with an average below {min_passing} will be flagged in history.")
    
    for student_name, grades in global_students[current_teacher].items():
        if len(grades) > 0:
            average = sum(grades) / len(grades)
            if average < min_passing:
                log_msg = f"[{get_timestamp()}] FLAG: {student_name} is failing with an average of {average:.2f}."
                global_history[current_teacher].append(log_msg)
                print(f"Warning: {student_name} is failing ({average:.2f}). Flagged in history.")
            else:
                print(f"{student_name} is safely passing ({average:.2f}).")
        else:
             print(f"{student_name} has no grades yet (N/A).")

def view_history():
    global current_teacher, global_history
    print(f"\n--- Gradebook History for {current_teacher} ---")
    
    history = global_history[current_teacher]
    if len(history) == 0:
        print("No actions found.")
    else:
        for record in history:
            print(record)

def main():
    global current_teacher
    
    while True:
        if current_teacher == "":
            print("\n=== Welcome to the Grade Book Manager ===")
            print("1. Login")
            print("2. Register")
            print("3. Exit System")
            
            choice = input("Enter choice (1-3): ")
            
            if choice == "1":
                login()
            elif choice == "2":
                register()
            elif choice == "3":
                print("Thank you for using the Grade Book Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        else:
            print(f"\n=== Active Session Menu ({current_teacher}) ===")
            print("1. Add Student")
            print("2. Add Grade")
            print("3. Remove Grade")
            print("4. Transfer Grade (Fix Error)")
            print("5. Calculate Student Average")
            print("6. Audit Failing Students")
            print("7. View Gradebook History")
            print("8. Log Out")
            
            choice = input("Enter choice (1-8): ")
            
            if choice == "1": add_student()
            elif choice == "2": add_grade()
            elif choice == "3": remove_grade()
            elif choice == "4": transfer_grade()
            elif choice == "5": calculate_average()
            elif choice == "6": enforce_passing_grade()
            elif choice == "7": view_history()
            elif choice == "8": logout()
            else: print("Invalid choice. Please enter a valid number.")

if __name__ == "__main__":
    main()