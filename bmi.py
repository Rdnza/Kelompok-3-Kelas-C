from tkinter import messagebox

def calculate_bmi(weight, height, age, gender, activity):
    try:
        height = height / 100  # Convert to meters
        bmi = weight / (height ** 2)

        if bmi < 18.5:
            status = "Underweight"
            calorie_adjustment = 500
        elif 18.5 <= bmi <= 24.9:
            status = "Normal"
            calorie_adjustment = 0
        elif 25 <= bmi <= 29.9:
            status = "Overweight"
            calorie_adjustment = -500
        else:
            status = "Obese"
            calorie_adjustment = -750

        calorie_needs = calculate_calories(weight, height, age, gender, activity, calorie_adjustment)
        return bmi, status, calorie_needs
    except ValueError:
        messagebox.showerror("Error", "Please enter valid inputs!")

def calculate_calories(weight, height, age, gender, activity, calorie_adjustment):
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multiplier = {"low": 1.2, "moderate": 1.55, "high": 1.9}
    maintenance_calories = bmr * activity_multiplier[activity]
    return round(maintenance_calories + calorie_adjustment, 2)
