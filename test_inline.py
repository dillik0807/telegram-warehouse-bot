#!/usr/bin/env python
# Тестовый скрипт для проверки inline кнопок

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Создаем inline кнопку
inline_keyboard = [
    [InlineKeyboardButton("📊 Экспорт в Excel", callback_data='export_client_debts')]
]
inline_markup = InlineKeyboardMarkup(inline_keyboard)

print("Inline markup создан успешно:")
print(inline_markup)
print("\nКнопки:")
for row in inline_keyboard:
    for button in row:
        print(f"  - {button.text}: {button.callback_data}")
