import json
from tkinter import messagebox
from database import load_users_database, save_users_database

current_user = None

def login(username, password):
    global current_user
    users_data = load_users_database()
    if username in users_data["users"] and users_data["users"][username] == password:
        current_user = username
        messagebox.showinfo("Success", "Login successful!")
        return True
    else:
        messagebox.showerror("Error", "Invalid username or password!")
        return False

def register(username, password):
    users_data = load_users_database()
    if username in users_data["users"]:
        messagebox.showerror("Error", "Username already exists!")
    else:
        users_data["users"][username] = password
        save_users_database(users_data)
        messagebox.showinfo("Success", "Registration successful!")

def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "You have successfully logged out!")
