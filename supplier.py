from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1040x590+340+200")
        self.root.title("Supplier")
        self.root.config(bg="skyblue")
        self.root.focus_force()

        # Variables
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_emp_name = StringVar()
        self.var_sup_contact = StringVar()

        # Title
        title = Label(self.root, text="Supplier Details", font=("goudy old style", 20), bg="#180161", fg="white")
        title.place(x=10, y=10, width=1020)

        # Search Frame (Extended Width)
        searchFrame = LabelFrame(self.root, text="Search Supplier", font=("goudy old style", 12, "bold"), bd=1, relief=RIDGE, bg="white", fg="black")
        searchFrame.place(x=10, y=50, height=70, width=1020)

        lbl_search = Label(searchFrame, text="Search by Invoice No.", bg='white', font=("goudy old style", 15))
        lbl_search.place(x=10, y=10)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightgray")
        txt_search.place(x=200, y=10, width=460)

        btn_search = Button(searchFrame, text="Search", command=self.search, font=("goudy old style", 15, "bold"), cursor="hand2", bg="#059212", fg="white", bd=1, relief=RIDGE)
        btn_search.place(x=670, y=9, width=120, height=30)

        # Supplier Info Labels and Entries
        lbl_sup_invoice = Label(self.root, text="Invoice No.", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_sup_invoice.place(x=10, y=130)

        txt_sup_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("goudy old style", 15), bg="#F6E96B")
        txt_sup_invoice.place(x=130, y=130, width=220)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 14, "bold"), bg="skyblue", fg="#180161")
        lbl_name.place(x=10, y=180)

        txt_name = Entry(self.root, textvariable=self.var_emp_name, font=("goudy old style", 15), bg="#F6E96B")
        txt_name.place(x=130, y=180, width=220)

        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_contact.place(x=10, y=230)

        txt_contact = Entry(self.root, textvariable=self.var_sup_contact, font=("goudy old style", 15), bg="#F6E96B")
        txt_contact.place(x=130, y=230, width=220)

        # Description on the Right Side with Larger Area
        lbl_des = Label(self.root, text="Description", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_des.place(x=380, y=130)

        self.txt_des = Text(self.root, font=("goudy old style", 15), bg="#F6E96B")
        self.txt_des.place(x=500, y=130, width=520, height=200)

        # Buttons on the Left Side (Moved Down)
        btn_save = Button(self.root, text="Save", command=self.save, font=("goudy old style", 15, "bold"), cursor="hand2", bg="blue", fg="white", bd=1, relief=RIDGE)
        btn_save.place(x=10, y=340, width=110, height=28)  # Changed Y to 340

        btn_update = Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"), cursor="hand2", bg="green", fg="white", bd=1, relief=RIDGE)
        btn_update.place(x=130, y=340, width=110, height=28)  # Changed Y to 340

        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), cursor="hand2", bg="red", fg="white", bd=1, relief=RIDGE)
        btn_delete.place(x=250, y=340, width=110, height=28)  # Changed Y to 340

        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), cursor="hand2", bg="gray", fg="white", bd=1, relief=RIDGE)
        btn_clear.place(x=370, y=340, width=110, height=28)  # Changed Y to 340

        # Supplier Table Frame
        emp_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#FAEDCE")
        emp_frame.place(x=10, y=390, width=1020, height=180)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.SupplierTable = ttk.Treeview(emp_frame, columns=("Invoice", "Name", "Contact", "Description"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)

        self.SupplierTable.heading("Invoice", text="Invoice")
        self.SupplierTable.heading("Name", text="Name")
        self.SupplierTable.heading("Contact", text="Contact")
        self.SupplierTable.heading("Description", text="Description")
        self.SupplierTable["show"] = "headings"
        self.SupplierTable.column("Invoice", width=100)
        self.SupplierTable.column("Name", width=100)
        self.SupplierTable.column("Contact", width=100)
        self.SupplierTable.column("Description", width=100)
        self.SupplierTable.pack(fill=BOTH, expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def save(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("Select * from Supplier where Invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Invoice No. is already assigned, try a different one.", parent=self.root)
                else:
                    cur.execute("Insert into Supplier(Invoice, Name, Contact, Description) values(?,?,?,?)", (
                        self.var_sup_invoice.get(),
                        self.var_emp_name.get(),
                        self.var_sup_contact.get(),
                        self.txt_des.get('1.0', END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()
        try:
            cur.execute("Select * from Supplier")
            rows = cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.SupplierTable.focus()
        content = (self.SupplierTable.item(f))
        row = content['values']
        self.var_sup_invoice.set(row[0])
        self.var_emp_name.set(row[1])
        self.var_sup_contact.set(row[2])
        self.txt_des.delete('1.0', END)
        self.txt_des.insert(END, row[3])

    def update(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("Select * from Supplier where Invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("Update Supplier set Name = ?, Contact = ?, Description = ? where Invoice = ?", (
                        self.var_emp_name.get(),
                        self.var_sup_contact.get(),
                        self.txt_des.get('1.0', END),
                        self.var_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier updated successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()
        try:
            if self.var_sup_invoice.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cur.execute("Select * from Supplier where Invoice=?", (self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)
                else:
                    cur.execute("Delete from Supplier where Invoice=?", (self.var_sup_invoice.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Supplier deleted successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_invoice.set("")
        self.var_emp_name.set("")
        self.var_sup_contact.set("")
        self.txt_des.delete('1.0', END)
        self.show()

    def search(self):
        con = sqlite3.connect(database=r'zstore.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("Select * from Supplier where Invoice=?", (self.var_searchtxt.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

# root = Tk()
# window = supplierClass(root)
# root.mainloop()