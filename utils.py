from PIL import Image, ImageTk
import os

def set_background(frame, image_path):
    try:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        background_label = tk.Label(frame, image=photo)
        background_label.photo = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error: {e}")

def get_meal_plan(status):
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
