"""import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from random import choice  # Import choice from random module
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from ttkthemes import ThemedStyle
from fpdf import FPDF

# Initialize Firebase with your credentials JSON file
cred = credentials.Certificate("dietician-def53-firebase-adminsdk-bmeut-414b0b260a.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dietician-def53-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a reference to the root of your Firebase Realtime Database
protein_options_ref = db.reference('protein_options')
fruit_options_ref = db.reference('fruit_options')
vegetable_option_ref = db.reference('vegetable_option')
grains_options_ref = db.reference('grains_options')
snack_options_ref = db.reference('snack_options')
taste_enhancer_options_ref = db.reference('taste_enhancer_options')
diabetic_options_ref = db.reference('diabetic_options')

class DietConsultantApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Diet Consultant')
        # Load the background image
        self.background_image = tk.PhotoImage(file="C://Users/vamshi/Desktop/eaman33.png")  # Replace "background_image.png" with your image file

        # Create a label with the background image and place it in the window
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Cover the entire window

        # Create a ThemedStyle object and set the theme
        self.style = ThemedStyle(self.root)
        self.style.set_theme("plastik")

        self.create_widgets()

    def create_widgets(self):
        # Create a frame to organize the input fields
        input_frame = ttk.LabelFrame(self.root, text="User Information")
        input_frame.pack(pady=10, padx=10)

        # Create labels and entry fields for user input
        ttk.Label(input_frame, text='Weight (kg)').grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Height (cm)').grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Age').grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Gender').grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Activity Level').grid(row=4, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Are you Diabetic?').grid(row=5, column=0, padx=5, pady=5)

        self.weight_entry = ttk.Entry(input_frame)
        self.height_entry = ttk.Entry(input_frame)
        self.age_entry = ttk.Entry(input_frame)

        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(input_frame, textvariable=self.gender_var, values=['Male', 'Female'])
        self.gender_var.set('Male')

        self.activity_var = tk.StringVar()
        self.activity_dropdown = ttk.Combobox(input_frame, textvariable=self.activity_var,
                                               values=['Sedentary', 'Lightly active', 'Moderately active', 'Very active', 'Super active'])
        self.activity_var.set('Sedentary')

        self.diabetic_var = tk.StringVar()
        self.diabetic_dropdown = ttk.Combobox(input_frame, textvariable=self.diabetic_var, values=['Yes', 'No'])
        self.diabetic_var.set('No')

        # Place the input fields in the grid
        self.weight_entry.grid(row=0, column=1, padx=5, pady=5)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)
        self.age_entry.grid(row=2, column=1, padx=5, pady=5)
        self.gender_dropdown.grid(row=3, column=1, padx=5, pady=5)
        self.activity_dropdown.grid(row=4, column=1, padx=5, pady=5)
        self.diabetic_dropdown.grid(row=5, column=1, padx=5, pady=5)

        # Create buttons for generating diet plan and downloading PDF
        ttk.Button(input_frame, text='Generate Diet Plan', command=self.generate_diet_plan).grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(input_frame, text='Download PDF', command=self.download_pdf).grid(row=7, column=0, columnspan=2, pady=10)

        # Create a label for displaying the diet plan
        self.diet_plan_label = ttk.Label(self.root, text='', wraplength=400)
        self.diet_plan_label.pack(pady=10)

    def generate_diet_plan(self):
        # Get user input
        weight = float(self.weight_entry.get())
        height = float(self.height_entry.get())
        age = int(self.age_entry.get())
        gender = self.gender_var.get()
        activity = self.activity_var.get()
        diabetic_status = self.diabetic_var.get()

        # Calculate BMR based on gender
        if gender == 'Male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        # Define activity level multipliers
        activity_multipliers = {
            'Sedentary': 1.2,
            'Lightly active': 1.375,
            'Moderately active': 1.55,
            'Very active': 1.725,
            'Super active': 1.9
        }

        # Calculate caloric intake
        caloric_intake = bmr * activity_multipliers[activity]

        # Generate diet plan based on diabetic status
        if diabetic_status == 'Yes':
            diabetic_options = diabetic_options_ref.get()
            diet_plan = "Diabetic-Friendly Meal Plan:\n\n"
            for i, meal in enumerate(diabetic_options, start=1):
                diet_plan += f"Meal {i}: {meal}\n"
        else:
            protein_options = protein_options_ref.get()
            fruit_options = fruit_options_ref.get()
            vegetable_option = vegetable_option_ref.get()
            grains_options = grains_options_ref.get()
            snack_options = snack_options_ref.get()
            taste_enhancer_options = taste_enhancer_options_ref.get()

            diet_plan = "Regular Meal Plan:\n\n"
            for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
                diet_plan += f"{meal_type}: {choice(protein_options)} + {choice(fruit_options)} + {vegetable_option} + Leafy Greens + {choice(grains_options)} + {choice(taste_enhancer_options)}\n"

            diet_plan += f"Snack: {choice(snack_options)} + {vegetable_option}\n"

        self.diet_plan_label.config(text=diet_plan)

    def download_pdf(self):
        diet_plan_text = self.diet_plan_label.cget("text")

        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)  # Larger font size for the header
                self.cell(0, 10, "Diet Plan", 0, 1, "C")

            def footer(self):
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

            def chapter_title(self, title):
                self.set_font("Arial", "B", 12)  # Font size for titles
                self.cell(0, 10, title, 0, 1, "L")
                self.ln(10)

            def chapter_body(self, body):
                self.set_font("Arial", "", 12)  # Font size for body text
                self.multi_cell(0, 10, body)
                self.ln()

        pdf = PDF()
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            pdf.add_page()
            pdf.chapter_title("Diet Plan")
            pdf.chapter_body(diet_plan_text)

            # Set the font family and size for the entire PDF
            pdf.set_font("Times", size=12)  # You can change the font and size as desired

            # Add font styles for specific lines or sections
            pdf.set_font("Times", "B", 12)  # Bold
            pdf.cell(0, 10, "Important Note:", 0, 1, "L")
            pdf.set_font("Times", "", 12)  # Regular
            pdf.multi_cell(0, 10, "Please follow this diet plan strictly for best results.")

            pdf.output(file_path)

if __name__ == '__main__':
    root = tk.Tk()
    app = DietConsultantApp(root)
    root.mainloop()"""


"""import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from random import choice
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from ttkthemes import ThemedStyle
from fpdf import FPDF

# Initialize Firebase with your credentials JSON file
cred = credentials.Certificate("dietician-def53-firebase-adminsdk-bmeut-414b0b260a.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dietician-def53-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a reference to the root of your Firebase Realtime Database
protein_options_ref = db.reference('protein_options')
fruit_options_ref = db.reference('fruit_options')
vegetable_option_ref = db.reference('vegetable_option')
grains_options_ref = db.reference('grains_options')
snack_options_ref = db.reference('snack_options')
taste_enhancer_options_ref = db.reference('taste_enhancer_options')
diabetic_options_ref = db.reference('diabetic_options')

class DietConsultantApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Diet Consultant')
        self.background_image = tk.PhotoImage(file="C://Users/vamshi/Desktop/eaman33.png")

        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.style = ThemedStyle(self.root)
        self.style.set_theme("plastik")

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="User Information")
        input_frame.pack(pady=10, padx=10)

        ttk.Label(input_frame, text='Full Name').grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Phone Number').grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Email ID').grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Weight (kg)').grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Height (cm)').grid(row=4, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Age').grid(row=5, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Gender').grid(row=6, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Activity Level').grid(row=7, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Are you Diabetic?').grid(row=8, column=0, padx=5, pady=5)

        self.full_name_entry = ttk.Entry(input_frame)
        self.phone_number_entry = ttk.Entry(input_frame)
        self.email_entry = ttk.Entry(input_frame)
        self.weight_entry = ttk.Entry(input_frame)
        self.height_entry = ttk.Entry(input_frame)
        self.age_entry = ttk.Entry(input_frame)

        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(input_frame, textvariable=self.gender_var, values=['Male', 'Female'])
        self.gender_var.set('Male')

        self.activity_var = tk.StringVar()
        self.activity_dropdown = ttk.Combobox(input_frame, textvariable=self.activity_var,
                                               values=['Sedentary', 'Lightly active', 'Moderately active', 'Very active', 'Super active'])
        self.activity_var.set('Sedentary')

        self.diabetic_var = tk.StringVar()
        self.diabetic_dropdown = ttk.Combobox(input_frame, textvariable=self.diabetic_var, values=['Yes', 'No'])
        self.diabetic_var.set('No')

        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.phone_number_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)
        self.height_entry.grid(row=4, column=1, padx=5, pady=5)
        self.age_entry.grid(row=5, column=1, padx=5, pady=5)
        self.gender_dropdown.grid(row=6, column=1, padx=5, pady=5)
        self.activity_dropdown.grid(row=7, column=1, padx=5, pady=5)
        self.diabetic_dropdown.grid(row=8, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text='Generate Diet Plan', command=self.generate_diet_plan).grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Button(input_frame, text='Download PDF', command=self.download_pdf).grid(row=10, column=0, columnspan=2, pady=10)

        self.diet_plan_label = ttk.Label(self.root, text='', wraplength=400)
        self.diet_plan_label.pack(pady=10)

    def generate_diet_plan(self):
        full_name = self.full_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        weight = float(self.weight_entry.get())
        height = float(self.height_entry.get())
        age = int(self.age_entry.get())
        gender = self.gender_var.get()
        activity = self.activity_var.get()
        diabetic_status = self.diabetic_var.get()

        # Calculate BMR based on gender
        if gender == 'Male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        activity_multipliers = {
            'Sedentary': 1.2,
            'Lightly active': 1.375,
            'Moderately active': 1.55,
            'Very active': 1.725,
            'Super active': 1.9
        }

        caloric_intake = bmr * activity_multipliers[activity]

        if diabetic_status == 'Yes':
            diabetic_options = diabetic_options_ref.get()
            diet_plan = f"Diabetic-Friendly Meal Plan for {full_name}:\n\n"
            for i, meal in enumerate(diabetic_options, start=1):
                diet_plan += f"Meal {i}: {meal}\n"
        else:
            protein_options = protein_options_ref.get()
            fruit_options = fruit_options_ref.get()
            vegetable_option = vegetable_option_ref.get()
            grains_options = grains_options_ref.get()
            snack_options = snack_options_ref.get()
            taste_enhancer_options = taste_enhancer_options_ref.get()

            diet_plan = f"Regular Meal Plan for {full_name}:\n\n"
            for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
                diet_plan += f"{meal_type}: {choice(protein_options)} + {choice(fruit_options)} + {vegetable_option} + Leafy Greens + {choice(grains_options)} + {choice(taste_enhancer_options)}\n"

            diet_plan += f"Snack: {choice(snack_options)} + {vegetable_option}\n"

        self.diet_plan_label.config(text=diet_plan)

    def download_pdf(self):
        diet_plan_text = self.diet_plan_label.cget("text")

        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)
                self.cell(0, 10, "Diet Plan", 0, 1, "C")

            def footer(self):
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

            def chapter_title(self, title):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, title, 0, 1, "L")
                self.ln(10)

            def chapter_body(self, body):
                self.set_font("Arial", "", 12)
                self.multi_cell(0, 10, body)
                self.ln()

        pdf = PDF()
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            pdf.add_page()
            pdf.chapter_title("Diet Plan")
            pdf.chapter_body(diet_plan_text)
            pdf.set_font("Times", size=12)

            pdf.set_font("Times", "B", 12)
            pdf.cell(0, 10, "Important Note:", 0, 1, "L")
            pdf.set_font("Times", "", 12)
            pdf.multi_cell(0, 10, "Please follow this diet plan strictly for best results.")

            pdf.output(file_path)

if __name__ == '__main__':
    root = tk.Tk()
    app = DietConsultantApp(root)
    root.mainloop()"""



import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from random import choice
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from ttkthemes import ThemedStyle
from fpdf import FPDF

# Initialize Firebase with your credentials JSON file
cred = credentials.Certificate("dietician-def53-firebase-adminsdk-bmeut-414b0b260a.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dietician-def53-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Get a reference to the root of your Firebase Realtime Database
protein_options_ref = db.reference('protein_options')
fruit_options_ref = db.reference('fruit_options')
vegetable_option_ref = db.reference('vegetable_option')
grains_options_ref = db.reference('grains_options')
snack_options_ref = db.reference('snack_options')
taste_enhancer_options_ref = db.reference('taste_enhancer_options')
diabetic_options_ref = db.reference('diabetic_options')

class DietConsultantApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Diet Consultant')
        self.background_image = tk.PhotoImage(file="C://Users/vamshi/Desktop/eaman.png")

        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.style = ThemedStyle(self.root)
        self.style.set_theme("plastik")

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="User Information")
        input_frame.pack(pady=10, padx=10)

        ttk.Label(input_frame, text='Full Name').grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Phone Number').grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Email ID').grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Weight (kg)').grid(row=3, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Height (cm)').grid(row=4, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Age').grid(row=5, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Gender').grid(row=6, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Activity Level').grid(row=7, column=0, padx=5, pady=5)
        ttk.Label(input_frame, text='Are you Diabetic?').grid(row=8, column=0, padx=5, pady=5)

        self.full_name_entry = ttk.Entry(input_frame)
        self.phone_number_entry = ttk.Entry(input_frame)
        self.email_entry = ttk.Entry(input_frame)
        self.weight_entry = ttk.Entry(input_frame)
        self.height_entry = ttk.Entry(input_frame)
        self.age_entry = ttk.Entry(input_frame)

        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(input_frame, textvariable=self.gender_var, values=['Male', 'Female'])
        self.gender_var.set('Male')

        self.activity_var = tk.StringVar()
        self.activity_dropdown = ttk.Combobox(input_frame, textvariable=self.activity_var,
                                               values=['Sedentary', 'Lightly active', 'Moderately active', 'Very active', 'Super active'])
        self.activity_var.set('Sedentary')

        self.diabetic_var = tk.StringVar()
        self.diabetic_dropdown = ttk.Combobox(input_frame, textvariable=self.diabetic_var, values=['Yes', 'No'])
        self.diabetic_var.set('No')

        self.full_name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.phone_number_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        self.weight_entry.grid(row=3, column=1, padx=5, pady=5)
        self.height_entry.grid(row=4, column=1, padx=5, pady=5)
        self.age_entry.grid(row=5, column=1, padx=5, pady=5)
        self.gender_dropdown.grid(row=6, column=1, padx=5, pady=5)
        self.activity_dropdown.grid(row=7, column=1, padx=5, pady=5)
        self.diabetic_dropdown.grid(row=8, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text='Generate Diet Plan', command=self.generate_diet_plan).grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Button(input_frame, text='Download PDF', command=self.download_pdf).grid(row=10, column=0, columnspan=2, pady=10)

        self.diet_plan_label = ttk.Label(self.root, text='', wraplength=400)
        self.diet_plan_label.pack(pady=10)

    def generate_diet_plan(self):
        full_name = self.full_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        weight = float(self.weight_entry.get())
        height = float(self.height_entry.get())
        age = int(self.age_entry.get())
        gender = self.gender_var.get()
        activity = self.activity_var.get()
        diabetic_status = self.diabetic_var.get()

        # Calculate BMR based on gender
        if gender == 'Male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        activity_multipliers = {
            'Sedentary': 1.2,
            'Lightly active': 1.375,
            'Moderately active': 1.55,
            'Very active': 1.725,
            'Super active': 1.9
        }

        caloric_intake = bmr * activity_multipliers[activity]

        if diabetic_status == 'Yes':
            diabetic_options = diabetic_options_ref.get()
            diet_plan = f"Diabetic-Friendly Meal Plan for {full_name}:\n\n"
            for i, meal in enumerate(diabetic_options, start=1):
                diet_plan += f"Meal {i}: {meal}\n"
        else:
            protein_options = protein_options_ref.get()
            fruit_options = fruit_options_ref.get()
            vegetable_option = vegetable_option_ref.get()
            grains_options = grains_options_ref.get()
            snack_options = snack_options_ref.get()
            taste_enhancer_options = taste_enhancer_options_ref.get()

            diet_plan = f"Regular Meal Plan for {full_name}:\n\n"
            for meal_type in ['Breakfast', 'Lunch', 'Dinner']:
                diet_plan += f"{meal_type}: {choice(protein_options)} + {choice(fruit_options)} + {vegetable_option} + Leafy Greens + {choice(grains_options)} + {choice(taste_enhancer_options)}\n"

            diet_plan += f"Snack: {choice(snack_options)} + {vegetable_option}\n"

        self.diet_plan_label.config(text=diet_plan)

    def download_pdf(self):
        full_name = self.full_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()
        diet_plan_text = self.diet_plan_label.cget("text")

        class PDF(FPDF):
            def header(self):
                self.set_font("Arial", "B", 14)
                self.cell(0, 10, "Diet Plan", 0, 1, "C")

            def footer(self):
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

            def chapter_title(self, title):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, title, 0, 1, "L")
                self.ln(10)

            def chapter_body(self, body):
                self.set_font("Arial", "", 12)
                self.multi_cell(0, 10, body)
                self.ln()

            def user_details(self, name, phone, email):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, "User Details", 0, 1, "L")
                self.set_font("Arial", "", 12)
                self.cell(0, 10, f"Full Name: {name}", 0, 1, "L")
                self.cell(0, 10, f"Phone Number: {phone}", 0, 1, "L")
                self.cell(0, 10, f"Email ID: {email}", 0, 1, "L")
                self.ln(10)

        pdf = PDF()
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            pdf.add_page()
            pdf.user_details(full_name, phone_number, email)
            pdf.chapter_title("Diet Plan")
            pdf.chapter_body(diet_plan_text)
            pdf.set_font("Times", size=12)

            pdf.set_font("Times", "B", 12)
            pdf.cell(0, 10, "Important Note:", 0, 1, "L")
            pdf.set_font("Times", "", 12)
            pdf.multi_cell(0, 10, "Please follow this diet plan strictly for best results.")

            pdf.output(file_path)

if __name__ == '__main__':
    root = tk.Tk()
    app = DietConsultantApp(root)
    root.mainloop()
