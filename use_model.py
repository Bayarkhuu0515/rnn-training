import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the saved model
model = tf.keras.models.load_model('cyrillic_transliteration_model.h5')
print("Model loaded successfully.")

# Character mappings from the previous training script
latin_chars = sorted(set(''.join([
    "саин баина уу", "баяртай", "мэндчилэгээ", "саихан баина уу", "шинэ тест",
    "хоол бол хоол", "сайн байна уу", "Зандэн", "өндэг"
])))
cyrillic_chars = sorted(set(''.join([
    "сайн байна уу", "баяртай", "мэндчилэгээ", "сайхан байна уу", "шинэ тест",
    "хоол бол хоол", "сайн байна уу", "Зандaн", "өндөг"
])))

latin_to_index = {char: idx + 1 for idx, char in enumerate(latin_chars)}
cyrillic_to_index = {char: idx + 1 for idx, char in enumerate(cyrillic_chars)}

index_to_cyrillic = {idx: char for char, idx in cyrillic_to_index.items()}

max_seq_length = max(len(seq) for seq in ["саин баина уу", "баяртай", "мэндчилэгээ", "саихан баина уу", "шинэ тест", "хоол бол хоол", "сайн байна уу", "Зандэн", "өндэг"])

# Convert text to sequences of integers
def text_to_sequence(text, char_to_index):
    return [char_to_index[char] for char in text if char in char_to_index]

# Function to transliterate text from Latin to Cyrillic
def sequence_to_text(sequence, index_to_char):
    return ''.join(index_to_char[idx] for idx in sequence if idx > 0)

def transliterate(text):
    sequence = pad_sequences([text_to_sequence(text, latin_to_index)], maxlen=max_seq_length, padding='post')
    prediction = model.predict(sequence)
    predicted_sequence = np.argmax(prediction[0], axis=-1)
    return sequence_to_text(predicted_sequence, index_to_cyrillic)

# Define your custom test inputs
custom_texts = [
    "саин баина уу",
    "хоол бол хоол",
    "шинэ тест"
]

# Use the transliterate function to get the outputs
for text in custom_texts:
    print(f'wrong Cyrillic: {text}')
    print(f'Cyrillic: {transliterate(text)}')
