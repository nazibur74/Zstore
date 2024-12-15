from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1040x590+340+200")
        self.root.title("Sales Management")
        self.root.config(bg="skyblue")
        self.root.focus_force()

        # Ensure bills directory exists
        self.bill_directory = 'bills'
        if not os.path.exists(self.bill_directory):
            os.makedirs(self.bill_directory)

        # Variables
        self.var_searchtxt = StringVar()
        self.var_product_id = StringVar()
        self.var_product_name = StringVar()
        self.var_qty = StringVar()
        self.var_price = StringVar()
        self.var_sale_qty = StringVar()
        self.var_customer_name = StringVar()
        self.var_customer_contact = StringVar()
        self.selected_products = []

        # Title
        title = Label(self.root, text="Sales Details", font=("goudy old style", 20), bg="#180161", fg="white")
        title.place(x=10, y=10, width=1020)

        # Search Frame
        searchFrame = LabelFrame(self.root, text="Search Product", font=("goudy old style", 12, "bold"), bd=1,relief=RIDGE, bg="white", fg="black")
        searchFrame.place(x=10, y=50, height=70, width=1020)

        lbl_search = Label(searchFrame, text="Search by Product ID/Name", bg='white', font=("goudy old style", 15))
        lbl_search.place(x=10, y=10)

        txt_search = Entry(searchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightgray")
        txt_search.place(x=250, y=10, width=460)

        btn_search = Button(searchFrame, text="Search", command=self.search, font=("goudy old style", 15, "bold"),cursor="hand2", bg="#059212", fg="white", bd=1, relief=RIDGE)
        btn_search.place(x=720, y=9, width=120, height=30)

        # Customer Info Labels and Entries
        lbl_customer_name = Label(self.root, text="Customer Name", font=("goudy old style", 15, "bold"), bg="skyblue",fg="#180161")
        lbl_customer_name.place(x=10, y=130)

        txt_customer_name = Entry(self.root, textvariable=self.var_customer_name, font=("goudy old style", 15),bg="#F6E96B")
        txt_customer_name.place(x=150, y=130, width=220)

        lbl_customer_contact = Label(self.root, text="Contact No.", font=("goudy old style", 15, "bold"), bg="skyblue",fg="#180161")
        lbl_customer_contact.place(x=10, y=180)

        txt_customer_contact = Entry(self.root, textvariable=self.var_customer_contact, font=("goudy old style", 15),bg="#F6E96B")
        txt_customer_contact.place(x=150, y=180, width=220)

        # Product Info Labels and Entries
        lbl_product_id = Label(self.root, text="Product ID", font=("goudy old style", 15, "bold"), bg="skyblue",fg="#180161")
        lbl_product_id.place(x=10, y=230)

        txt_product_id = Entry(self.root, textvariable=self.var_product_id, font=("goudy old style", 15), bg="#F6E96B",state='readonly')
        txt_product_id.place(x=150, y=230, width=220)

        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_name.place(x=10, y=280)

        txt_name = Entry(self.root, textvariable=self.var_product_name, font=("goudy old style", 15), bg="#F6E96B", state='readonly')
        txt_name.place(x=150, y=280, width=220)

        lbl_price = Label(self.root, text="Price", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_price.place(x=10, y=330)

        txt_price = Entry(self.root, textvariable=self.var_price, font=("goudy old style", 15), bg="#F6E96B", state='readonly')
        txt_price.place(x=150, y=330, width=220)

        lbl_qty = Label(self.root, text="Available Qty", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_qty.place(x=10, y=380)

        txt_qty = Entry(self.root, textvariable=self.var_qty, font=("goudy old style", 15), bg="#F6E96B", state='readonly')
        txt_qty.place(x=150, y=380, width=220)

        lbl_sale_qty = Label(self.root, text="Sale Qty", font=("goudy old style", 15, "bold"), bg="skyblue", fg="#180161")
        lbl_sale_qty.place(x=10, y=430)

        txt_sale_qty = Entry(self.root, textvariable=self.var_sale_qty, font=("goudy old style", 15), bg="#F6E96B")
        txt_sale_qty.place(x=150, y=430, width=220)

        # Buttons
        btn_add_to_cart = Button(self.root, text="Add to Cart", command=self.add_to_cart,
        font=("goudy old style", 15, "bold"), cursor="hand2", bg="green", fg="white", bd=1,
         relief=RIDGE)
        btn_add_to_cart.place(x=10, y=480, width=160, height=28)

        btn_generate_bill = Button(self.root, text="Generate Bill", command=self.generate_bill,
        font=("goudy old style", 15, "bold"), cursor="hand2", bg="blue", fg="white", bd=1,
           relief=RIDGE)
        btn_generate_bill.place(x=190, y=480, width=160, height=28)

        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15), cursor="hand2",
        bg="gray", fg="white", bd=1, relief=RIDGE)
        btn_clear.place(x=370, y=480, width=160, height=28)

        # Product Table Frame
        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg="#FAEDCE")
        product_frame.place(x=400, y=130, width=600, height=330)

        scrolly = Scrollbar(product_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(product_frame, columns=("ID", "Name", "Price", "Qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        self.ProductTable.heading("ID", text="Product ID")
        self.ProductTable.heading("Name", text="Name")
        self.ProductTable.heading("Price", text="Price")
        self.ProductTable.heading("Qty", text="Available Quantity")
        self.ProductTable["show"] = "headings"
        self.ProductTable.column("ID", width=100)
        self.ProductTable.column("Name", width=150)
        self.ProductTable.column("Price", width=120)
        self.ProductTable.column("Qty", width=100)
        self.ProductTable.pack(fill=BOTH, expand=1)
        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # Show Products
    def show(self):
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT id, name, price, qty FROM product")
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Add to Cart
    def add_to_cart(self):
        product_id = self.var_product_id.get()
        product_name = self.var_product_name.get()
        price = self.var_price.get()
        sale_qty = self.var_sale_qty.get()
        available_qty = self.var_qty.get()

        if product_id == "" or product_name == "" or price == "" or sale_qty == "":
            messagebox.showerror("Error", "Please select product and enter sale quantity", parent=self.root)
        elif int(sale_qty) > int(available_qty):
            messagebox.showerror("Error", "Invalid Sale Quantity", parent=self.root)
        else:
            total_price = float(price) * int(sale_qty)
            self.selected_products.append((product_id, product_name, price, sale_qty, total_price))
            messagebox.showinfo("Added", f"{product_name} added to cart", parent=self.root)

    # Get Data for Selected Product
    def get_data(self, event):
        selected_item = self.ProductTable.focus()
        item_data = self.ProductTable.item(selected_item)
        product_details = item_data['values']

        self.var_product_id.set(product_details[0])
        self.var_product_name.set(product_details[1])
        self.var_price.set(product_details[2])
        self.var_qty.set(product_details[3])

    # Search Product
    def search(self):
        search_text = self.var_searchtxt.get()
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT id, name, price, qty FROM product WHERE id LIKE ? OR name LIKE ?",
                        (f'%{search_text}%', f'%{search_text}%'))
            rows = cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Clear Fields
    def clear(self):
        self.var_searchtxt.set("")
        self.var_product_id.set("")
        self.var_product_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_sale_qty.set("")
        self.var_customer_name.set("")
        self.var_customer_contact.set("")
        self.selected_products.clear()

    # Generate Bill
    def generate_bill(self):
        customer_name = self.var_customer_name.get()
        customer_contact = self.var_customer_contact.get()

        if not customer_name or not customer_contact:
            messagebox.showerror("Error", "Please enter customer name and contact", parent=self.root)
            return

        if not self.selected_products:
            messagebox.showerror("Error", "No products in cart to generate bill", parent=self.root)
            return

        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        bill_text = f"{current_datetime}\n"
        bill_text += f"Customer Name: {customer_name}\nContact: {customer_contact}\n"
        bill_text += f"{'ID':<15}{'Name':<30}{'Qty':<10}{'Price':<10}{'Total':<10}\n"
        bill_text += "-" * 70 + "\n"

        total_amount = 0
        con = sqlite3.connect('zstore.db')
        cur = con.cursor()

        for product in self.selected_products:
            product_id, name, price, qty, total_price = product
            bill_text += f"{product_id:<10}{name:<30}{qty:<10}{price:<10}{total_price:<10}\n"
            total_amount += total_price

            # Deduct the sold quantity from the database
            cur.execute("SELECT qty FROM product WHERE id = ?", (product_id,))
            result = cur.fetchone()
            if result:
                available_qty = result[0]
                new_qty = available_qty - int(qty)
                cur.execute("UPDATE product SET qty = ? WHERE id = ?", (new_qty, product_id))

            # Insert the sale into the sales table
            sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cur.execute(
                "INSERT INTO sales (customer_name, customer_contact, product_id, product_name, quantity, price, total, sale_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (customer_name, customer_contact, product_id, name, int(qty), float(price), total_price, sale_date)
            )

        con.commit()
        con.close()

        bill_text += "-" * 70 + "\n"
        bill_text += f"{'Total Amount':<65}{total_amount:<10}\n"

        # Save bill to file
        self.save_bill_to_file(customer_name, bill_text)

        # Clear cart after bill generation
        self.selected_products.clear()


    # Save Bill to File
    def save_bill_to_file(self, customer_name, bill_text):
        filename = f"{customer_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_bill.pdf"
        bill_path = os.path.join(self.bill_directory, filename)

        # Temporarily hide the main window
        self.root.withdraw()

        try:
            # Create a PDF file
            c = canvas.Canvas(bill_path, pagesize=letter)
            width, height = letter

            # Add a title and the bill content
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, height - 50, f"Zstore")
            c.setFont("Helvetica", 12)

            # Add the bill content
            text_object = c.beginText(100, height - 100)
            text_object.setFont("Helvetica", 12)

            # Break the bill text into lines and add it to the PDF
            for line in bill_text.splitlines():
                text_object.textLine(line)
            c.drawText(text_object)

            # Finalize the PDF file
            c.save()

            messagebox.showinfo("Bill Saved", f"Bill saved successfully{bill_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {str(e)}")
        finally:
            self.root.deiconify()  # Show the main window again
    
# root = Tk()
# window = salesClass(root)
# root.mainloop()