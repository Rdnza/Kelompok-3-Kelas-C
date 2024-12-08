import tkinter as tk
from tkinter import ttk
from auth import login, register, logout
from bmi import calculate_bmi
from report import save_to_report
from database import load_history_database, save_history_database
from utils import set_background, get_meal_plan