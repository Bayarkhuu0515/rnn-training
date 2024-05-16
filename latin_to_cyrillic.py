import tkinter as tk
import re

# Simple mapping dictionary for Latin to Cyrillic
latin_to_cyrillic_simple = {
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'zh': 'ж', 'z': 'з',
    'i': 'и', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
    'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х', 'ts': 'ц', 'ch': 'ч',
    'sh': 'ш', 'y': 'ы', 'e': 'э', 'yu': 'ю', 'ya': 'я', 'yo': 'ё', 'j': 'ж', 'kh' : 'х'
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
        return word

    words = text.split()
    new_words = [transliterate_word(word) for word in words]
    return ' '.join(new_words)


# Hybrid translation function
def hybrid_translation(text):
    # Apply simple mapping translation first
    text = translate_simple(text)

    # Apply rule-based transliteration
    text = rule_based_transliteration(text)

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
