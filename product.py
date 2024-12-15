from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1040x590+340+200")
        self.root.title("Product")
        self.root.config(bg="skyblue")
        self.root.focus_force()

        # Variables
        self.var_searchtxt = StringVar()
        self.var_product_id = StringVar()
        self.var_product_name = StringVar()
        self.var_category = StringVar()
        self.var_supplier = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()

        # Title
        title = Label(self.root, text="Product Details", font=("goudy old style", 20), bg="#180161", fg="white")
        title.place(x=10, y=10, width=1020)

        # Search Frame
        searchFrame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 12, "bold"), bd=1, relief=RIDGE, bg="white", fg="black")
        searchFrame.place(x=10, y=50, height=70, width=1020)

        lbl_search = Label(searchFrame, text="Search by Product ID/Name", bg='white', font=("goudy old style", 15))
        lbl_search.place(x=10, y=10)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightgray")
        txt_search.place(x=250, y=10, width=460)

        btn_search = Button(searchFrame, text="Search", command=self.search, font=("goudy old style", 15, "bold"), cursor="hand2", bg="#059212", fg="white", bd=1, relief=RIDGE)
        btn_search.place(x=720, y=9, width=120, height=30)

        # Product Info Labels and Entries
        lbl_product_id = Label(self.root, text="Product ID", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_product_id.place(x=10, y=130)

        txt_product_id = Entry(self.root, textvariable=self.var_product_id, font=("goudy old style", 15), bg="#F6E96B")
        txt_product_id.place(x=130, y=130, width=220)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_name.place(x=10, y=180)

        txt_name = Entry(self.root, textvariable=self.var_product_name, font=("goudy old style", 15), bg="#F6E96B")
        txt_name.place(x=130, y=180, width=220)

        lbl_category = Label(self.root, text="Category", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_category.place(x=10, y=230)

        # Store the category combo box as an instance variable
        self.cmb_category = ttk.Combobox(self.root, textvariable=self.var_category, font=("goudy old style", 15), state="readonly", justify=CENTER)
        self.cmb_category.place(x=130, y=230, width=220)
        self.fetch_category()  # Fetch categories from DB

        lbl_supplier = Label(self.root, text="Supplier", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_supplier.place(x=10, y=280)

        # Store the supplier combo box as an instance variable
        self.cmb_supplier = ttk.Combobox(self.root, textvariable=self.var_supplier, font=("goudy old style", 15), state="readonly", justify=CENTER)
        self.cmb_supplier.place(x=130, y=280, width=220)
        self.fetch_supplier()  # Fetch suppliers from DB

        lbl_price = Label(self.root, text="Price", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_price.place(x=10, y=330)

        txt_price = Entry(self.root, textvariable=self.var_price, font=("goudy old style", 15), bg="#F6E96B")
        txt_price.place(x=130, y=330, width=220)

        lbl_qty = Label(self.root, text="Quantity", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_qty.place(x=10, y=380)

        txt_qty = Entry(self.root, textvariable=self.var_qty, font=("goudy old style", 15), bg="#F6E96B")
        txt_qty.place(x=130, y=380, width=220)

        # Buttons
        btn_save = Button(self.root, text="Save", command=self.save, font=("goudy old style", 15, "bold"), cursor="hand2", bg="blue", fg="white", bd=1, relief=RIDGE)
        btn_save.place(x=10, y=430, width=160, height=28)

        btn_update = Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"), cursor="hand2", bg="green", fg="white", bd=1, relief=RIDGE)
        btn_update.place(x=190, y=430, width=160, height=28)

        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), cursor="hand2", bg="red", fg="white", bd=1, relief=RIDGE)
        btn_delete.place(x=10, y=470, width=160, height=28)

        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), cursor="hand2", bg="gray", fg="white", bd=1, relief=RIDGE)
        btn_clear.place(x=190, y=470, width=160, height=28)

        # Product Table Frame
        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#FAEDCE")
        product_frame.place(x=370, y=130, width=650, height=350)

        scrolly = Scrollbar(product_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(product_frame, columns=("ID", "Name", "Category", "Supplier", "Price", "Qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("ID", text="Product ID")
        self.ProductTable.heading("Name", text="Name")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("Supplier", text="Supplier")
        self.ProductTable.heading("Price", text="Price")
        self.ProductTable.heading("Qty", text="Quantity")
        self.ProductTable["show"] = "headings"
        self.ProductTable.column("ID", width=100)
        self.ProductTable.column("Name", width=150)
        self.ProductTable.column("Category", width=120)
        self.ProductTable.column("Supplier", width=120)
        self.ProductTable.column("Price", width=100)
        self.ProductTable.column("Qty", width=100)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # Fetch Category data from DB
    def fetch_category(self):
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        cur.execute("SELECT name FROM category")
        rows = cur.fetchall()
        categories = [row[0] for row in rows]
        self.var_category.set("Select")
        self.cmb_category['values'] = categories  # Correctly reference instance variable

    # Fetch Supplier data from DB
    def fetch_supplier(self):
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        cur.execute("SELECT Name FROM supplier")
        rows = cur.fetchall()
        suppliers = [row[0] for row in rows]
        self.var_supplier.set("Select")
        self.cmb_supplier['values'] = suppliers  # Correctly reference instance variable

    # Save Product
    def save(self):
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        try:
            if self.var_product_id.get() == "":
                messagebox.showerror("Error", "Product ID must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE id=?", (self.var_product_id.get(),))
                row = cur.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Product ID already exists", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO product (id, name, category, supplier, price, qty) VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            self.var_product_id.get(),
                            self.var_product_name.get(),
                            self.var_category.get(),
                            self.var_supplier.get(),
                            self.var_price.get(),
                            self.var_qty.get()
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Fetch Data
    def show(self):
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Get Data
    def get_data(self, ev):
        f = self.ProductTable.focus()
        content = (self.ProductTable.item(f))
        row = content['values']
        self.var_product_id.set(row[0])
        self.var_product_name.set(row[1])
        self.var_category.set(row[2])
        self.var_supplier.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])

    # Update Product
    def update(self):
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        try:
            if self.var_product_id.get() == "":
                messagebox.showerror("Error", "Product ID is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE id=?", (self.var_product_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                else:
                    cur.execute("UPDATE product SET name=?, category=?, supplier=?, price=?, qty=? WHERE id=?",
                                (
                                    self.var_product_name.get(),
                                    self.var_category.get(),
                                    self.var_supplier.get(),
                                    self.var_price.get(),
                                    self.var_qty.get(),
                                    self.var_product_id.get()
                                ))
                    con.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Delete Product
    def delete(self):
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        try:
            if self.var_product_id.get() == "":
                messagebox.showerror("Error", "Product ID is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE id=?", (self.var_product_id.get(),))
                row = cur.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Product ID", parent=self.root)
                else:
                    cur.execute("DELETE FROM product WHERE id=?", (self.var_product_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Product Deleted Successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Clear Data
    def clear(self):
        self.var_product_id.set("")
        self.var_product_name.set("")
        self.var_category.set("Select")
        self.var_supplier.set("Select")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_searchtxt.set("")
        self.show()

    # Search Function
    def search(self):
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM product WHERE name LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

# root = Tk()
# window = productClass(root)
# root.mainloop()