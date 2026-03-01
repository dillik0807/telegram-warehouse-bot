"""
Тест для проверки текста кнопок
"""

# Проверяем эмодзи в кнопках
button_text = '📋 Список цен'
print(f"Текст кнопки: '{button_text}'")
print(f"Длина: {len(button_text)}")
print(f"Байты: {button_text.encode('utf-8')}")
print(f"Repr: {repr(button_text)}")

# Проверяем сравнение
test_texts = [
    '📋 Список цен',
    '? Список цен',
    'Список цен',
]

for test in test_texts:
    result = test == button_text
    print(f"\n'{test}' == '{button_text}': {result}")
