from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1040x590+340+200")
        self.root.title("Employee")
        self.root.config(bg="skyblue")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_emp_gender = StringVar()
        self.var_emp_contact = StringVar()
        self.var_emp_name = StringVar()
        self.var_emp_dob = StringVar()
        self.var_emp_doj = StringVar()
        self.var_emp_email = StringVar()
        self.var_emp_pass = StringVar()
        self.var_emp_utype = StringVar()
        self.var_emp_salary = StringVar()

        searchFrame = LabelFrame(self.root, text="Search Employee", font=("goudy old style", 12, "bold"), bd=1, relief=RIDGE, bg="white", fg = "black")
        searchFrame.place(x=250, y=20, height=70, width=600)

        cmb_search = ttk.Combobox(searchFrame, textvariable=self.var_searchby, values=("Search", "Name", "Email", "Contact"),cursor="hand2", state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg = "lightgray").place(x=200, y=10, width=260)

        btn_search = Button(searchFrame, text="Search", command=self.search, font=("goudy old style", 15, "bold"), cursor="hand2",bg = "#059212", fg = "white", bd = 1, relief= RIDGE).place(x=470, y=9, width=120, height=30)

        title = Label(self.root, text = "Employee  Details", font = ("goudy old style", 20), bg = "#180161", fg = "white").place(x=50, y=110, width=950)

        lbl_id = Label(self.root, text = "ID", font=("goudy old style", 15, "bold"), bg = "skyblue", fg = "#180161").place(x=60, y=170)
        lbl_gender = Label(self.root, text = "Gender", font=("goudy old style", 15, "bold"), bg = "skyblue",fg = "#180161",).place(x=340, y=170)
        lbl_contacr = Label(self.root, text = "Mobile No.", font=("goudy old style", 15, "bold"), bg = "skyblue",fg = "#180161",).place(x=648, y=170)

        txt_id = Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15), bg = "#F6E96B").place(x=100, y=170, width=220)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_emp_gender, values=("Select", "Male", "Female", "Other"),cursor="hand2", state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_gender.place(x=420, y=170)
        cmb_gender.current(0)
        txt_contacr = Entry(self.root, textvariable=self.var_emp_contact, font=("goudy old style", 15), bg = "#F6E96B").place(x=750, y=170, width=220)

        lbl_name = Label(self.root, text = "Name", font=("goudy old style", 14, "bold"), bg = "skyblue", fg = "#180161").place(x=50, y=250)
        lbl_dob = Label(self.root, text = "Date of Birth", font=("goudy old style", 15, "bold"), bg = "skyblue", fg = "#180161").place(x=350, y=250)
        lbl_doj = Label(self.root, text = "Date of Joining", font=("goudy old style", 15, "bold"), bg = "skyblue", fg = "#180161").place(x=648, y=250)

        txt_name = Entry(self.root, textvariable=self.var_emp_name, font=("goudy old style", 15), bg = "#F6E96B").place(x=105, y=250, width=215)
        txt_dob = Entry(self.root, textvariable=self.var_emp_dob, font=("goudy old style", 15), bg = "#F6E96B").place(x=470, y=250, width=170)
        txt_doj = Entry(self.root, textvariable=self.var_emp_doj, font=("goudy old style", 15), bg = "#F6E96B").place(x=780, y=250, width=190)

        lbl_email = Label(self.root, text = "Email", font=("goudy old style", 15, "bold"), bg = "skyblue", fg = "#180161").place(x=50, y=330)
        lbl_pass = Label(self.root, text = "Password", font=("goudy old style", 15, "bold"), bg = "skyblue", fg = "#180161").place(x=350, y=330)
        lbl_utype = Label(self.root, text = "User Type", font=("goudy old style", 15, "bold"), bg = "skyblue", fg = "#180161").place(x=650, y=330)

        txt_email = Entry(self.root, textvariable=self.var_emp_email, font=("goudy old style", 15), bg = "#F6E96B").place(x=105, y=330, width=215)
        txt_pass = Entry(self.root, textvariable=self.var_emp_pass, font=("goudy old style", 15), bg = "#F6E96B").place(x=435, y=330, width=205)
        cmb_utype = ttk.Combobox(self.root, textvariable=self.var_emp_utype, values=("Select", "Admin", "Employee"),cursor="hand2", state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_utype.place(x=750, y=330, width=220)
        cmb_utype.current(0)

        lbl_address = Label(self.root, text = "Address", font=("goudy old style", 15, "bold"), bg = "skyblue", fg = "#180161").place(x=50, y=410)
        lbl_salary = Label(self.root, text = "Salary", font=("goudy old style", 15, "bold"), bg = "skyblue", fg = "#180161").place(x=460, y=410)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg = "#F6E96B")
        self.txt_address.place(x=125, y=410, width=320, height=70)
        txt_salary = Entry(self.root, textvariable=self.var_emp_salary, font=("goudy old style", 15), bg = "#F6E96B").place(x=520, y=410, width=205)

        btn_save = Button(self.root, text="Save", command=self.save, font=("goudy old style", 15, "bold"), cursor="hand2",bg = "blue", fg = "white", bd = 1, relief= RIDGE).place(x=500, y=455, width=110, height=28)
        btn_update = Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"), cursor="hand2",bg = "green", fg = "white", bd = 1, relief= RIDGE).place(x=630, y=455, width=110, height=28)
        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), cursor="hand2",bg = "red", fg = "white", bd = 1, relief= RIDGE).place(x=760, y=455, width=110, height=28)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), cursor="hand2",bg = "gray", fg = "white", bd = 1, relief= RIDGE).place(x=890, y=455, width=110, height=28)

        emp_frame = Frame(self.root, bd = 2, relief=RIDGE, bg="#FAEDCE")
        emp_frame.place(x=0, y=495, relwidth=1, height=100)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("ID", "Gender", "Contact","Name", "DateofBirth", "DateofJoining", "Email", "Password", "UserType", "Address", "Salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("ID", text="Employee ID")
        self.EmployeeTable.heading("Gender", text="Gender")
        self.EmployeeTable.heading("Contact", text="Contact")
        self.EmployeeTable.heading("Name", text="Name")
        self.EmployeeTable.heading("DateofBirth", text="Date of Birth")
        self.EmployeeTable.heading("DateofJoining", text="Date of Joining")
        self.EmployeeTable.heading("Email", text="Email")
        self.EmployeeTable.heading("Password", text="Password")
        self.EmployeeTable.heading("UserType", text="User")
        self.EmployeeTable.heading("Address", text="Address")
        self.EmployeeTable.heading("Salary", text="Salary")

        self.EmployeeTable["show"] = "headings"

        self.EmployeeTable.column("ID", width=100)
        self.EmployeeTable.column("Gender", width=100)
        self.EmployeeTable.column("Contact", width=100)
        self.EmployeeTable.column("Name", width=100)
        self.EmployeeTable.column("DateofBirth", width=100)
        self.EmployeeTable.column("DateofJoining", width=100)
        self.EmployeeTable.column("Email", width=100)
        self.EmployeeTable.column("Password", width=100)
        self.EmployeeTable.column("UserType", width=100)
        self.EmployeeTable.column("Address", width=100)
        self.EmployeeTable.column("Salary", width=100)

        self.EmployeeTable.pack(fill=BOTH, expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def get_data(self, ev):
        f = self.EmployeeTable.focus()
        content = (self.EmployeeTable.item(f))
        row = content['values']

        self.var_emp_id.set(row[0]),
        self.var_emp_gender.set(row[1]),
        self.var_emp_contact.set(row[2]),
        self.var_emp_name.set(row[3]),
        self.var_emp_dob.set(row[4]),
        self.var_emp_doj.set(row[5]),
        self.var_emp_email.set(row[6]),
        self.var_emp_pass.set(row[7]),
        self.var_emp_utype.set(row[8]),
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[9]),
        self.var_emp_salary.set(row[10]),


    def save(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()

        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Employee ID must be required", parent = self.root)

            else :
                cur.execute("Select * from Employee where ID=?", (self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error", "This Employee ID is already assigned, try diffirect one.", parent = self.root)
                else :
                    cur.execute("Insert into Employee(ID ,  Gender ,  Contact , Name ,  DateofBirth ,  DateofJoining ,  Email ,  Password ,  UserType ,  Address ,  Salary) values(?,?,?,?,?,?,?,?,?,?,?)", (
                        self.var_emp_id.get(),
                        self.var_emp_gender.get(),
                        self.var_emp_contact.get(),
                        self.var_emp_name.get(),
                        self.var_emp_dob.get(),
                        self.var_emp_doj.get(),
                        self.var_emp_email.get(),
                        self.var_emp_pass.get(),
                        self.var_emp_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_emp_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee added successfully", parent = self.root)
                    self.show()

        except Exception as ex :
            messagebox.showerror("Eorror", f"Error due to : {str(ex)}", parent = self.root)


    def show(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()

        try:
            cur.execute("Select * from Employee")
            rows = cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)

        except Exception as ex :
            messagebox.showerror("Eorror", f"Error due to : {str(ex)}", parent = self.root)


    def update(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()

        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Employee ID must be required", parent = self.root)

            else :
                cur.execute("Select * from Employee where ID=?", (self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalid Employee ID.", parent = self.root)
                else :
                    cur.execute("Update Employee set   Gender =?,  Contact =?, Name =?,  DateofBirth =?,  DateofJoining =?,  Email =?,  Password =?,  UserType =?,  Address =?,  Salary =? where ID =?", (
                        self.var_emp_gender.get(),
                        self.var_emp_contact.get(),
                        self.var_emp_name.get(),
                        self.var_emp_dob.get(),
                        self.var_emp_doj.get(),
                        self.var_emp_email.get(),
                        self.var_emp_pass.get(),
                        self.var_emp_utype.get(),
                        self.txt_address.get('1.0', END),
                        self.var_emp_salary.get(),
                        self.var_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Employee updated successfully", 
                    parent = self.root)
                    self.show()

        except Exception as ex :
            messagebox.showerror("Eorror", f"Error due to : {str(ex)}", parent = self.root)


    def delete(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()
        try :
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error", "Employee ID must be required", parent = self.root)

            else :
                cur.execute("Select * from Employee where ID=?", (self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error", "Invalid Employee ID.", parent = self.root)
                else :
                    op = messagebox.askyesno("Confirm", "Do you want to delete?", parent = self.root)
                    if op == True:
                        cur.execute("delete from Employee where ID=?", (self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Employee deleted successfully", parent = self.root)
                        self.clear()
        except Exception as ex :
            messagebox.showerror("Eorror", f"Error due to : {str(ex)}", parent = self.root)

    def clear(self) :
        self.var_emp_id.set(""),
        self.var_emp_gender.set("Select"),
        self.var_emp_contact.set(""),
        self.var_emp_name.set(""),
        self.var_emp_dob.set(""),
        self.var_emp_doj.set(""),
        self.var_emp_email.set(""),
        self.var_emp_pass.set(""),
        self.var_emp_utype.set("Select"),
        self.txt_address.delete('1.0', END)
        self.var_emp_salary.set(""),
        self.var_searchby.set("Select"),
        self.var_searchtxt.set(""),
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()

        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select a valid search option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should not be empty", parent=self.root)
            else:
                cur.execute(f"SELECT * FROM Employee WHERE {self.var_searchby.get()} LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:self.EmployeeTable.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

# root = Tk()
# employee = employeeClass(root)
# root.mainloop()