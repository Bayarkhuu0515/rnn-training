import tkinter as tk
from tkinter import filedialog, messagebox
import re
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

import tensorflow as tf
from keras.models import load_model

# Load the saved model
model = load_model('cyrillic_transliteration_model.h5')
print("Model loaded successfully.")

# Read the character mappings from the training data files
with open('wrong.txt', 'r') as file:
    lines = file.readlines()
    cyrillic_wrong_texts = [line.strip() for line in lines]
with open('correct.txt', 'r') as file:
    lines = file.readlines()
    cyrillic_texts = [line.strip() for line in lines]

# Create a character mapping, ensuring all unique characters are captured
latin_chars = sorted(set(''.join(cyrillic_wrong_texts)))
cyrillic_chars = sorted(set(''.join(cyrillic_texts)))

latin_to_index = {char: idx + 1 for idx, char in enumerate(latin_chars)}
cyrillic_to_index = {char: idx + 1 for idx, char in enumerate(cyrillic_chars)}

index_to_cyrillic = {idx: char for char, idx in cyrillic_to_index.items()}

max_seq_length = max(len(seq) for seq in cyrillic_wrong_texts)

# Convert text to sequences of integers
def text_to_sequence(text, char_to_index):
    return [char_to_index.get(char, 0) for char in text]  # Use 0 for unknown characters

def predictWithAi(text):
    words = text.split()  # Split the text into individual words
    transliterated_words = []

    for word in words:
        sequence = text_to_sequence(word, latin_to_index)
        sequence = pad_sequences([sequence], maxlen=max_seq_length, padding='post')
        prediction = model.predict(sequence)
        predicted_sequence = np.argmax(prediction[0], axis=-1)
        transliterated_word = ''.join([index_to_cyrillic.get(idx, '') for idx in predicted_sequence if idx > 0])
        transliterated_words.append(transliterated_word)

    return ' '.join(transliterated_words)


# Simple mapping dictionary for Latin to Cyrillic
latin_to_cyrillic_simple = {
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'ye': 'е', 'zh': 'ж', 'z': 'з',
    'i': 'и', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
    'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х', 'ts': 'ц', 'ch': 'ч',
    'sh': 'ш', 'y': 'ы', 'e': 'э', 'yu': 'ю', 'ya': 'я', 'yo': 'ё', 'j': 'ж', 'kh' : 'х',
    'w': 'в'
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

        word = re.sub(r'(?<=[аэиоүуөя])и', 'й', word, flags=re.IGNORECASE)

        if any(char in 'аоуАОУ' for char in word):
            word = word.replace('ий', 'ы').replace('ИЙ', 'Ы')
        return word

    words = text.split()
    new_words = [transliterate_word(word) for word in words]
    return ' '.join(new_words)





# Hybrid translation function
def hybrid_translation(text):
    # Apply simple mapping translation first
    text = translate_simple(text)
    print("After simple mapping:", text)
    # Apply rule-based transliteration
    text = rule_based_transliteration(text)
    print("After rule-based transliteration:", text)
    # Apply AI-based transliteration
    text = predictWithAi(text)
    print("After AI-based transliteration:", text)
    return text

# Function to handle translation and update the GUI
def translate(event=None):
    latin_text = latin_input.get("1.0", tk.END).strip()
    cyrillic_text = hybrid_translation(latin_text)
    cyrillic_output.delete("1.0", tk.END)
    cyrillic_output.insert(tk.END, cyrillic_text)

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


# Start the GUI event loop
root.mainloop()
