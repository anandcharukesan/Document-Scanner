import os
from PIL import Image
from main import scanner
import shutil
from fpdf import FPDF
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

def delete_files_in_directory(directory):
    file_list = os.listdir(directory)
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

delete_files_in_directory("scanned_images/")
delete_files_in_directory("Output path/")
delete_files_in_directory("Destination/")

output_directory = "scanned_images/"

def load_images(directory):
    direc = directory
    for filename in os.listdir(direc):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            image_path = os.path.join(directory, filename)
            scanner(image_path, output_directory)

def select_images():
    # Open a dialog to select multiple image files
    image_files = ctk.filedialog.askopenfilenames(title="Select Images")

    # Open a dialog to select the destination folder
    destination_folder = "Destination/"
    # Copy the selected images to the destination folder
    delete_files_in_directory(destination_folder)

    for file in image_files:
        shutil.copy(file, destination_folder)

    print("Images copied successfully!")

    load_images(destination_folder)

def convert_images_to_pdf(directory):
    # Get a list of image files in the specified directory
    image_files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith(
            (".png", ".jpg", ".jpeg"))]

    # Create a PDF object
    pdf = FPDF()

    # Iterate over the image files and add them as pages to the PDF
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        image = Image.open(image_path)

        img_width, img_height = image.size

        pdf.add_page()
        pdf.image(image_path, x=10, y=10, w=pdf.w - 20)

    # Select a directory to save the PDF using a file dialog
    save_directory = ctk.filedialog.askdirectory(title="Select Directory to Save PDF")

    if save_directory:
        # Prompt the user to enter the desired file name for the PDF
        file_path = filedialog.asksaveasfilename(initialdir=save_directory, defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

        if file_path:
            pdf.output(file_path)
            print(f"PDF saved successfully at: {file_path}")

            # Show a custom tkinter window for success message
            success_window = ctk.CTk()
            success_window.geometry("300x150")
            success_window.title("Success")

            success_label = ctk.CTkLabel(success_window, text="PDF saved successfully!", fg_color="transparent", width=40, font=("Arial", 18))
            success_label.pack(pady=20)

            success_window.mainloop()
        else:
            print("No file path selected.")
    else:
        print("No save directory selected.")

def select_directory():
    # Select a directory using a file dialog
    directory = "scanned_images/"
    print(directory)

    # Call the function to convert images to PDF
    if directory:
        convert_images_to_pdf(directory)

# Create the customtikinter window
window = ctk.CTk()

# Set the window size
window.geometry("400x250")

# Increase the font size for the "Document Scanner" label
app_name = ctk.CTkLabel(window, text="Document Scanner", fg_color="transparent", width=40, font=("Arial", 30))
app_name.pack(pady=20, padx=20)

# Create the button to select images
select_button = ctk.CTkButton(window, text="Select Images", command=select_images)
select_button.pack(pady=10)

# Create the button to save PDF
button = ctk.CTkButton(window, text="Save PDF", command=select_directory)
button.pack(pady=10)

# Run the customtikinter event loop
window.mainloop()

