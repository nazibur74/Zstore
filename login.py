import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from dashboard import dashboardClass

class loginClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+100+100")
        self.root.title("Login to Zstore")
        self.root.config(bg="#f0f0f0")  # Light background color for a modern look

        # Frame for Login Form
        login_frame = Frame(self.root, bg="white", bd=0, relief=RIDGE)
        login_frame.place(x=450, y=100, width=450, height=500)

        # Fixed Logo
        self.logo_img = Image.open("Images/Logo1.png").resize((150, 150), Image.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = Label(login_frame, image=self.logo_img, bg="white")
        self.logo_label.pack(pady=20)

        # Email
        self.var_email = StringVar()
        lbl_email = Label(login_frame, text="Email", font=("Arial", 14, "bold"), bg="white", fg="#333333")
        lbl_email.pack(pady=5)
        self.txt_email = Entry(login_frame, textvariable=self.var_email, font=("Arial", 13), bg='#e8e8e8', relief=GROOVE, bd=0)
        self.txt_email.pack(pady=5, fill=X, padx=20, ipady=8)
        self.txt_email.config(highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#333333", borderwidth=0)

        # Password
        self.var_password = StringVar()
        lbl_password = Label(login_frame, text="Password", font=("Arial", 14, "bold"), bg="white", fg="#333333")
        lbl_password.pack(pady=5)
        self.txt_password = Entry(login_frame, textvariable=self.var_password, show='*', font=("Arial", 13), bg='#e8e8e8', relief=GROOVE, bd=0)
        self.txt_password.pack(pady=5, fill=X, padx=20, ipady=8)
        self.txt_password.config(highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#333333", borderwidth=0)

        # Password Visibility Toggle
        self.show_password = BooleanVar()
        self.show_password.set(False)
        chk_show_password = Checkbutton(login_frame, text="Show Password", variable=self.show_password, command=self.toggle_password, font=("Arial", 10), bg="white", cursor="hand2", fg="#333333", bd=0)
        chk_show_password.pack(pady=5)

        # Login Button
        btn_login = Button(login_frame, text="Login", command=self.login, font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", cursor="hand2", relief=GROOVE, bd=0)
        btn_login.pack(pady=20, fill=X, padx=80, ipady=10)
        btn_login.config(highlightthickness=1, highlightbackground="#4CAF50", borderwidth=0)

    def login(self):
        email = self.var_email.get()
        password = self.var_password.get()

        # Connect to the SQLite database and validate credentials
        try:
            con = sqlite3.connect("zstore.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM Employee WHERE Email=? AND Password=? AND UserType='Admin'", (email, password))
            row = cur.fetchone()

            if row:
                self.open_dashboard()
            else:
                messagebox.showerror("Login Error", "Invalid email or password!", parent=self.root)
            con.close()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def toggle_password(self):
        if self.show_password.get():
            self.txt_password.config(show="")
        else:
            self.txt_password.config(show="*")

    def open_dashboard(self):
        self.root.destroy()  # Close the login window
        root = Tk()  # Create a new root window for the dashboard
        self.new_obj = dashboardClass(root)
        root.mainloop()

if __name__ == "__main__":
    root = Tk()
    login_window = loginClass(root)
    root.mainloop()
