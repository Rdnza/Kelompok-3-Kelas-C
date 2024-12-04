import tkinter as tk
from tkinter import ttk, messagebox
import json

# Database File
DB_FILE = "user_data.json"

# Current logged-in user
current_user = None

# Load or initialize the database
def load_database():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}, "history": {}}

def save_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Login functionality
def login():
    global current_user
    username = username_var.get()
    password = password_var.get()

    data = load_database()
    if username in data["users"] and data["users"][username] == password:
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

    data = load_database()
    if username in data["users"]:
        messagebox.showerror("Error", "Username already exists!")
    else:
        data["users"][username] = password
        save_database(data)
        messagebox.showinfo("Success", "Registration successful!")

# Calculate BMI and transition to calorie calculation
def calculate_bmi():
    try:
        weight = float(weight_var.get())
        height = float(height_var.get()) / 100  # Convert to meters
        bmi = weight / (height ** 2)

        if bmi < 18.5:
            status = "Underweight"
            calorie_adjustment = 500  # Gain weight
            recommendation = (
                "Increase your calorie intake with nutrient-dense foods like nuts, avocado, and whole grains.\n"
                "Light resistance exercises can help build muscle mass."
            )
        elif 18.5 <= bmi <= 24.9:
            status = "Normal"
            calorie_adjustment = 0  # Maintain weight
            recommendation = (
                "Maintain your current diet and exercise routine to stay healthy.\n"
                "Engage in regular physical activity like walking or light jogging."
            )
        elif 25 <= bmi <= 29.9:
            status = "Overweight"
            calorie_adjustment = -500  # Lose weight
            recommendation = (
                "Adopt a calorie deficit diet with vegetables, lean proteins, and whole grains.\n"
                "Include moderate-intensity exercises like cycling or brisk walking for 30-45 minutes daily."
            )
        else:
            status = "Obese"
            calorie_adjustment = -750  # Lose weight faster
            recommendation = (
                "Follow a low-calorie, balanced diet. Consult a healthcare provider for a personalized plan.\n"
                "Incorporate low-impact exercises like swimming or yoga."
            )

        # Save the BMI result
        data = load_database()
        if current_user:
            if current_user not in data["history"]:
                data["history"][current_user] = []
            data["history"][current_user].append({"type": "BMI", "value": bmi, "status": status})
            save_database(data)

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
    except ValueError:
        messagebox.showerror("Error", "Please enter valid inputs!")

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

notebook = ttk.Notebook(root)
login_tab = ttk.Frame(notebook)
calculator_tab = ttk.Frame(notebook)

notebook.add(login_tab, text="Login")
notebook.add(calculator_tab, text="Calculator", state="disabled")
notebook.pack(expand=True, fill="both")

# Login Tab
username_var = tk.StringVar()
password_var = tk.StringVar()

ttk.Label(login_tab, text="Username:").grid(row=0, column=0, padx=10, pady=10)
ttk.Entry(login_tab, textvariable=username_var).grid(row=0, column=1, padx=10, pady=10)

ttk.Label(login_tab, text="Password:").grid(row=1, column=0, padx=10, pady=10)
ttk.Entry(login_tab, textvariable=password_var, show="*").grid(row=1, column=1, padx=10, pady=10)

ttk.Button(login_tab, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)
ttk.Button(login_tab, text="Register", command=register).grid(row=3, column=0, columnspan=2, pady=10)

# Calculator Tab
weight_var = tk.StringVar()
height_var = tk.StringVar()
age_var = tk.StringVar()
gender_var = tk.StringVar()
activity_var = tk.StringVar()

ttk.Label(calculator_tab, text="Weight (kg):").grid(row=0, column=0, padx=10, pady=10)
ttk.Entry(calculator_tab, textvariable=weight_var).grid(row=0, column=1, padx=10, pady=10)

ttk.Label(calculator_tab, text="Height (cm):").grid(row=1, column=0, padx=10, pady=10)
ttk.Entry(calculator_tab, textvariable=height_var).grid(row=1, column=1, padx=10, pady=10)

ttk.Label(calculator_tab, text="Age:").grid(row=2, column=0, padx=10, pady=10)
ttk.Entry(calculator_tab, textvariable=age_var).grid(row=2, column=1, padx=10, pady=10)

ttk.Label(calculator_tab, text="Gender:").grid(row=3, column=0, padx=10, pady=10)
ttk.Combobox(calculator_tab, textvariable=gender_var, values=["male", "female"]).grid(row=3, column=1, padx=10, pady=10)

ttk.Label(calculator_tab, text="Activity Level:").grid(row=4, column=0, padx=10, pady=10)
ttk.Combobox(
    calculator_tab, 
    textvariable=activity_var, 
    values=["low", "moderate", "high"]
).grid(row=4, column=1, padx=10, pady=10)

ttk.Button(calculator_tab, text="Calculate BMI", command=calculate_bmi).grid(row=5, column=0, columnspan=2, pady=10)

# Initialize the application
root.mainloop()