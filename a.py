import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Embedding, TimeDistributed
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt  # Importing matplotlib for plotting

# Your existing code...

# Train the model
history = model.fit(X_train, y_train, epochs=10000, validation_data=(X_test, y_test))

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# Plotting the training and validation loss
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plotting the training and validation accuracy
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Function to transliterate text from Latin to Cyrillic
def sequence_to_text(sequence, index_to_char):
    return ''.join(index_to_char[idx] for idx in sequence if idx > 0)

def transliterate(text):
    sequence = pad_sequences([text_to_sequence(text, latin_to_index)], maxlen=max_seq_length, padding='post')
    prediction = model.predict(sequence)
    predicted_sequence = np.argmax(prediction[0], axis=-1)
    return sequence_to_text(predicted_sequence, index_to_cyrillic)

# Define your test inputs
test_texts = [
    "сайн байна уу",
    "баяртай",
    "мэндчилэгээ",
    "сайхан байна уу",
    "шинэ тест",
    "хоол бол хоол",
    "сайн байна уу"
]

# Use the transliterate function to get the outputs
for text in test_texts:
    print(f'wrong Cyrillic: {text}')
    print(f'Cyrillic: {transliterate(text)}')

# Evaluate the model again (unnecessary duplicate code)
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
