import customtkinter as ctk
import requests
import json

GITHUB_JSON_URL = "https://raw.githubusercontent.com/codingadrian/boruca_dictionary/dev-branch/boruca_dictionary.json"

# Load data from the JSON file hosted on GitHub with error handling
def load_data():
    try:
        response = requests.get(GITHUB_JSON_URL)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()  # Parse JSON content
    except requests.exceptions.RequestException as e:
        print(f"Error al cargar los datos desde GitHub: {e}")
        return {"words": []}

# Initialize the main window
root = ctk.CTk()
root.title("Diccionario Boruca")
root.geometry("600x400")  # Set the default window size

# Set the appearance mode and color theme
ctk.set_appearance_mode("light")  # Can be "dark" or "light"
ctk.set_default_color_theme("blue")  # Can be "blue", "green", or "dark-blue"

# Add a welcome label
welcome_label = ctk.CTkLabel(root, text="¡Bienvenido al Diccionario Boruca!", font=("Arial", 16))
welcome_label.pack(pady=20)


data = load_data()
print(data)

# Start the main application loop
root.mainloop()
