import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass

class dashboardClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+30+100")
        self.root.title("Zstore")
        self.root.config(bg="white")

        # Title and Logout Button
        title = Label(self.root, text="Zstore", font=("times new roman", 40, "bold"), bg="skyblue", fg="#211C6A", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)
        btn_logout = Button(self.root, text="Log out", font=("arial", 13, "bold"), command=self.logout, cursor="hand2").place(x=1210, y=20, height=28, width=100)

        # Left Menu Section
        self.menuLogo = Image.open("Images/Menu1.png").resize((200, 200), Image.LANCZOS)
        self.menuLogo = ImageTk.PhotoImage(self.menuLogo)

        leftMenu = Frame(self.root, relief=RIDGE, bg="#A3FFD6")
        leftMenu.place(x=10, y=80, height=610, width=300)

        lbl_menuLogo = Label(leftMenu, image=self.menuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        self.icon_side = PhotoImage(file="Images/MenuLogo1.png")
        lbl_menu = Label(leftMenu, text="Menu", font=("arial", 27), bg="white", fg="#180161").pack(side=TOP, fill=X)

        # Buttons
        btn_employee = Button(leftMenu, text="Employee", command=self.employee, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 25, "bold"), bg="skyblue", fg="#180161", bd=1, cursor="hand2").pack(side=TOP, fill=X)
        btn_supplier = Button(leftMenu, text="Supplier", command=self.supplier, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 25, "bold"), bg="skyblue", fg="#180161", bd=1, cursor="hand2").pack(side=TOP, fill=X)
        btn_category = Button(leftMenu, text="Category", command=self.category, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 25, "bold"), bg="skyblue", fg="#180161", bd=1, cursor="hand2").pack(side=TOP, fill=X)
        btn_product = Button(leftMenu, text="Product", command=self.product, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 25, "bold"), bg="skyblue", fg="#180161", bd=1, cursor="hand2").pack(side=TOP, fill=X)
        btn_sales = Button(leftMenu, text="Sales", command=self.sales, image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 25, "bold"), bg="skyblue", fg="#180161", bd=1, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(leftMenu, text="Exit", image=self.icon_side, compound=LEFT, padx=5, anchor="w", font=("times new roman", 25, "bold"), bg="skyblue", fg="#180161", bd=1, cursor="hand2").pack(side=TOP, fill=X)

        # Dashboard Information Icons
        self.icon_employee = PhotoImage(file="Images/EmployeeIcon.png")
        self.icon_supplier = PhotoImage(file="Images/SupplierIcon.png")
        self.icon_category = PhotoImage(file="Images/CategoryIcon.png")
        self.icon_product = PhotoImage(file="Images/ProductsIcon.png")
        self.icon_sales = PhotoImage(file="Images/SalesIcon.png")

        # Dashboard Information Labels
        self.lbl_employee = Label(self.root, text="Total Employee\n[ 0 ]", image=self.icon_employee, compound=TOP, font=("goudy old style", 20, "bold"), bd=1, relief=RIDGE, bg="#EFF396", fg="#180161")
        self.lbl_employee.place(x=340, y=120, width=300, height=150)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[ 0 ]", image=self.icon_supplier, compound=TOP, font=("goudy old style", 20, "bold"), bd=1, relief=RIDGE, bg="#EFF396", fg="#180161")
        self.lbl_supplier.place(x=670, y=120, width=300, height=150)

        self.lbl_category = Label(self.root, text="Total Category\n[ 0 ]", image=self.icon_category, compound=TOP, font=("goudy old style", 20, "bold"), bd=1, relief=RIDGE, bg="#EFF396", fg="#180161")
        self.lbl_category.place(x=1000, y=120, width=300, height=150)

        self.lbl_product = Label(self.root, text="Total Products\n[ 0 ]", image=self.icon_product, compound=TOP, font=("goudy old style", 20, "bold"), bd=1, relief=RIDGE, bg="#EFF396", fg="#180161")
        self.lbl_product.place(x=340, y=300, width=300, height=150)

        self.lbl_sales = Label(self.root, text="Total Sales\n[ 0 ]", image=self.icon_sales, compound=TOP, font=("goudy old style", 20, "bold"), bd=1, relief=RIDGE, bg="#EFF396", fg="#180161")
        self.lbl_sales.place(x=670, y=300, width=300, height=150)

        # Footer
        lbl_footer = Label(self.root, text="YAGAMI | 74234", anchor="e", font=("times new roman", 12), bg="white", fg="#180161").place(x=1230, y=680)

        # Update Content
        self.update_content()

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def logout(self):
        self.root.destroy()

    def update_content(self):
        con = sqlite3.connect(database='zstore.db')
        cur = con.cursor()
        try:
            # Fetch and update each label
            cur.execute('SELECT COUNT(*) FROM Employee')
            employee_count = cur.fetchone()[0]
            self.lbl_employee.config(text=f'Total Employee\n[ {employee_count} ]')

            cur.execute('SELECT COUNT(*) FROM Supplier')
            supplier_count = cur.fetchone()[0]
            self.lbl_supplier.config(text=f'Total Supplier\n[ {supplier_count} ]')

            cur.execute('SELECT COUNT(*) FROM category')
            category_count = cur.fetchone()[0]
            self.lbl_category.config(text=f'Total Category\n[ {category_count} ]')

            cur.execute('SELECT COUNT(*) FROM product')
            product_count = cur.fetchone()[0]
            self.lbl_product.config(text=f'Total Products\n[ {product_count} ]')

            cur.execute('SELECT COUNT(*) FROM sales')
            sales_count = cur.fetchone()[0]
            self.lbl_sales.config(text=f'Total Sales\n[ {sales_count} ]')

        except sqlite3.Error as ex:
            messagebox.showerror('Error', f'Error due to {str(ex)}', parent=self.root)
        finally:
            con.close()

# root = Tk()
# dashboard = dashboardClass(root)
# root.mainloop()