import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Embedding, TimeDistributed
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

pyo.init_notebook_mode() # Initialize Plotly





# Read the .svc file
# df = pd.read_csv('words.svc', sep=';', header=None, names=['wrongwords ', 'correctwords'])
# Create dummy data for wrong and correct Cyrillic texts
cyrillic_wrong_texts = [
    "саин баина уу",
    "баяртай",
    "мэндчилэгээ",
    "саихан баина уу",
    "шинэ тест",
    "хоол бол хоол",
    "сайн байна уу",
    "Зандэн",
    "өндэг",
]
cyrillic_texts = [
    "сайн байна уу",
    "баяртай",
    "мэндчилэгээ",
    "сайхан байна уу",
    "шинэ тест",
    "хоол бол хоол",
    "сайн байна уу",
    "Зандaн",
    "өндөг",
]

# Extract the wrong and correct Cyrillic texts
cyrillic_wrong_texts = cyrillic_wrong_texts
# df['wrongwords'].tolist()
cyrillic_texts = cyrillic_texts
# df['correctwords'].tolist()

# Create a character mapping, ensuring all unique characters are captured
latin_chars = sorted(set(''.join(cyrillic_wrong_texts)))
cyrillic_chars = sorted(set(''.join(cyrillic_texts)))

latin_to_index = {char: idx + 1 for idx, char in enumerate(latin_chars)}
cyrillic_to_index = {char: idx + 1 for idx, char in enumerate(cyrillic_chars)}

index_to_cyrillic = {idx: char for char, idx in cyrillic_to_index.items()}

max_seq_length = max(len(seq) for seq in cyrillic_wrong_texts)

# Convert text to sequences of integers
def text_to_sequence(text, char_to_index):
    return [char_to_index[char] for char in text if char in char_to_index]

X = [text_to_sequence(text, latin_to_index) for text in cyrillic_wrong_texts]
y = [text_to_sequence(text, cyrillic_to_index) for text in cyrillic_texts]

X = pad_sequences(X, maxlen=max_seq_length, padding='post')
y = pad_sequences(y, maxlen=max_seq_length, padding='post')

X = np.array(X)
y = np.array(y)

# Reshape y for RNN output
y = np.expand_dims(y, -1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the RNN model
vocab_size_latin = len(latin_chars) + 1
vocab_size_cyrillic = len(cyrillic_chars) + 1
embedding_dim = 64
rnn_units = 128

model = Sequential()
model.add(Embedding(input_dim=vocab_size_latin, output_dim=embedding_dim))
model.add(SimpleRNN(rnn_units, return_sequences=True))
model.add(TimeDistributed(Dense(vocab_size_cyrillic, activation='softmax')))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Train the model
history = model.fit(X_train, y_train, epochs=1000, validation_data=(X_test, y_test))



# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')


# Plotting the training and validation loss using Plotly
# Plotting the training and validation loss using Plotly in offline mode
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(range(len(history.history['loss']))), y=history.history['loss'], mode='lines', name='Training Loss'))
fig.add_trace(go.Scatter(x=list(range(len(history.history['val_loss']))), y=history.history['val_loss'], mode='lines', name='Validation Loss'))
fig.update_layout(title='Model Loss', xaxis_title='Epoch', yaxis_title='Loss')
pyo.plot(fig, filename='loss_plot.html')  # This will create an HTML file and open it in the default web browser


# Plotting the training and validation accuracy using Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(range(len(history.history['accuracy']))), y=history.history['accuracy'], mode='lines', name='Training Accuracy'))
fig.add_trace(go.Scatter(x=list(range(len(history.history['val_accuracy']))), y=history.history['val_accuracy'], mode='lines', name='Validation Accuracy'))
fig.update_layout(title='Model Accuracy', xaxis_title='Epoch', yaxis_title='Accuracy')
fig.show()

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
    "сайн байна уу",
    "өндөр"
]

# Use the transliterate function to get the outputs
for text in test_texts:
    print(f'wrong Cyrillic: {text}')
    print(f'Cyrillic: {transliterate(text)}')




# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
