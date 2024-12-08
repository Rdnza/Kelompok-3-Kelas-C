# bmi.py
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from database import load_history_database, save_history_database

# Function to calculate BMI and provide recommendations
def calculate_bmi(weight_var, height_var, age_var, gender_var, activity_var, current_user):
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

        calorie_needs = calculate_calories(weight_var, height_var, age_var, gender_var, activity_var, calorie_adjustment)
        save_to_report(bmi, status, calorie_needs, exercise_recommendation, meal_plan, current_user)

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

# Function to calculate calories
def calculate_calories(weight_var, height_var, age_var, gender_var, activity_var, calorie_adjustment):
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

# Function to get meal plan based on BMI status
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

# Function to save BMI result to a PDF report
def save_to_report(bmi, status, calorie_needs, exercise_recommendation, meal_plan, current_user):
    # Use the logged-in username for the file name, or "guest" if no user is logged in
    report_file = f"{current_user}_report.pdf" if current_user else "guest_report.pdf"
    
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
    c.drawString(100, 670, "Exercise Recommendation: ")
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

# Example of how to use this:
# Assuming 'current_user' is fetched from your database after a successful login.
# current_user = "john_doe"  # This is just an example, it will be dynamically set after login.
