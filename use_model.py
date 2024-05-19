

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
