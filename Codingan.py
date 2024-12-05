import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

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

# Save users data to database
def save_users_database(data):
    with open(USERS_DB_FILE, "w") as f:
        json.dump(data, f)

# Load or initialize the history database
def load_history_database():
    try:
        with open(HISTORY_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"history": {}}

# Save history data to database
def save_history_database(data):
    with open(HISTORY_DB_FILE, "w") as f:
        json.dump(data, f)

# Login functionality
def login():
    global current_user
    username = username_var.get()
    password = password_var.get()

    users_data = load_users_database()
    if username in users_data["users"] and users_data["users"][username] == password:
        current_user = username
        messagebox.showinfo("Success", "Login successful!")
        notebook.tab(1, state="normal")
        notebook.select(1)
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# Register functionality
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

# Logout functionality
def logout():
    global current_user
    current_user = None
    notebook.select(0)
    notebook.tab(1, state="disabled")
    messagebox.showinfo("Logout", "You have successfully logged out!")

# Calculate BMI and transition to calorie calculation
def calculate_bmi():
    try:
        weight = float(weight_var.get())
        height = float(height_var.get()) / 100  # Convert to meters
        bmi = weight / (height ** 2)

        if bmi < 18.5:
            status = "Underweight"
            calorie_adjustment = 500
            recommendation = "Increase your calorie intake with nutrient-dense foods. Light resistance exercises can help build muscle mass."
        elif 18.5 <= bmi <= 24.9:
            status = "Normal"
            calorie_adjustment = 0
            recommendation = "Maintain your current diet and exercise routine to stay healthy."
        elif 25 <= bmi <= 29.9:
            status = "Overweight"
            calorie_adjustment = -500
            recommendation = "Adopt a calorie deficit diet and include moderate-intensity exercises like cycling."
        else:
            status = "Obese"
            calorie_adjustment = -750
            recommendation = "Follow a low-calorie diet and incorporate low-impact exercises like swimming."

        # Save BMI to history
        history_data = load_history_database()
        if current_user:
            if current_user not in history_data["history"]:
                history_data["history"][current_user] = []
            history_data["history"][current_user].append({"type": "BMI", "value": bmi, "status": status})
            save_history_database(history_data)

        # Show BMI result and proceed to calorie calculation
        messagebox.showinfo(
            "BMI Result",
            f"Your BMI: {bmi:.2f} ({status})\n\nRecommendation:\n{recommendation}"
        )
        calculate_calories(bmi, calorie_adjustment, status)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid inputs!")

# Calculate Calorie Needs
def calculate_calories(bmi, calorie_adjustment, status):
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
        target_calories = maintenance_calories + calorie_adjustment

        # Recommendations based on BMI status
        meal_plan = generate_meal_plan(target_calories, status)

        messagebox.showinfo(
            "Calorie Needs",
            f"Your daily calorie target is: {target_calories:.2f} kcal\n\n"
            f"Suggested Meal Plan:\n{meal_plan['details']}\n\n"
            f"Exercise Recommendation:\n{meal_plan['exercise']}"
        )

        # Save the report
        save_report(bmi, status, target_calories, meal_plan)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid inputs!")

# Generate a report and save it to a file
def save_report(bmi, status, target_calories, meal_plan):
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")
        report_content = f"""
        User Report - {current_user}
        Date: {date_str}
        ===========================
        BMI Calculation:
        ---------------------------
        BMI: {bmi:.2f}
        Status: {status}

        Calorie Needs:
        ---------------------------
        Daily Calorie Target: {target_calories:.2f} kcal

        Suggested Meal Plan:
        ---------------------------
        {meal_plan['details']}

        Exercise Recommendation:
        ---------------------------
        {meal_plan['exercise']}
        """
        # Save the report to a file
        report_file = f"{current_user}report{date_str}.txt"
        with open(report_file, "w") as file:
            file.write(report_content)

        messagebox.showinfo(
            "Report Saved",
            f"Report has been saved successfully as '{report_file}' in the current directory."
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the report: {str(e)}")

def generate_meal_plan(target_calories, status):
    """Generate a meal plan and exercise recommendation based on target calories and BMI status."""
    breakfast = round(target_calories * 0.3)
    lunch = round(target_calories * 0.35)
    dinner = round(target_calories * 0.25)
    snacks = round(target_calories * 0.1)

    meal_options = {
        "breakfast": ["Oatmeal with fruits", "Scrambled eggs with toast"],
        "lunch": ["Grilled chicken salad", "Vegetable stir-fry with rice"],
        "dinner": ["Baked salmon with vegetables", "Vegetarian curry with rice"],
        "snacks": ["Mixed nuts", "Protein bar"]
    }

    if status in ["Overweight", "Obese"]:
        exercise = "Cardio-focused workouts like brisk walking, cycling, or swimming."
    elif status == "Underweight":
        exercise = "Light resistance exercises to build muscle mass."
    else:
        exercise = "Maintain regular activities like walking or jogging."

    details = (
        f"Breakfast: {breakfast} kcal - {meal_options['breakfast'][0]}\n"
        f"Lunch: {lunch} kcal - {meal_options['lunch'][0]}\n"
        f"Dinner: {dinner} kcal - {meal_options['dinner'][0]}\n"
        f"Snacks: {snacks} kcal - {meal_options['snacks'][0]}"
    )

    return {"details": details, "exercise": exercise}

# UI setup
root = tk.Tk()
root.title("BMI and Calorie Needs Calculator")
root.geometry("600x500")  # Adjusted size for better appearance
root.configure(bg="#f5f5f5")

# Improved styling
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#f5f5f5")
style.configure("TLabel", background="#f5f5f5", foreground="#333333", font=("Arial", 12))
style.configure("TButton", background="#008CBA", foreground="white", font=("Arial", 12), padding=5)
style.map("TButton", background=[("active", "#005f73")])

# Notebook for tabbed interface
notebook = ttk.Notebook(root)
login_tab = ttk.Frame(notebook)
calculator_tab = ttk.Frame(notebook)

notebook.add(login_tab, text="Login")
notebook.add(calculator_tab, text="Calculator", state="disabled")
notebook.pack(expand=True, fill="both")

# Login Tab UI Elements
username_var = tk.StringVar()
password_var = tk.StringVar()

ttk.Label(login_tab, text="Username:", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=10)
ttk.Entry(login_tab, textvariable=username_var, font=("Arial", 12), width=25).grid(row=0, column=1, padx=20, pady=10)

ttk.Label(login_tab, text="Password:", font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10)
ttk.Entry(login_tab, textvariable=password_var, font=("Arial", 12), show="*", width=25).grid(row=1, column=1, padx=20, pady=10)

ttk.Button(login_tab, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)
ttk.Button(login_tab, text="Register", command=register).grid(row=3, column=0, columnspan=2, pady=10)

# Calculator Tab UI Elements
weight_var = tk.StringVar()
height_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
activity_var = tk.StringVar()

ttk.Label(calculator_tab, text="Weight (kg):", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=10)
ttk.Entry(calculator_tab, textvariable=weight_var, font=("Arial", 12), width=25).grid(row=0, column=1, padx=20, pady=10)

ttk.Label(calculator_tab, text="Height (cm):", font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10)
ttk.Entry(calculator_tab, textvariable=height_var, font=("Arial", 12), width=25).grid(row=1, column=1, padx=20, pady=10)

ttk.Label(calculator_tab, text="Age (years):", font=("Arial", 12)).grid(row=2, column=0, padx=20, pady=10)
ttk.Entry(calculator_tab, textvariable=age_var, font=("Arial", 12), width=25).grid(row=2, column=1, padx=20, pady=10)

ttk.Label(calculator_tab, text="Gender:", font=("Arial", 12)).grid(row=3, column=0, padx=20, pady=10)
gender_dropdown = ttk.Combobox(calculator_tab, textvariable=gender_var, font=("Arial", 12), values=["male", "female"], state="readonly", width=22)
gender_dropdown.grid(row=3, column=1, padx=20, pady=10)
gender_dropdown.set("Select Gender")

ttk.Label(calculator_tab, text="Activity Level:", font=("Arial", 12)).grid(row=4, column=0, padx=20, pady=10)
activity_dropdown = ttk.Combobox(calculator_tab, textvariable=activity_var, font=("Arial", 12), values=["low", "moderate", "high"], state="readonly", width=22)
activity_dropdown.grid(row=4, column=1, padx=20, pady=10)
activity_dropdown.set("Select Activity Level")

ttk.Button(calculator_tab, text="Calculate BMI and Calorie Needs", command=calculate_bmi).grid(row=5, column=0, columnspan=2, pady=20)
ttk.Button(calculator_tab, text="Logout", command=logout).grid(row=6, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()