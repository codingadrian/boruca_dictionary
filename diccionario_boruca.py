import os
import customtkinter as ctk
import json
import requests
import webbrowser
from datetime import datetime

# URL of the JSON file in the GitHub repository
GITHUB_JSON_URL = "https://raw.githubusercontent.com/codingadrian/user_boruca_dictionary/master/diccionario_boruca.json"
LOCAL_JSON_PATH = os.path.expanduser("~/.local/share/boruca_dictionary.json")
DOWNLOAD_INFO_PATH = os.path.expanduser("~/.local/share/download_info.json")

# Ensure the directory exists
if not os.path.exists(os.path.dirname(LOCAL_JSON_PATH)):
    os.makedirs(os.path.dirname(LOCAL_JSON_PATH))


# Load data from the JSON file hosted on GitHub with error handling and local file storage
def load_data():
    try:
        # Attempt to download the JSON file from GitHub
        response = requests.get(GITHUB_JSON_URL, timeout=10)
        response.raise_for_status()  # Check for HTTP errors

        # Save the downloaded JSON to a local file
        with open(LOCAL_JSON_PATH, "w", encoding="utf-8") as local_file:
            json.dump(response.json(), local_file, ensure_ascii=False, indent=4)

        # Save the download date to a separate file
        with open(DOWNLOAD_INFO_PATH, "w", encoding="utf-8") as info_file:
            download_info = {
                "last_download_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            json.dump(download_info, info_file, ensure_ascii=False, indent=4)

        # Return the data from the downloaded JSON
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error downloading data from GitHub: {e}")

        # If download fails, try to load from the local file
        if os.path.exists(LOCAL_JSON_PATH):
            print("Loading data from the local file.")
            with open(LOCAL_JSON_PATH, "r", encoding="utf-8") as local_file:
                return json.load(local_file)

        # If no local file exists, return an empty dataset
        print("No local data available.")
        return {"words": []}

# Applies a default theme
ctk.set_appearance_mode("light")  # Set the default theme
ctk.set_default_color_theme("blue")  # Set the default color theme

# Function to search for a word in both Boruca and Spanish
def search_word(word_to_search, data, from_language):
    matches = []
    word_to_search = word_to_search.lower()
    for entry in data['words']:
        if from_language == "Boruca" and word_to_search == entry['boruca_word'].lower():
            matches.append(entry)
        elif from_language == "Español" and word_to_search == entry['spanish_translation'].lower():
            matches.append(entry)
    return matches

# Function to display search results in a formatted box
def display_results(results, search_entry, data, search_language):
    # Clear any previous results
    for widget in result_frame.winfo_children():
        widget.destroy()

    if not results:
        # Display a message if no results are found
        no_results_label = ctk.CTkLabel(result_frame, text=f"No se encontraron resultados para '{search_entry.get()}'.", font=("Arial", 12))
        no_results_label.pack(pady=10)
        root.geometry("")  # Resize the window to fit the content
        return

    word_grouped = {}
    for result in results:
        word = result['boruca_word']
        if word not in word_grouped:
            word_grouped[word] = []
        word_grouped[word].append(result)

    for i, (word, entries) in enumerate(word_grouped.items(), start=1):
        # Container frame for the word result
        result_container = ctk.CTkFrame(result_frame, corner_radius=10, border_width=2, border_color="black")
        result_container.pack(fill="x", pady=10, padx=10)

        # Display the word in bold
        word_label = ctk.CTkLabel(result_container, text=f"{word.capitalize()}", font=("Arial", 14, "bold"))
        word_label.pack(anchor="w", padx=10, pady=5)

        for j, entry in enumerate(entries, start=1):
            # Format part of speech and translation
            pos_translation_label = ctk.CTkLabel(result_container, text=f"{j}. ({entry['part_of_speech']}) {entry['spanish_translation']}")
            pos_translation_label.pack(anchor="w", padx=20)

            # Format example sentences in italic
            example_label = ctk.CTkLabel(result_container, text=f"\"{entry['example_sentence_boruca']}\" | \"{entry['example_sentence_spanish']}\"", font=("Arial", 12, "italic"))
            example_label.pack(anchor="w", padx=40, pady=5)

            # Display the comment if it exists
            if "comment" in entry and entry["comment"]:
                comment_label = ctk.CTkLabel(result_container, text=f"Comentario: {entry['comment']}", font=("Arial", 12))
                comment_label.pack(anchor="w", padx=40, pady=5)

    root.geometry("")  # Resize the window to fit the content
    result_frame.update_idletasks()

# Function to open the website
def open_website(url):
    webbrowser.open(url)

# Function to retrieve and save the last download date
def get_last_download_date():
    if os.path.exists(DOWNLOAD_INFO_PATH):
        with open(DOWNLOAD_INFO_PATH, "r", encoding="utf-8") as info_file:
            download_info = json.load(info_file)
            return download_info.get("last_download_date", "Fecha desconocida")
    return "Fecha desconocida"

# Function to create the main window
def create_main_window():
    global result_frame, root

    # Load data from JSON hosted on GitHub
    data = load_data()

    root = ctk.CTk()
    root.title("Diccionario Boruca")

    # Create variable for search language
    search_language = ctk.StringVar(value="Boruca")

    # Top Frame for language selection
    top_frame = ctk.CTkFrame(root)
    top_frame.pack(anchor="ne", padx=10, pady=10)

    language_selector = ctk.CTkOptionMenu(top_frame, variable=search_language, values=["Boruca", "Español"])
    language_selector.pack(side=ctk.RIGHT, padx=5)

    # Functions for dictionary operations
    def on_search(event=None):
        word = search_entry.get()
        results = search_word(word, data, search_language.get())
        display_results(results, search_entry, data, search_language)

    # ----DISPLAY----

    # Welcome Message
    ctk.CTkLabel(root, text="¡Bienvenido a la aplicación del Diccionario Boruca!", font=("Arial", 12), justify=ctk.CENTER).pack(pady=10)

    # How it works
    ctk.CTkLabel(root, text="Esta aplicación te permite buscar palabras en el idioma Boruca.", font=("Arial", 12), justify=ctk.CENTER).pack(pady=10)

    # Search Entry and Button
    search_entry = ctk.CTkEntry(root, width=100)
    search_entry.pack(pady=10)

    # Bind the Enter key to the on_search function
    search_entry.bind("<Return>", on_search)

    ctk.CTkButton(root, text="Buscar", command=on_search).pack(pady=10)

    # Result Frame for displaying search results
    result_frame = ctk.CTkFrame(root)
    result_frame.pack(pady=20, padx=10, fill="both", expand=True)

    # Bottom Frame
    bottom_frame = ctk.CTkFrame(root)
    bottom_frame.pack(side=ctk.BOTTOM, fill=ctk.X, padx=10, pady=10)

    # Create a footer container for centering
    footer_container = ctk.CTkFrame(bottom_frame)
    footer_container.pack(anchor="center")

    # Last Download Date and Version Display
    last_download_date = get_last_download_date()
    version_info = f"Versión 1.0 - Data Fecha: {last_download_date}"
    ctk.CTkLabel(footer_container, text=version_info, font=("Arial", 10)).pack(pady=5)


    # Website URL (modify this URL as needed)
    website_url = "https://www.example.com"

    # Footer
    footer_text = "© 2024 Diccionario Boruca. Todos los derechos reservados. Visita "
    footer_label = ctk.CTkLabel(footer_container, text=footer_text, font=("Arial", 10))
    footer_label.pack(side=ctk.LEFT)

    website_link = ctk.CTkLabel(footer_container, text="este sitio web", font=("Arial", 10), text_color="blue", cursor="hand2")
    website_link.pack(side=ctk.LEFT)
    website_link.bind("<Button-1>", lambda e: open_website(website_url))

    ctk.CTkLabel(footer_container, text=" para más información.", font=("Arial", 10)).pack(side=ctk.LEFT)

    root.mainloop()

# Run the application
if __name__ == "__main__":
    create_main_window()
