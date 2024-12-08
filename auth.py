# auth.py
import tkinter as tk
from tkinter import messagebox
from database import load_users_database, save_users_database

# Current logged-in user
current_user = None

def login(username_var, password_var, login_frame, bmi_calculator_frame):
    global current_user
    username = username_var.get()
    password = password_var.get()

    users_data = load_users_database()
    if username in users_data["users"] and users_data["users"][username] == password:
        current_user = username
        messagebox.showinfo("Success", "Login successful!")
        login_frame.pack_forget()  # Hide login frame
        bmi_calculator_frame.pack(fill="both", expand=True)  # Show BMI calculator frame
    else:
        messagebox.showerror("Error", "Invalid username or password!")

def register(username_var, password_var):
    username = username_var.get()
    password = password_var.get()

    users_data = load_users_database()
    if username in users_data["users"]:
        messagebox.showerror("Error", "Username already exists!")
    else:
        users_data["users"][username] = password
        save_users_database(users_data)
        messagebox.showinfo("Success", "Registration successful!")

def logout(bmi_calculator_frame, login_frame):
    global current_user
    current_user = None
    bmi_calculator_frame.pack_forget()  # Hide BMI calculator frame
    login_frame.pack(fill="both", expand=True)  # Show login frame
    messagebox.showinfo("Logout", "You have successfully logged out!")
