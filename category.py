from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1040x590+340+200")
        self.root.title("Category")
        self.root.config(bg="skyblue")
        self.root.focus_force()

        # Define StringVar for holding category name
        self.var_cat_name = StringVar()

        # Set up UI elements
        self.setup_title()
        self.setup_fields()
        self.setup_buttons()
        self.setup_table()
        self.show_categories()

    def setup_title(self):
        title = Label(self.root, text="Product Category", font=("goudy old style", 20), bg="#180161", fg="white")
        title.place(x=50, y=20, width=950)

    def setup_fields(self):
        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 20, "bold"), bg="skyblue", fg="#180161")
        lbl_name.place(x=60, y=70)

        txt_name = Entry(self.root, textvariable=self.var_cat_name, font=("goudy old style", 15), bg="#F6E96B")
        txt_name.place(x=60, y=110, width=380)

    def setup_buttons(self):
        btn_add = Button(self.root, text="Add", command=self.add_category, font=("goudy old style", 15, "bold"), cursor="hand2", bg="green", fg="white", bd=1, relief=RIDGE)
        btn_add.place(x=60, y=150, width=180, height=28)

        btn_delete = Button(self.root, text="Delete", command=self.delete_category, font=("goudy old style", 15, "bold"), cursor="hand2", bg="red", fg="white", bd=1, relief=RIDGE)
        btn_delete.place(x=260, y=150, width=180, height=28)

    def setup_table(self):
        self.cat_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.cat_frame.place(x=500, y=80, width=500, height=400)

        self.scroll_x = Scrollbar(self.cat_frame, orient=HORIZONTAL)
        self.scroll_y = Scrollbar(self.cat_frame, orient=VERTICAL)

        self.category_table = ttk.Treeview(self.cat_frame, columns=("id", "name"), xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.category_table.heading("id", text="ID")
        self.category_table.heading("name", text="Category Name")
        self.category_table.column("id", width=70)
        self.category_table.column("name", width=100)
        self.category_table["show"] = "headings"

        self.scroll_x.pack(side=BOTTOM, fill=X)
        self.scroll_y.pack(side=RIGHT, fill=Y)
        self.scroll_x.config(command=self.category_table.xview)
        self.scroll_y.config(command=self.category_table.yview)

        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

    def add_category(self):
        if self.var_cat_name.get() == "":
            messagebox.showerror("Error", "Category Name is required!")
            self.root.focus_force()  # Ensure the window regains focus
            return

        conn = sqlite3.connect("zstore.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO category (name) VALUES (?)", (self.var_cat_name.get(),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Category added successfully!")
        self.root.focus_force()  # Ensure the window regains focus
        self.show_categories()
        self.clear_fields()

    def delete_category(self):
        if not self.var_cat_name.get():
            messagebox.showerror("Error", "Select a category to delete!")
            self.root.focus_force()  # Ensure the window regains focus
            return

        conn = sqlite3.connect("zstore.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM category WHERE name=?", (self.var_cat_name.get(),))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Category deleted successfully!")
        self.root.focus_force()  # Ensure the window regains focus
        self.show_categories()
        self.clear_fields()

    def clear_fields(self):
        self.var_cat_name.set("")

    def show_categories(self):
        conn = sqlite3.connect("zstore.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM category")
        rows = cursor.fetchall()
        self.category_table.delete(*self.category_table.get_children())
        for row in rows:
            self.category_table.insert("", END, values=row)
        conn.close()

    def get_data(self, event):
        selected_row = self.category_table.focus()
        data = self.category_table.item(selected_row)
        row_data = data['values']
        if row_data:
            self.var_cat_name.set(row_data[1])

# root = Tk()
# window = categoryClass(root)
# root.mainloop()