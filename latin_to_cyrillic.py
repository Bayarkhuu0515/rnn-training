import tkinter as tk
from tkinter import filedialog, messagebox
import re
import requests
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

import tensorflow as tf
from keras.models import load_model

model = load_model('cyrillic_transliteration_model.h5')
print("Model loaded successfully.")

with open('wrong.txt', 'r') as file:
    lines = file.readlines()
    cyrillic_wrong_texts = [line.strip() for line in lines]
with open('correct.txt', 'r') as file:
    lines = file.readlines()
    cyrillic_texts = [line.strip() for line in lines]

latin_chars = sorted(set(''.join(cyrillic_wrong_texts)))
cyrillic_chars = sorted(set(''.join(cyrillic_texts)))

latin_to_index = {char: idx + 1 for idx, char in enumerate(latin_chars)}
cyrillic_to_index = {char: idx + 1 for idx, char in enumerate(cyrillic_chars)}

index_to_cyrillic = {idx: char for char, idx in cyrillic_to_index.items()}

max_seq_length = max(len(seq) for seq in cyrillic_wrong_texts)

def text_to_sequence(text, char_to_index):
    return [char_to_index.get(char, 0) for char in text]  

def predictWithAi(text):
    words = text.split() 
    transliterated_words = []

    for word in words:
        sequence = text_to_sequence(word, latin_to_index)
        sequence = pad_sequences([sequence], maxlen=max_seq_length, padding='post')
        prediction = model.predict(sequence)
        predicted_sequence = np.argmax(prediction[0], axis=-1)
        transliterated_word = ''.join([index_to_cyrillic.get(idx, '') for idx in predicted_sequence if idx > 0])
        transliterated_words.append(transliterated_word)

    return ' '.join(transliterated_words)


latin_to_cyrillic_simple = {
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'ye': 'е', 'zh': 'ж', 'z': 'з',
    'i': 'и', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п',
    'r': 'р', 's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'h': 'х', 'ts': 'ц', 'ch': 'ч',
    'sh': 'ш', 'e': 'э', 'yu': 'ю', 'ya': 'я', 'yo': 'ё', 'j': 'ж', 'kh' : 'х',
    'w': 'в', 'y':'я'
}

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
            word = word.replace('ё', 'е').replace('ё', 'е')
        elif any(char in 'аоуыАОУ' for char in word):
            word = word.replace('ү', 'у').replace('ү', 'У')
            word = word.replace('о', 'о').replace('О', 'О')

        word = re.sub(r'(?<=[аэиоүуөя])и', 'й', word, flags=re.IGNORECASE)
        word = re.sub(r'(?<=[о])я', 'ё', word, flags=re.IGNORECASE)
        word = re.sub(r'(?<=[өү])я', 'е', word, flags=re.IGNORECASE)

        if any(char in 'аоуАОУ' for char in word):
            word = word.replace('ий', 'ы').replace('ИЙ', 'Ы')
        return word

    words = text.split()
    new_words = [transliterate_word(word) for word in words]
    return ' '.join(new_words)





def hybrid_translation(text):
    text = translate_simple(text)
    print("After simple mapping:", text)
    text = rule_based_transliteration(text)
    print("Wrong:", text)
    text = predictWithAi(text)
    print("after AI transliteration:", text)
    text = rule_based_transliteration(text)
    print("transliteration:", text)
    
    # API call to spellcheck.gov.mn
    response = requests.post(
        "http://spellcheck.gov.mn/scripts/tiny_mce/plugins/spellchecker/rpc.php",
        data={"text": text}
    )
    
    if response.status_code == 200:
        if 'application/json' in response.headers.get('Content-Type', ''):
            try:
                response_data = response.json()
                corrected_text = response_data.get('result', text)
            except ValueError:
                print("Response is not in JSON format")
                corrected_text = text
        else:
            corrected_text = response.text.strip()
    else:
        print(f"API call failed with status code {response.status_code}")
        corrected_text = text
    
    return corrected_text



def translate(event=None):
    latin_text = latin_input.get("1.0", tk.END).strip()
    cyrillic_text = hybrid_translation(latin_text)
    cyrillic_output.delete("1.0", tk.END)
    cyrillic_output.insert(tk.END, cyrillic_text)


root = tk.Tk()
root.title("Latin to Cyrillic Translator")


latin_label = tk.Label(root, text="Latin Text:")
latin_label.pack()
latin_input = tk.Text(root, height=30, width=100)
latin_input.pack()


latin_input.bind('<Return>', translate)

translate_button = tk.Button(root, text="Translate", command=translate)
translate_button.pack()

cyrillic_label = tk.Label(root, text="Cyrillic Text:")
cyrillic_label.pack()
cyrillic_output = tk.Text(root, height=30, width=100)
cyrillic_output.pack()


root.mainloop()
