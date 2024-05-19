import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

# Load the saved model
model = load_model('cyrillic_transliteration_model.h5')
print("Model loaded successfully.")

# Read the character mappings from the training data files
with open('cyrillwrong.txt', 'r') as file:
    lines = file.readlines()
    cyrillic_wrong_texts = [line.strip() for line in lines]
with open('ugiin_san.txt', 'r') as file:
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

# Function to predict transliteration using the loaded model
def predict(text):
    sequence = text_to_sequence(text, latin_to_index)
    sequence = pad_sequences([sequence], maxlen=max_seq_length, padding='post')
    prediction = model.predict(sequence)
    predicted_sequence = np.argmax(prediction[0], axis=-1)
    return ''.join([index_to_cyrillic.get(idx, '') for idx in predicted_sequence if idx > 0])

# Define your test inputs
test_texts = [
    "саин байна уу",
    "бяртай",
    "мэндчилэгөө",
    "сайхан байна уу",
    "шина тест",
    "хоол бол хоол",
    "сайн байна уу",
    "өндор"
]

# Use the predict function to get the outputs for predefined test texts
print("Predefined test cases:")
for text in test_texts:
    print(f'wrong Cyrillic: {text}')
    print(f'Cyrillic: {predict(text)}')

# Simple interface for custom input
print("\nCustom input transliteration:")
while True:
    custom_text = input("Enter a word or sentence to transliterate (or type 'exit' to quit): ")
    if custom_text.lower() == 'exit':
        break
    print(f'Cyrillic: {predict(custom_text)}')
