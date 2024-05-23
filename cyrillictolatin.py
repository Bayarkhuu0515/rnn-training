import tkinter as tk
from tkinter import filedialog, messagebox
import re

# Simple mapping dictionary for Cyrillic to Latin
cyrillic_to_latin_simple = {
    'ий': 'ii', 'ай': 'ai', 'эй': 'ei','ой': 'oi', 'уй': 'ui', 'үй': 'ui',
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'ye', 'ж': 'j', 'з': 'z',
    'и': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
    'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ү': 'u',
    'ш': 'sh', 'ы': 'i', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'ё': 'yo', 'ө':'o'
}

# Function for simple mapping translation
def translate_simple(text):
    result = ''
    skip = 0
    for i, char in enumerate(text):
        if skip:
            skip -= 1
            continue
        if i < len(text) - 1 and text[i:i+2].lower() in cyrillic_to_latin_simple:
            latin = cyrillic_to_latin_simple[text[i:i+2].lower()]
            if text[i].isupper():
                latin = latin.upper()
            result += latin
            skip = 1
        else:
            latin = cyrillic_to_latin_simple.get(char.lower(), char)
            if char.isupper():
                latin = latin.upper()
            result += latin
    return result

# Hybrid translation function
def hybrid_translation(text):
    # Apply simple mapping translation
    text = translate_simple(text)
    print("After simple mapping:", text)
    return text

# Function to handle translation and update the GUI
def translate():
    input_file_path = input_file_entry.get()
    output_file_path = output_file_entry.get()

    if not input_file_path:
        messagebox.showerror("Error", "Please select an input file.")
        return
    if not output_file_path:
        messagebox.showerror("Error", "Please select an output file.")
        return

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            cyrillic_text = f.read().strip()
            latin_text = hybrid_translation(cyrillic_text)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(latin_text)

        messagebox.showinfo("Success", "Translation completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Set up the GUI
root = tk.Tk()
root.title("Cyrillic to Latin Translator")

# Input file selection
input_file_label = tk.Label(root, text="Input File:")
input_file_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)

def browse_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

browse_input_button = tk.Button(root, text="Browse", command=browse_input_file)
browse_input_button.grid(row=0, column=2, padx=5, pady=5)

# Output file selection
output_file_label = tk.Label(root, text="Output File:")
output_file_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=5)

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

browse_output_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_output_button.grid(row=1, column=2, padx=5, pady=5)

# Translate button
translate_button = tk.Button(root, text="Translate", command=translate)
translate_button.grid(row=2, column=1, pady=10)

# Start the GUI event loop
root.mainloop()
