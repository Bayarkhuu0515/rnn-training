import tkinter as tk
from tkinter import filedialog, messagebox
import re
import requests
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import asyncio
import tensorflow as tf
from keras.models import load_model
import json
import threading

import requests
import json

async def check_spelling_with_api_and_save_to_file(words:str):
    print('API CALLED')
    url = "https://api.bolor.net/v1.2/spell-check-short"
    headers = {
        "Content-Type": "text/plain",
        "token": "a3596f7deb1d4e297844c9bcb61956f9327c6e27338db7302ee98551db7495a4"
    }

    # Join the list of words into a single string
    response = requests.post(url, data=words.encode('utf-8'), headers=headers)
    print("API ашиглан боловсруулж буй хариу:")
    print(response)
    print("API төвөл")
    print(response.status_code)

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        # Хэрэв хүсэлт амжилтгүй болвол хоосон жагсаалт буцаана
        return []

    try:
        # JSON хариуг дараалал болгож авах
        
        incorrects = response.json()
        print('Буруу үгс:')
        print(response.json())
        
        # Хэрэв алдаатай үг байвал файлд хадгална
        with open("wrong.txt", "a+", encoding="utf-8") as file:
            # Move the cursor to the end of the file
            file.seek(0, 2)
    
            # Check if the file is not empty
            if file.tell() > 0:
                # Add a newline if the file is not empty
                file.write("\n")
    
            # Iterate over each word in the incorrects list
            for word in incorrects:
                # Write the word followed by a newline character to the file
                file.write(f"{word}\n")
                
        return incorrects
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        # Хэрэв алдаа гарвал хоосон жагсаалт буцаана
        return []

# Example usage
words_to_check = "Монгол улсын их сургууль mонгал"
spell_check_result = check_spelling_with_api_and_save_to_file(words_to_check)
print(spell_check_result)



async def correct_word_using_api_and_save_to_correct(word: str):
    url = "https://api.bolor.net/v1.2/spell-suggest"
    headers = {
        "Content-Type": "text/plain",
        "token": "793a95e0565331fa79994e4ea83bedf07823445fe94dc95c968a208dcca0e094"
    }
    data = word.encode('utf-8')
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        # add the correct word to the correct.txt file
        with open("correct.txt", "a+", encoding="utf-8") as file:
            file.seek(0, 2)
            if file.tell() > 0:
                file.write("\n")
            file.write(response.json())

        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return ''



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





async def hybrid_translation(text):
    text = translate_simple(text)
    print("After simple mapping:", text)
    text = rule_based_transliteration(text)
    print("Wrong:", text)
    text = predictWithAi(text)
    print("after AI transliteration:", text)
    text = rule_based_transliteration(text)
    print("transliteration:", text)
    # 
    wrongWordList = await check_spelling_with_api_and_save_to_file(text)
    
    # алдаатай үгүүдийг засах api дуудалт
    # if(len(wrongWordList) > 0):
    #     for word in wrongWordList:
    #         # алдаатай үгүүдийг api ашиглан засах
    #         await correct_word_using_api_and_save_to_correct(word)
    return text



async def translate(event=None):
    latin_text = latin_input.get("1.0", tk.END).strip()
    cyrillic_text = await hybrid_translation(latin_text)
    cyrillic_output.delete("1.0", tk.END)
    cyrillic_output.insert(tk.END, cyrillic_text)

# Wrapper to run the async function
def run_translate():
    asyncio.run_coroutine_threadsafe(translate(), loop)

# Function to run the asyncio event loop in a separate thread
def start_asyncio_event_loop():
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Create and start a thread running the asyncio event loop

threading.Thread(target=start_asyncio_event_loop, daemon=True).start()


root = tk.Tk()
root.title("Latin to Cyrillic Translator")


latin_label = tk.Label(root, text="Latin Text:")
latin_label.pack()
latin_input = tk.Text(root, height=30, width=100)
latin_input.pack()


latin_input.bind('<Return>', lambda event:run_translate())

translate_button = tk.Button(root, text="Translate", command=run_translate)
translate_button.pack()

cyrillic_label = tk.Label(root, text="Cyrillic Text:")
cyrillic_label.pack()
cyrillic_output = tk.Text(root, height=30, width=100)
cyrillic_output.pack()


root.mainloop()
