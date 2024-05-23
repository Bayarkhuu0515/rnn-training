import tkinter as tk
from tkinter import filedialog, messagebox
import re
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

import tensorflow as tf

# Simple mapping dictionary for Latin to Cyrillic
latin_to_cyrillic_simple = {
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'ye': 'е', 'zh': 'ж', 'z': 'з',
    'i': 'и', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
    'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х', 'ts': 'ц', 'ch': 'ч',
    'sh': 'ш', 'y': 'я', 'e': 'э', 'yu': 'ю', 'ya': 'я', 'yo': 'ё', 'j': 'ж', 'kh' : 'х'
}

# Function for simple mapping translation
def translate_simple(text):
    result = ''
    skip = 0
    for i, char in enumerate(text):
        if skip:
            skip -= 1
            continue
        if i < len(text) - 1 and text[i:i+2].lower() in latin_to_cyrillic_simple:
            cyrillic = latin_to_cyrillic_simple[text[i:i+2].lower()]
            if text[i].isupper():
                cyrillic = cyrillic.upper()
            result += cyrillic
            skip = 1
        else:
            cyrillic = latin_to_cyrillic_simple.get(char.lower(), char)
            if char.isupper():
                cyrillic = cyrillic.upper()
            result += cyrillic
    return result

def rule_based_transliteration(text):
    def transliterate_word(word):
        if any(char in 'эиөЭИӨ' for char in word):
            word = word.replace('у', 'ү').replace('У', 'Ү')
            word = word.replace('о', 'ө').replace('О', 'Ө')
        elif any(char in 'аоуАОУ' for char in word):
            word = word.replace('у', 'у').replace('У', 'У')
            word = word.replace('о', 'о').replace('О', 'О')

        word = re.sub(r'(?<=[аэиоүуө])и', 'й', word, flags=re.IGNORECASE)

        if any(char in 'аоуАОУ' for char in word):
            word = word.replace('ий', 'ы').replace('ИЙ', 'Ы')

        return word

    words = text.split()
    new_words = [transliterate_word(word) for word in words]
    return ' '.join(new_words)

# Hybrid translation function
def hybrid_translation(text):
    words = re.split(r'(\s+)', text)  # Split text by spaces and keep the delimiters
    translated_words = []
    for word in words:
        if word.strip():  # If the word is not just whitespace
            word = translate_simple(word)
            word = rule_based_transliteration(word)
        translated_words.append(word)
    return ''.join(translated_words)

# Function to handle translation and update the GUI
def translate(event=None):
    latin_text = latin_input.get("1.0", tk.END).strip()
    cyrillic_text = hybrid_translation(latin_text)
    cyrillic_output.delete("1.0", tk.END)
    cyrillic_output.insert(tk.END, cyrillic_text)

# Function to handle file-based translation
def translate_file():
    input_file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not input_file_path:
        return

    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if not output_file_path:
        return

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            latin_text = f.read().strip()
            cyrillic_text = hybrid_translation(latin_text)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(cyrillic_text)

        messagebox.showinfo("Success", "Translation completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Set up the GUI
root = tk.Tk()
root.title("Latin to Cyrillic Translator")

# Latin input text area
latin_label = tk.Label(root, text="Latin Text:")
latin_label.pack()
latin_input = tk.Text(root, height=10, width=50)
latin_input.pack()

# Bind the Enter key to the translate function
latin_input.bind('<Return>', translate)

# Translate button
translate_button = tk.Button(root, text="Translate", command=translate)
translate_button.pack()

# Cyrillic output text area
cyrillic_label = tk.Label(root, text="Cyrillic Text:")
cyrillic_label.pack()
cyrillic_output = tk.Text(root, height=10, width=50)
cyrillic_output.pack()

# File translation button
file_translate_button = tk.Button(root, text="Translate File", command=translate_file)
file_translate_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
