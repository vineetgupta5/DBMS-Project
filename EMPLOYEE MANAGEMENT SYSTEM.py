import mysql.connector
from datetime import date

# -------- DATABASE CONNECTION --------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vineet@5665",   
    database="ems"
)

cursor = conn.cursor()
print("\nConnected to EMS Database!\n")


# -------- FUNCTIONS --------

def add_department():
    dept_id = input("Enter Department ID: ")
    name = input("Enter Department Name: ")

    cursor.execute(
        "INSERT INTO department (department_id, department_name) VALUES (%s, %s)",
        (dept_id, name)
    )
    conn.commit()
    print("Department added!\n")


def add_employee():
    
    cursor.execute("SELECT * FROM department")
    print("\nDepartments:")
    for row in cursor.fetchall():
        print(row)

    emp_id = input("\nEnter Employee ID: ")
    name = input("Name: ")
    gender = input("Gender: ")
    phone = input("Phone: ")
    email = input("Email: ")
    hire_date = input("Hire Date (YYYY-MM-DD): ")
    job_title = input("Job Title: ")
    dept_id = input("Department ID from list above: ")

    query = """
    INSERT INTO employee
    (employee_id, name, gender, phone, email, hire_date, job_title, department_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (emp_id, name, gender, phone, email, hire_date, job_title, dept_id))
    conn.commit()
    print("Employee added!\n")


def add_salary():
    emp_id = input("Employee ID: ")
    basic = float(input("Basic Salary: "))
    bonus = float(input("Bonus: "))
    deductions = float(input("Deductions: "))

    net = basic + bonus - deductions

    cursor.execute("""
        INSERT INTO salary
        (employee_id, basic_salary, bonus, deductions, net_salary)
        VALUES (%s,%s,%s,%s,%s)
    """, (emp_id, basic, bonus, deductions, net))

    conn.commit()
    print("Salary added!\n")


def mark_attendance():
    emp_id = input("Employee ID: ")
    att_date = input("Date (YYYY-MM-DD) or press Enter for today: ")

    if att_date == "":
        att_date = date.today()

    status = input("Status (Present/Absent): ")

    cursor.execute("""
        INSERT INTO attendance (employee_id, date, status)
        VALUES (%s,%s,%s)
        ON DUPLICATE KEY UPDATE status = VALUES(status)
    """, (emp_id, att_date, status))

    conn.commit()
    print("Attendance recorded!\n")


def apply_leave():
    emp_id = input("Employee ID: ")
    leave_type = input("Leave Type (Sick/Casual/Paid): ")
    start = input("Start Date (YYYY-MM-DD): ")
    end = input("End Date (YYYY-MM-DD): ")

    cursor.execute("""
        INSERT INTO leaves
        (employee_id, leave_type, start_date, end_date, status)
        VALUES (%s,%s,%s,%s,'Pending')
    """, (emp_id, leave_type, start, end))

    conn.commit()
    print("Leave applied (Pending)!\n")


def view_pending_leaves():
    cursor.execute("""
        SELECT leave_id, employee_id, leave_type, start_date, end_date
        FROM leaves
        WHERE status='Pending'
    """)
    rows = cursor.fetchall()

    print("\nPending Leaves:")
    for row in rows:
        print(row)
    print()


def approve_reject_leave():
    leave_id = input("Enter Leave ID: ")
    decision = input("Approve or Reject? ").capitalize()

    if decision not in ["Approve", "Reject"]:
        print("Invalid choice\n")
        return

    cursor.execute("""
        UPDATE leaves
        SET status=%s
        WHERE leave_id=%s
    """, (decision + "d", leave_id))

    conn.commit()
    print("Leave status updated!\n")


def view_employees():
    cursor.execute("""
        SELECT e.employee_id, e.name, d.department_name
        FROM employee e
        LEFT JOIN department d
        ON e.department_id = d.department_id
    """)
    rows = cursor.fetchall()

    print("\nEmployees:")
    for row in rows:
        print(row)
    print()


def view_attendance():
    emp_id = input("Employee ID: ")

    cursor.execute("""
        SELECT date, status
        FROM attendance
        WHERE employee_id=%s
        ORDER BY date
    """, (emp_id,))

    rows = cursor.fetchall()

    print("\nAttendance:")
    for row in rows:
        print(row)
    print()


def view_leave():
    emp_id = input("Employee ID: ")

    cursor.execute("""
        SELECT leave_type, start_date, end_date, status
        FROM leaves
        WHERE employee_id=%s
    """, (emp_id,))

    rows = cursor.fetchall()

    print("\nLeave Records:")
    for row in rows:
        print(row)
    print()


def delete_employee():
    emp_id = input("Enter Employee ID to delete: ")

    confirm = input("Are you sure? (yes/no): ").lower()
    if confirm != "yes":
        print("Deletion cancelled.\n")
        return

    cursor.execute("DELETE FROM employee WHERE employee_id = %s", (emp_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("Employee not found.\n")
    else:
        print("Employee deleted successfully!")
        print("Salary, attendance, and leave records removed automatically.\n")


# -------- MENU --------

while True:
    print("========== EMS MENU ==========")
    print("1. Add Department")
    print("2. Add Employee")
    print("3. Add Salary")
    print("4. Mark Attendance")
    print("5. Apply Leave")
    print("6. View Employees")
    print("7. View Attendance")
    print("8. View Leave")
    print("9. View Pending Leaves")
    print("10. Approve/Reject Leave")
    print("11. Delete Employee")
    print("11. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_department()
    elif choice == "2":
        add_employee()
    elif choice == "3":
        add_salary()
    elif choice == "4":
        mark_attendance()
    elif choice == "5":
        apply_leave()
    elif choice == "6":
        view_employees()
    elif choice == "7":
        view_attendance()
    elif choice == "8":
        view_leave()
    elif choice == "9":
        view_pending_leaves()
    elif choice == "10":
        approve_reject_leave()
    elif choice == "11":
        delete_employee()
    elif choice== "12":
        break
    else:
        print("Invalid choice!\n")

print("Program Closed.")
conn.close()
