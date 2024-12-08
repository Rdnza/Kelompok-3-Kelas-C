# main.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from auth import current_user, login, register, logout
from bmi import calculate_bmi
from database import load_users_database, load_history_database

# Set up the main window
root = tk.Tk()
root.title("BMI and Healthcare")
root.geometry("600x600")

# Frame for Login
login_frame = ttk.Frame(root)
# Frame for BMI Calculator
bmi_calculator_frame = ttk.Frame(root)

# Define variables for inputs
username_var = tk.StringVar()
password_var = tk.StringVar()
weight_var = tk.StringVar()
height_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar(value="male")
activity_var = tk.StringVar(value="low")

# Load background image
import os
current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "background.jpeg")

# Function to set background for both frames
def set_background(frame):
    try:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        background_label = tk.Label(frame, image=photo)
        background_label.photo = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error: {e}")

# Set background for the login frame
set_background(login_frame)

# Login Form Widgets
ttk.Label(login_frame, text="Username:", font=('Helvetica-Bold', 12)).place(x=100, y=50)
ttk.Entry(login_frame, textvariable=username_var).place(x=200, y=50, width=200)
ttk.Label(login_frame, text="Password:", font=('Helvetica-Bold', 12)).place(x=100, y=100)
ttk.Entry(login_frame, textvariable=password_var, show="*").place(x=200, y=100, width=200)
ttk.Button(login_frame, text="Login", command=lambda: login(username_var, password_var, login_frame, bmi_calculator_frame)).place(x=150, y=200, width=100)
ttk.Button(login_frame, text="Register", command=lambda: register(username_var, password_var)).place(x=300, y=200, width=100)

login_frame.pack(fill="both", expand=True)  # Display the login frame initially

# Set background for the bmi_calculator_frame
set_background(bmi_calculator_frame)

# BMI Calculation Form Widgets
ttk.Label(bmi_calculator_frame, text="Weight (kg):", font=('Helvetica-Bold', 12)).place(x=100, y=50)
ttk.Entry(bmi_calculator_frame, textvariable=weight_var).place(x=200, y=50, width=200)
ttk.Label(bmi_calculator_frame, text="Height (cm):", font=('Helvetica-Bold', 12)).place(x=100, y=100)
ttk.Entry(bmi_calculator_frame, textvariable=height_var).place(x=200, y=100, width=200)
ttk.Label(bmi_calculator_frame, text="Age:", font=('Helvetica-Bold', 12)).place(x=100, y=150)
ttk.Entry(bmi_calculator_frame, textvariable=age_var).place(x=200, y=150, width=200)
ttk.Label(bmi_calculator_frame, text="Gender:", font=('Helvetica-Bold', 12)).place(x=100, y=200)
ttk.Combobox(bmi_calculator_frame, textvariable=gender_var, values=["male", "female"], state="readonly").place(x=200, y=200, width=200)
ttk.Label(bmi_calculator_frame, text="Activity Level:", font=('Helvetica-Bold', 12)).place(x=100, y=250)
ttk.Combobox(bmi_calculator_frame, textvariable=activity_var, values=["low", "moderate", "high"], state="readonly").place(x=200, y=250, width=200)

ttk.Button(bmi_calculator_frame, text="Calculate BMI", command=lambda: calculate_bmi(weight_var, height_var, age_var, gender_var, activity_var, current_user)).place(x=150, y=350, width=100)
ttk.Button(bmi_calculator_frame, text="Logout", command=lambda: logout(bmi_calculator_frame, login_frame)).place(x=300, y=350, width=100)

root.mainloop()
