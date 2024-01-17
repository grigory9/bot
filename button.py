from telebot import types

start_menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
i1 = types.KeyboardButton("🎲 Рандомный тест")
start_menu.add(i1)

admin_menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
i1 = types.KeyboardButton('📊 Статистика бота')
i2 = types.KeyboardButton('ОП 🔐')
i3 = types.KeyboardButton('🀄️ Добавить опрос')
i4 = types.KeyboardButton('Рассылка 📨')
i5 = types.KeyboardButton('⚙️ Настройка бота')
i6 = types.KeyboardButton('🚫 Выйти из админки')
admin_menu.add(i1, i2)
admin_menu.add(i3, i4)
admin_menu.add(i5)
admin_menu.add(i6)

d_key = (types.ReplyKeyboardRemove())

opka = types.ReplyKeyboardMarkup(resize_keyboard = True)
i1 = types.KeyboardButton('➕ Добавить канал')
i2 = types.KeyboardButton('➖ Убрать канал')
i3 = types.KeyboardButton('⛏ Изменить текст')
i4 = types.KeyboardButton('🗑 Удалить все ОП')
opka.add(i1)
opka.add(i2)
opka.add(i3)
opka.add(i4)

setting_menu = types.ReplyKeyboardMarkup(resize_keyboard = True)
i1 = types.KeyboardButton('✨ Изменить приветствие')
i2 = types.KeyboardButton('❌ Выход')
setting_menu.add(i1)
setting_menu.add(i2)


back = types.ReplyKeyboardMarkup(resize_keyboard = True)
i1 = types.KeyboardButton('Отменить')
back.add(i1)

foll = types.InlineKeyboardMarkup()
i1 = types.InlineKeyboardButton(text = 'Я подписался ✅', callback_data = 'check_foll')
foll.add(i1)

#Тип рассылки
t_r = types.ReplyKeyboardMarkup(resize_keyboard = True)
i1 = types.KeyboardButton('Перессылка | ПРЕМ ЭМОДЗИ, ОДНО ФОТО')
i2 = types.KeyboardButton('Копирование | БЕЗ ПРЕМ, ОДНО ФОТО')
t_r.add(i1)
t_r.add(i2)
