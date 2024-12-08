from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def save_to_report(bmi, status, calorie_needs, exercise_recommendation, meal_plan, current_user):
    report_file = f"{current_user}_report.pdf" if current_user else "report.pdf"
    c = canvas.Canvas(report_file, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, f"Report for {current_user or 'Guest'}")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 720, f"BMI: {bmi:.2f} ({status})")
    c.drawString(100, 700, f"Calorie Needs: {calorie_needs} kcal/day")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 670, "Exercise Recommendation:")
    c.setFont("Helvetica", 10)
    c.drawString(100, 650, exercise_recommendation)
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 620, "Meal Plan:")
    c.setFont("Helvetica", 10)
    lines = meal_plan.split("\n")
    y_position = 600
    for line in lines:
        c.drawString(100, y_position, line)
        y_position -= 20

    c.setFont("Helvetica", 10)
    c.drawString(100, y_position - 20, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    c.showPage()
    c.save()
