import sqlite3
import tkinter
from PIL import Image, ImageTk
import PIL.Image
import tkinter.messagebox as tk
from tkinter.font import Font
from easygui import *
from tkinter import *
import random

conn = sqlite3.connect('leaveDb.db')
cur = conn.cursor()


conn.execute("CREATE TABLE if not exists balance (employee_id text,sickleave int,maternityleave int,emergencyleave int)")
conn.execute("CREATE TABLE if not exists status (leave_id int,employee_id text,leave text,Date1 text,Date2 text,days int,status text)")
conn.execute('''CREATE TABLE if not exists employee (employee_id text primary key,Name text,ContactNumber text,Password text)''')
conn.execute("CREATE TABLE if not EXISTS attendence (employee_id text primary key, presence int, leaves int, FOREIGN KEY (employee_id) REFERENCES employee (employee_id))")

def AdminLogin():
    message = "Enter Username and Password"
    title = "Admin Login"
    fieldnames = ["Username", "Password"]
    field = []
    field = multpasswordbox(message, title, fieldnames)
    if field[0] == 'raghav' and field[1] == 'raghav123':
        tkinter.messagebox.showinfo("Admin Login", "Login Successfully")
        adminwindow()
    else:
        tk.showerror("Error info", "Incorrect username or password")


def EmployeeLogin():
    message = "Enter Employee ID and Password"
    title = "Employee Login"
    fieldnames = ["Employee ID", "Password"]
    field = []
    field = multpasswordbox(message, title, fieldnames)

    for row in conn.execute('SELECT * FROM employee'):
        if field[0] == row[0] and field[1] == row[3]:
            global login
            login = field[0]
            f = 1
            print("Success")
            tkinter.messagebox.showinfo("Employee Login", "Login Successfully")
            EmployeeLoginWindow()
            break
    if not f:
        print("Invalid")
        tk.showerror("Error info", "Incorrect employee id or password")

def Employeelogout():
    global login
    login = -1
    LoginWindow.destroy()


def EmployeeLeaveStatus():
    global leaveStatus
    leaveStatus = []
    for i in conn.execute('SELECT * FROM status where employee_id=?', (login,)):
        leaveStatus = i

    WindowStatus()


def EmployeeAllStatus():
    allStatus = Toplevel()
    txt = Text(allStatus)
    for i in conn.execute('SELECT * FROM status where employee_id=?', (login,)):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def EmployeeInformationWindow():
    employeeInformation = Toplevel()
    txt = Text(employeeInformation)
    for i in conn.execute('SELECT employee_id,Name,ContactNumber FROM employee where employee_id=?', (login,)):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def EmployeeAllInformationWindow():
    allEmployeeInformation = Toplevel()
    txt = Text(allEmployeeInformation)
    for i in conn.execute('SELECT employee_id,Name,ContactNumber FROM employee'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def WindowStatus():
    StatusWindow = Toplevel()
    label_1 = Label(StatusWindow, text="Employee ID=", fg="blue", justify=LEFT, font=("Calibri", 16))
    label_2 = Label(StatusWindow, text=leaveStatus[1], font=("Calibri", 16))
    label_3 = Label(StatusWindow, text="Type=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_4 = Label(StatusWindow, text=leaveStatus[2], font=("Calibri", 16))
    label_5 = Label(StatusWindow, text="start=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_6 = Label(StatusWindow, text=leaveStatus[3], font=("Calibri", 16))
    label_7 = Label(StatusWindow, text="end=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_8 = Label(StatusWindow, text=leaveStatus[4], font=("Calibri", 16))
    label_9 = Label(StatusWindow, text="Status:", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_10 = Label(StatusWindow, text=leaveStatus[6], font=("Calibri", 16))
    label_11 = Label(StatusWindow, text="leave_id:", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_12 = Label(StatusWindow, text=leaveStatus[0], font=("Calibri", 16))
    label_11.grid(row=0, column=0)
    label_12.grid(row=0, column=1)
    label_1.grid(row=1, column=0)
    label_2.grid(row=1, column=1)
    label_3.grid(row=2, column=0)
    label_4.grid(row=2, column=1)
    label_5.grid(row=3, column=0)
    label_6.grid(row=3, column=1)
    label_7.grid(row=4, column=0)
    label_8.grid(row=4, column=1)
    label_9.grid(row=5, column=0)
    label_10.grid(row=5, column=1)


def balance():
    global login
    #check = (login,)
    global balanced
    balanced = []
    for i in conn.execute('SELECT * FROM balance WHERE employee_id = ?',(login,)):
        balanced = i

    WindowBalance()


def WindowBalance():
    balanceWindow = Toplevel()
    label_1 = Label(balanceWindow, text="Employee ID=", fg="blue", justify=LEFT, font=("Calibri", 16))
    label_2 = Label(balanceWindow, text=balanced[0], font=("Calibri", 16))
    label_3 = Label(balanceWindow, text="Sick Leave=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_4 = Label(balanceWindow, text=balanced[1], font=("Calibri", 16))
    label_5 = Label(balanceWindow, text="Maternity Leave=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_6 = Label(balanceWindow, text=balanced[2], font=("Calibri", 16))
    label_7 = Label(balanceWindow, text="Emergency Leave=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_8 = Label(balanceWindow, text=balanced[3], font=("Calibri", 16))
    label_1.grid(row=0, column=0)
    label_2.grid(row=0, column=1)
    label_3.grid(row=1, column=0)
    label_4.grid(row=1, column=1)
    label_5.grid(row=2, column=0)
    label_6.grid(row=2, column=1)
    label_7.grid(row=3, column=0)
    label_8.grid(row=3, column=1)


def apply():
    message = "Enter the following details "
    title = "Leave Apply"
    fieldNames = ["Employee ID", "From", "To", "days"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    if fieldValues is not None:
        message1 = "Select type of leave"
        title1 = "Type of leave"
        choices = ["Sick leave", "Maternity leave", "Emergency leave"]
        choice = choicebox(message1, title1, choices)
        leaveid = random.randint(1, 1000)

        conn.execute("INSERT INTO status(leave_id,employee_id,leave,Date1,Date2,days,status) VALUES (?,?,?,?,?,?,?)",
                     (leaveid, fieldValues[0], choice, fieldValues[1], fieldValues[2], fieldValues[3], "Pending"))
        conn.commit()

def LeaveApproval():
    message = "Enter leave_id"
    title = "leave approval"
    fieldNames = ["Leave_id"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    print(fieldValues)
    message1 = "Approve/Deny"
    title1 = "leave approval"
    choices = ["approve", "deny"]
    choice = choicebox(message1, title1, choices)
    print("new one______________________________________________________________________________________________________")
    print("choice",choice)

    conn.execute("UPDATE status SET status = ? WHERE leave_id= ?", (choice, fieldValues[0]))
    conn.commit()

    if choice == 'approve':
        print(0)
        cur.execute("SELECT leave FROM status WHERE leave_id=?", (fieldValues[0],))
        row = cur.fetchall()
        col = row
        print(col)
        print("col 0 0",col[0][0])
        for row in conn.execute("SELECT employee_id FROM status WHERE leave_id=?", (fieldValues[0],)):
            print(2)
            exampleId = row[0]
            print("exampleId",exampleId)

        for row in conn.execute("SELECT days FROM status WHERE leave_id=?", (fieldValues[0],)):
            print(2)
            exampleDays = row[0]
            print("Exampledays",exampleDays)


        for row in conn.execute("SELECT sickleave from balance where employee_id=?", (exampleId,)):
            balance = row[0]
            print("balance",balance)


        for row in conn.execute("SELECT maternityleave from balance where employee_id=?", (exampleId,)):
            balance1 = row[0]
            print("balance1",balance1)

        for row in conn.execute("SELECT emergencyleave from balance where employee_id=?", (exampleId,)):
            balance2 = row[0]
            print("balance2",balance2)

        if (col[0][0] == 'sickleave'):
            print(3)
            conn.execute("UPDATE balance SET sickleave =? WHERE employee_id= ?", ((balance - exampleDays), (exampleId)))
            conn.commit()

        if (col[0][0] == 'maternityleave'):
            print(3)
            conn.execute("UPDATE balance SET maternityleave =? WHERE employee_id= ?", ((balance1 - exampleDays), (exampleId)))
            conn.commit()

        if (col[0][0] == 'emergencyleave'):
            print(3)
            conn.execute("UPDATE balance SET emergencyleave =? WHERE employee_id= ?", ((balance2 - exampleDays), (exampleId)))
            conn.commit()


def leavelist():
    leavelistwindow = Toplevel()
    txt = Text(leavelistwindow)
    for i in conn.execute('SELECT * FROM status'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def registration():
    message = "Enter Details of Employee"
    title = "Registration"
    fieldNames = ["Employee ID", "Name", "Contact Number", "Password"]
    fieldValues = []
    fieldValues = multpasswordbox(message, title, fieldNames)
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

        if errmsg == "": break


        fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
    conn.execute("INSERT INTO employee(employee_id,Name,ContactNumber,Password) VALUES (?,?,?,?)",
                 (fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3]))
    conn.execute("INSERT INTO balance(employee_id,sickleave,maternityleave,emergencyleave) VALUES (?,?,?,?)", (fieldValues[0], 12, 12, 50))
    conn.execute("INSERT INTO attendence(employee_id,presence,leaves) VALUES (?,?,?)", (fieldValues[0], 0, 0))
    conn.commit()
    tkinter.messagebox.showinfo("Employee Registration", "Successfully Registered")







def attendencemark():
    message = "Enter the attendence details "
    title = "attendence"
    fieldNames = ["Employee ID"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    cur.execute("SELECT presence,leaves FROM attendence WHERE employee_id=?", (fieldValues[0],))
    row = cur.fetchall()
    print("row:",row)
    message1 = "mark attendence"
    title1 = "attendence"
    choices = ["Present","Absent"]
    choice = choicebox(message1, title1, choices)
    print("choice:",choice)
    present = row[0][0]
    leave = row[0][1]
    if choice == 'Present':
        present=present+1
    if choice == 'Absent':
        leave=leave+1
    conn.execute("update attendence set presence=? , leaves=? where employee_id=? ",(present,leave,fieldValues[0]))
    conn.commit()
    tkinter.messagebox.showinfo("Attendence","Attendence is marked!")



def seeattendence():
    employeeattendence = Toplevel()
    txt = Text(employeeattendence)
    cur.execute("SELECT presence,leaves FROM attendence WHERE employee_id=?", (login,))
    row = cur.fetchall()
    x1="total present: "
    x2="total absent: "
    x3="your attendence: "
    x4=row[0][0]+row[0][1]
    x5=(row[0][0]/x4)*100
    txt.insert(INSERT, x1)
    txt.insert(INSERT,row[0][0])
    txt.insert(INSERT, '\n')
    txt.insert(INSERT, x2)
    txt.insert(INSERT, row[0][1])
    txt.insert(INSERT, '\n')
    txt.insert(INSERT, x3)
    txt.insert(INSERT, x5)
    txt.pack()




def EmployeeLoginWindow():
    # employee login window after successful login
    global LoginWindow
    LoginWindow = Toplevel()
    LoginWindow.wm_attributes('-fullscreen', '1')
    LoginWindow.configure(background="#87ceeb")

    MainLabel4 = Label(LoginWindow, text="Leave Management System", bd=12,
                       font=("Calibri", 30, "bold"), bg="blue", fg="white", pady=3)
    # MainLabel.place(relx=0.0, rely=0.7)
    # MainLabel.pack(fill=X)
    MainLabel4.pack(fill=X)

    # Background_Label = Label(LoginWindow, image=filename)
    # Background_Label.place(x=0, y=0, relwidth=1, relheight=1)

    informationEmployee = Button(LoginWindow, text='Employee information', command=EmployeeInformationWindow, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    informationEmployee['font'] = BtnFont
    informationEmployee.pack(fill=X)

    submit = Button(LoginWindow, text='Submit Leave', command=apply, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    submit['font'] = BtnFont
    submit.pack(fill=X)

    LeaveBalance = Button(LoginWindow, text='Leave Balance', command=balance, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    LeaveBalance['font'] = BtnFont
    LeaveBalance.pack(fill=X)

    LeaveApplicationStatus = Button(LoginWindow, text='Last leave status', command=EmployeeLeaveStatus, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    LeaveApplicationStatus['font'] = BtnFont
    LeaveApplicationStatus.pack(fill=X)

    AllLeaveStatus = Button(LoginWindow, text='All leave status', command=EmployeeAllStatus, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    AllLeaveStatus['font'] = BtnFont
    AllLeaveStatus.pack(fill=X)



    Seeattendance = Button(LoginWindow, text='Check Attendance', bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                       font=("Calibri", 36, "bold"), pady=3, command=seeattendence)
    Seeattendance['font'] = BtnFont
    Seeattendance.pack(fill=X)



    LogoutBtn = Button(LoginWindow, text='Logout', bd=12, relief=GROOVE, fg="red", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3, command=Employeelogout)
    LogoutBtn['font'] = BtnFont
    LogoutBtn.pack(fill=X)

    informationEmployee.pack()
    submit.pack()
    LeaveBalance.pack()
    LeaveApplicationStatus.pack()
    AllLeaveStatus.pack()
    LogoutBtn.pack()
    ExitBtn.pack()














def adminwindow():
    adminmainwindow = Toplevel()
    adminmainwindow.wm_attributes('-fullscreen', '1')
    adminmainwindow.configure(background="#87ceeb")
    # Background_Label = Label(adminmainwindow, image=filename)

    # root2 = Tk()
    # root.wm_attributes('-fullscreen', True)

    MainLabel3 = Label(adminmainwindow, text="Leave Management System", bd=12,
                       font=("Calibri", 30, "bold"), bg="blue", fg="white", pady=3)
    # MainLabel.place(relx=0.0, rely=0.7)
    # MainLabel.pack(fill=X)
    MainLabel3.pack(fill=X)

    # Background_Label.place(x=0, y=3, relwidth=1, relheight=1)
    # Background_Label.pack()
    informationEmployee = Button(adminmainwindow, text='All Employee information', command=EmployeeAllInformationWindow, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    informationEmployee['font'] = BtnFont
    informationEmployee.pack(fill=X)



    LeaveListButton = Button(adminmainwindow, text='Leave approval list', command=leavelist, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    LeaveListButton['font'] = BtnFont
    LeaveListButton.pack(fill=X)

    ApprovalButton = Button(adminmainwindow, text='Approve leave', command=LeaveApproval, bd=12, relief=GROOVE, fg="blue", bg="#ffffb3",
                      font=("Calibri", 36, "bold"), pady=3)
    ApprovalButton['font'] = BtnFont
    ApprovalButton.pack(fill=X)




    Markattendance = Button(adminmainwindow, text='Mark attendance', command=attendencemark, bd=12, relief=GROOVE,
                            fg="blue", bg="#ffffb3",
                            font=("Calibri", 36, "bold"), pady=3)
    Markattendance['font'] = BtnFont
    Markattendance.pack(fill=X)




    LogoutBtn = Button(adminmainwindow, text='Logout', command=adminmainwindow.destroy, bd=12, relief=GROOVE, fg="red",
                     bg="#ffffb3",
                     font=("Calibri", 36, "bold"), pady=3)
    LogoutBtn['font'] = BtnFont
    LogoutBtn.pack(fill=X)

    informationEmployee.pack()
    LeaveListButton.pack()
    ApprovalButton.pack()
    ExitBtn.pack()


root = Tk()
#root.state('zoomed') ##for title bar
root.wm_attributes('-fullscreen', True)
root.title("Leave Management System")

root.iconbitmap(default='leavelogo.ico')
filename = PhotoImage(file="background.gif")

root.configure(background="#C0C0C0")
# background_label = Label(root, image=filename)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

BtnFont = Font(family='Calibri(Body)', size=20)
# MainLabel = Label(root, text="Leave Management System", bd=12, relief=GROOVE, fg="White", bg="blue",
#                       font=("Calibri", 36, "bold"), pady=3)
MainLabel2 = Label(root, text="Leave Management System", bd=12,
                      font=("Calibri", 30, "bold"), bg="#708090", fg="white" , pady=3)
#MainLabel.place(relx=0.0, rely=0.7)
#MainLabel.pack(fill=X)
MainLabel2.pack(fill=X)

img = PIL.Image.open("employee2.jpg")
img = img.resize((500, 300))
img2 = ImageTk.PhotoImage(img)

lb = Label(image = img2)
lb.pack(pady=30)

im = PhotoImage(file='login.gif')

AdminLgnBtn = Button(root, text='Admin login',  bd=12, relief=GROOVE, fg="blue", bg="#F0E68C",
                      font=("Calibri", 36, "bold"), pady=3, command=AdminLogin,width=30)
AdminLgnBtn['font'] = BtnFont
#AdminLgnBtn.place(relx=0.0, rely=0.7)
AdminLgnBtn.pack()


LoginBtn = Button(root, text='Employee login', bd=12, relief=GROOVE, fg="blue", bg="#F0E68C",
                      font=("Calibri", 36, "bold"), pady=3, command=EmployeeLogin,width=30)
LoginBtn['font'] = BtnFont
#LoginBtn.place(relx=0.0, rely=0.8)
LoginBtn.pack()


EmployeeRegistration = Button(root, text='Employee registration', command=registration, bd=12, relief=GROOVE, fg="blue", bg="#F0E68C",
                      font=("Calibri", 36, "bold"), pady=3,width = 30)
EmployeeRegistration['font'] = BtnFont
#EmployeeRegistration.place(relx=0.0, rely=0.9,width=90)
EmployeeRegistration.pack()

ExitBtn = Button(root, text='Exit', command=root.destroy, bd=12, relief=GROOVE, fg="red", bg="#F0E68C",
                      font=("Calibri", 36, "bold"), pady=3,width=30)
ExitBtn['font'] = BtnFont
#ExitBtn.place(relx=0.0, rely=0.5)
ExitBtn.pack()
#MainLabel.pack()
# AdminLgnBtn.pack()
# LoginBtn.pack()
# EmployeeRegistration.pack()
# ExitBtn.pack()


root.mainloop()
