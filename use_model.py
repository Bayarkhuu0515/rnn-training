from keras.models import load_model

# returns a compiled model
# identical to the previous one
model = load_model('my_model.h5')

with open('cyrillwrong.txt', 'r') as file:
    lines = file.readlines()
    cyrillic_wrong_texts = [line.strip() for line in lines]
with open('ugiin_san.txt', 'r') as file:
    lines = file.readlines()
    cyrillic_texts = [line.strip() for line in lines]

# Create a character mapping, ensuring all unique characters are captured
latin_chars = sorted(set(''.join(cyrillic_wrong_texts)))
cyrillic_chars = sorted(set(''.join(cyrillic_texts)))
