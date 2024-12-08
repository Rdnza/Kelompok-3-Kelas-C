import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import json
import os
from PIL import Image, ImageTk

# Database Files
USERS_DB_FILE = "users_data.json"
HISTORY_DB_FILE = "history_data.json"

# Current logged-in user
current_user = None

# Load or initialize the users database
def load_users_database():
    try:
        with open(USERS_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}}

def save_users_database(data):
    with open(USERS_DB_FILE, "w") as f:
        json.dump(data, f)

def load_history_database():
    try:
        with open(HISTORY_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"history": {}}

def save_history_database(data):
    with open(HISTORY_DB_FILE, "w") as f:
        json.dump(data, f)

def login():
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

def register():
    username = username_var.get()
    password = password_var.get()

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
    bmi_calculator_frame.pack_forget()  # Hide BMI calculator frame
    login_frame.pack(fill="both", expand=True)  # Show login frame
    
    # Reset all input fields
    weight_var.set("")
    height_var.set("")
    age_var.set("")
    gender_var.set("male")
    activity_var.set("low")

    messagebox.showinfo("Logout", "You have successfully logged out!")

def calculate_bmi():
    try:
        weight = float(weight_var.get())
        height = float(height_var.get()) / 100  # Convert to meters
        bmi = weight / (height ** 2)

        # Determine BMI status and calorie recommendations
        if bmi < 18.5:
            status = "Underweight"
            calorie_adjustment = 500
            exercise_recommendation = "Focus on strength training and resistance exercises."
            meal_plan = get_meal_plan("underweight")
        elif 18.5 <= bmi <= 24.9:
            status = "Normal"
            calorie_adjustment = 0
            exercise_recommendation = "Maintain a balanced routine with moderate cardio and strength training."
            meal_plan = get_meal_plan("normal")
        elif 25 <= bmi <= 29.9:
            status = "Overweight"
            calorie_adjustment = -500
            exercise_recommendation = "Focus on cardio exercises (running, cycling) to burn fat."
            meal_plan = get_meal_plan("overweight")
        else:
            status = "Obese"
            calorie_adjustment = -750
            exercise_recommendation = "Focus on intense cardio workouts (HIIT, running) and strength training."
            meal_plan = get_meal_plan("obese")

        calorie_needs = calculate_calories(calorie_adjustment)
        save_to_report(bmi, status, calorie_needs, exercise_recommendation, meal_plan)

        history_data = load_history_database()
        if current_user:
            if current_user not in history_data["history"]:
                history_data["history"][current_user] = []
            history_data["history"][current_user].append({"type": "BMI", "value": bmi, "status": status})
            save_history_database(history_data)

        messagebox.showinfo(
            "BMI Result",
            f"Your BMI: {bmi:.2f} ({status})\n\n"
            f"Calorie Needs: {calorie_needs} kcal/day\n"
            f"Exercise Recommendation: {exercise_recommendation}\n\n"
            f"Meal Plan:\n{meal_plan}"
        )
    except ValueError:
        messagebox.showerror("Error", "Please enter valid inputs!")

def calculate_calories(calorie_adjustment):
    try:
        weight = float(weight_var.get())
        height = float(height_var.get())
        age = int(age_var.get())
        gender = gender_var.get()
        activity = activity_var.get()

        if gender == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        activity_multiplier = {"low": 1.2, "moderate": 1.55, "high": 1.9}
        maintenance_calories = bmr * activity_multiplier[activity]
        return round(maintenance_calories + calorie_adjustment, 2)
    except ValueError:
        return "Invalid input"

def get_meal_plan(status):
    # Budget-friendly meal plans based on BMI status
    if status == "underweight":
        return """
        Breakfast: Scrambled eggs with toast and a banana.
        Lunch: Rice and beans with a side of mixed greens.
        Dinner: Chicken with roasted potatoes and carrots.
        Snacks: Peanut butter on whole wheat bread.
        """
    elif status == "normal":
        return """
        Breakfast: Oatmeal with sliced banana and peanut butter.
        Lunch: Whole wheat sandwich with turkey, lettuce, and tomato.
        Dinner: Baked chicken with brown rice and steamed broccoli.
        Snacks: Yogurt with mixed berries and a small handful of almonds.
        """
    elif status == "overweight":
        return """
        Breakfast: Greek yogurt with oats and a handful of berries.
        Lunch: Tuna salad with mixed greens and olive oil dressing.
        Dinner: Grilled chicken with steamed vegetables and quinoa.
        Snacks: Carrot sticks and hummus.
        """
    elif status == "obese":
        return """
        Breakfast: Boiled eggs with spinach and whole wheat toast.
        Lunch: Grilled chicken with quinoa and roasted vegetables.
        Dinner: Baked salmon with green beans and sweet potatoes.
        Snacks: Apple slices with peanut butter.
        """
    return ""

def save_to_report(bmi, status, calorie_needs, exercise_recommendation, meal_plan):
    report_file = f"{current_user}_report.pdf" if current_user else "report.pdf"
    c = canvas.Canvas(report_file, pagesize=letter)

    # Set up header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"Report for {current_user or 'Guest'}")
    
    # Add BMI and status
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 720, f"BMI: {bmi:.2f} ({status})")
    c.drawString(100, 700, f"Calorie Needs: {calorie_needs} kcal/day")
    
    # Add Exercise Recommendation
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 670, "Exercise Recommendation:")
    c.setFont("Helvetica", 10)
    c.drawString(100, 650, exercise_recommendation)
    
    # Add Meal Plan
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 620, "Meal Plan:")
    c.setFont("Helvetica", 10)
    lines = meal_plan.split("\n")
    y_position = 600
    for line in lines:
        c.drawString(100, y_position, line)
        y_position -= 20

    # Add Date
    c.setFont("Helvetica", 10)
    c.drawString(100, y_position - 20, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Save the PDF
    c.showPage()
    c.save()
    messagebox.showinfo("Report Saved", f"Report saved to {report_file}")

# Set up the main window
root = tk.Tk()
root.title("BMI and Healthcare")
root.geometry("600x600")

# Define fonts
font_large = ('Helvetica', 12)
font_bold = ('Helvetica-Bold', 12)

# Define colors
bg_color = "#A8D5BA"  # Soft green background color
button_color = "#4C9A2A"  # Darker green for buttons
entry_color = "#F4F4F4"  # Light gray for entry fields
text_color = "#2F4F4F"  # Darker gray for text

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
current_dir = os.path.dirname(__file__)
image_path = os.path.join(current_dir, "background.jpeg")

# Function to set background image for both frames
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
ttk.Label(login_frame, text="Username:", font=font_bold, foreground=text_color).place(x=100, y=50)
ttk.Entry(login_frame, textvariable=username_var, font=font_large, background=entry_color).place(x=200, y=50, width=200)

ttk.Label(login_frame, text="Password:", font=font_bold, foreground=text_color).place(x=100, y=100)
ttk.Entry(login_frame, textvariable=password_var, show="*", font=font_large, background=entry_color).place(x=200, y=100, width=200)

ttk.Button(login_frame, text="Login", command=login, style="TButton").place(x=150, y=200, width=100)
ttk.Button(login_frame, text="Register", command=register, style="TButton").place(x=300, y=200, width=100)

login_frame.pack(fill="both", expand=True)  # Display the login frame initially

# Set background for the bmi_calculator_frame
set_background(bmi_calculator_frame)

# BMI Calculation Form Widgets
ttk.Label(bmi_calculator_frame, text="Weight (kg):", font=font_bold, foreground=text_color).place(x=100, y=50)
ttk.Entry(bmi_calculator_frame, textvariable=weight_var, font=font_large, background=entry_color).place(x=200, y=50, width=200)

ttk.Label(bmi_calculator_frame, text="Height (cm):", font=font_bold, foreground=text_color).place(x=100, y=100)
ttk.Entry(bmi_calculator_frame, textvariable=height_var, font=font_large, background=entry_color).place(x=200, y=100, width=200)

ttk.Label(bmi_calculator_frame, text="Age:", font=font_bold, foreground=text_color).place(x=100, y=150)
ttk.Entry(bmi_calculator_frame, textvariable=age_var, font=font_large, background=entry_color).place(x=200, y=150, width=200)

ttk.Label(bmi_calculator_frame, text="Gender:", font=font_bold, foreground=text_color).place(x=100, y=200)
ttk.Combobox(bmi_calculator_frame, textvariable=gender_var, values=["male", "female"], font=font_large, state="readonly").place(x=200, y=200, width=200)

ttk.Label(bmi_calculator_frame, text="Activity Level:", font=font_bold, foreground=text_color).place(x=100, y=250)
ttk.Combobox(bmi_calculator_frame, textvariable=activity_var, values=["low", "moderate", "high"], font=font_large, state="readonly").place(x=200, y=250, width=200)

ttk.Button(bmi_calculator_frame, text="Calculate BMI", command=calculate_bmi, style="TButton").place(x=150, y=350, width=100)
ttk.Button(bmi_calculator_frame, text="Logout", command=logout, style="TButton").place(x=300, y=350, width=100)

root.mainloop()
