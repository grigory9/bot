import telebot
import sqlite3
import random
import time

from telebot import *
from config import *
from button import *
from get_text import *


bot = telebot.TeleBot(token = token, parse_mode = 'html')

@bot.message_handler(commands = ['start'])
def welcome(message):
	if message.chat.type == 'private':
		connect_start = sqlite3.connect('data.db',check_same_thread = False)
		cursor_start = connect_start.cursor()

		cursor_start.execute("""CREATE TABLE IF NOT EXISTS users (
			id INTEGER,
			username TEXT,
			ref TEXT
		)""")
		connect_start.commit()

		cursor_start.execute("""CREATE TABLE IF NOT EXISTS surveys (
			id_survey INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT,
			link TEXT
		)""")
		connect_start.commit()

		cursor_start.execute("""CREATE TABLE IF NOT EXISTS op (
			id_channel TEXT
		)""")
		connect_start.commit()

		cursor_start.execute(f"SELECT id FROM users WHERE id = '{message.chat.id}'")
		data = cursor_start.fetchone()
		if data is None:
			us_id = message.chat.id
			us_username = message.from_user.username
			ref = 'None'

			cursor_start.execute(f"INSERT INTO users (id, username, ref) VALUES ('{us_id}', '{us_username}', '{ref}')")
			connect_start.commit()

		full_text = message.text
		se = 'survey'

		if se in full_text:
			#text = message.text
			new_text = full_text.replace('/start survey_', '')
			print(new_text)

			cursor_start.execute(f"SELECT name FROM surveys WHERE id_survey = '{new_text}'")
			name_survey = cursor_start.fetchone()[0]

			cursor_start.execute(f"SELECT link FROM surveys WHERE id_survey = '{new_text}'")
			link_survey = cursor_start.fetchone()[0]

			look = types.InlineKeyboardMarkup()
			webAppTest = types.WebAppInfo(link_survey)
			i1 = types.InlineKeyboardButton(text = '⚡ Пройти тест', web_app = webAppTest)
			look.add(i1)

			bot.send_message(message.chat.id, f'<b>✨ Что бы пройти тест <i>{name_survey}</i> нажмите на кнопку.</b>', reply_markup = look)
		else:
			text = open(hello_path, 'r')
			bot.copy_message(message.chat.id, admin, text.read(), reply_markup = start_menu)


@bot.message_handler(commands = ['admin'])
def adminka(message):
	if message.chat.id == admin:
		bot.reply_to(message, '<b>Админ меню открыто.</b>', reply_markup = admin_menu)


@bot.message_handler(content_types = ['text'])
def content(message):
	if message.chat.type == 'private':
		if message.text == '🎲 Рандомный тест':
			connect_game = sqlite3.connect('data.db', check_same_thread = False)
			cursor_game = connect_game.cursor()

			cursor_game.execute("SELECT id_survey FROM surveys ORDER BY RANDOM() LIMIT 1")
			data = cursor_game.fetchone()[0]
			print(data)

			cursor_game.execute(f"SELECT name FROM surveys WHERE id_survey = '{data}'")
			name_survey = cursor_game.fetchone()[0]
			print(name_survey)

			cursor_game.execute(f"SELECT link FROM surveys WHERE id_survey = '{data}'")
			link_survey = cursor_game.fetchone()[0]
			print(link_survey)

			look = types.InlineKeyboardMarkup()
			webAppTest = types.WebAppInfo(link_survey)
			i1 = types.InlineKeyboardButton(text = '⚡ Пройти тест', web_app = webAppTest)
			look.add(i1)

			bot.reply_to(message, f"🎊 <b>Случайный тест</b>\n<b>❇ Название</b>: {name_survey}", reply_markup = look, disable_web_page_preview = True)

		#Админская часть бота
		elif message.text == '📊 Статистика бота':
			if message.chat.id == admin:
				connect_stat_people = sqlite3.connect('data.db',check_same_thread = False)
				cursor_stat_people = connect_stat_people.cursor()

				cursor_stat_people.execute("SELECT COUNT(*) FROM users")
				count_users = cursor_stat_people.fetchone()[0]

				cursor_stat_people.execute("SELECT COUNT(*) FROM surveys")
				count_anime = cursor_stat_people.fetchone()[0]

				bot.send_message(message.chat.id, f'📊 <b>Статистика бота @{bot.get_me().username}</b>\n◉ Живых участников: {count_users}\n◉ Всего опросов добавлено: {count_anime}', reply_markup = d_key)

		elif message.text == 'ОП 🔐':
			if message.chat.id == admin:
				msg = bot.send_message(message.chat.id, '<b>Что делаем ? 🤔</b>.', reply_markup = opka)
				bot.register_next_step_handler(msg, opka_1)

		elif message.text == '🀄️ Добавить опрос':
			if message.chat.id == admin:
				msg = bot.reply_to(message, '<b>Первым делом отправьте название для опроса.</b>', reply_markup = back)
				bot.register_next_step_handler(msg, add_survey)

		elif message.text == 'Рассылка 📨':
			if message.chat.id == admin:
				msg = bot.reply_to(message, '<b>Выберите тип рассылки.</b>', reply_markup = t_r)
				bot.register_next_step_handler(msg, tip_rass)

		elif message.text == '⚙️ Настройка бота':
			if message.chat.id == admin:
				msg = bot.reply_to(message, '<b>Что делаем ?</b>', reply_markup = setting_menu)
				bot.register_next_step_handler(msg, set_bot)

		elif message.text == '🚫 Выйти из админки':
			if message.chat.id == admin:
				bot.reply_to(message, '<b>Админ меню успешно закрыто.</b>', reply_markup = d_key)
def set_bot(message):
	if message.text == '❌ Выход':
		bot.reply_to(message, '<b>Вы успешно отменили действие.</b>', reply_markup = admin_menu)

	elif message.text == '✨ Изменить приветствие':
		msg = bot.reply_to(message, '<b>Отправьте новое приветствие.</b>')
		bot.register_next_step_handler(msg, edit_hello)

def edit_hello(message):
	if message.text == 'Отменить':
		bot.send_message(message.chat.id, 'Отменено 😥', reply_markup = d_key )

	else:
		text = message.message_id
		fa = open(hello_path, 'w', encoding = 'UTF-8')
		fa.write(str(text))
		fa.close()
		bot.send_message(message.chat.id, 'Успешно изменено. ✅', reply_markup = d_key)

#Рассылка
def tip_rass(message):
	if message.text == 'Перессылка | ПРЕМ ЭМОДЗИ, ОДНО ФОТО':
		msg = bot.send_message(message.chat.id, 'Отправьте пост для рассылки', reply_markup = back)
		bot.register_next_step_handler(msg, peressilka)

	elif message.text == 'Копирование | БЕЗ ПРЕМ, ОДНО ФОТО':
		msg = bot.send_message(message.chat.id, 'Отправьте пост для рассылки', reply_markup = back)
		bot.register_next_step_handler(msg, copy_post)

#Перессылка поста
def peressilka(message):
	connect_per = sqlite3.connect('data.db', check_same_thread = False)
	cursor_per = connect_per.cursor()

	if message.text == 'Отменить':
		bot.send_message(message.chat.id, 'Отменено', reply_markup = d_key)

	else:
		cursor_per.execute('SELECT id FROM users')
		result = cursor_per.fetchall()
		i = 0
		b = 0
		bot.send_message(message.chat.id, '<b>Начинаю делать рассылку, после окончания вы получите статистику</b> 🧸', parse_mode = 'html' ,reply_markup = d_key)
		try:
			for x in result:
				try:
					i += 1
					bot.forward_message(int(x[0]), message.chat.id, message.message_id)
					#print(f'ID: {x[0]} | Успешно получил сообщение.')
				except telebot.apihelper.ApiTelegramException as err:
					i -= 1
					b += 1
					if 'retry after' in str(err).lower():
						retry_after = int(str(err).split('retry after ')[1])
						bot.send_message(admin, f'Упc, ограничения телеграмма. Ждем {retry_after} секунд.')
						#print(f'Упc, ограничения телеграмма. Ждем {retry_after} секунд.')
						time.sleep(retry_after)
		finally:
			#cursor.close()
			pass
		bot.send_message(admin, f'Статистика по рассылке\n\nУспешно: {i}\nПровалов: {b}', reply_markup = d_key)

@bot.message_handler(commands = ['del'])
def delete_qu(message):
    if message.chat.id == admin:
        text = message.text
        finaly_text = text.replace('/del ', '')

        connect_del_qu = sqlite3.connect('data.db', check_same_thread = False)
        cursor_del_qu = connect_del_qu.cursor()
        cursor_del_qu.execute(f"DELETE FROM surveys WHERE id_survey = '{finaly_text}'")
        connect_del_qu.commit()
        bot.reply_to(message, "Succes delete")

#Копирование поста
def copy_post(message):
	connect_copy = sqlite3.connect('data.db', check_same_thread = False)
	cursor_copy = connect_copy.cursor()

	if message.text == 'Отменить':
		bot.send_message(message.chat.id, 'Отменено', reply_markup = d_key)

	else:
		cursor_copy.execute('SELECT id FROM users')
		result = cursor_copy.fetchall()

		chat_id = message.chat.id
		message_id = message.message_id

		i = 0
		b = 0
		bot.send_message(message.chat.id, '<b>Начинаю делать рассылку, после окончания вы получите статистику</b> 🧸', parse_mode = 'html' ,reply_markup = d_key)
		try:
			for x in result:
				try:
					i += 1
					original_message = bot.copy_message(int(x[0]), admin,  message_id, reply_markup=message.reply_markup)
					print(f'ID: {x[0]} | Успешно получил сообщение.')
				except telebot.apihelper.ApiTelegramException as err:
					i -= 1
					b += 1
					if 'retry after' in str(err).lower():
						retry_after = int(str(err).split('retry after ')[1])
						print(f'Упc, огроничения телеграмма. Ждем {retry_after} секунд.')
						time.sleep(retry_after)
		finally:
			pass

		bot.send_message(admin, f'Статистика по рассылке\n\nУспешно: {i}\nПровалов: {b}', reply_markup = d_key)


#Добавлние опросов
def add_survey(message):
	if message.text == 'Отменить':
		bot.reply_to(message, '<b>Добавление опроса отменено</b>', reply_markup = admin_menu)
	else:
		global name_survey
		name_survey = message.text

		msg = bot.reply_to(message, '<b>Отправь ссылку на опрос.</b>')
		bot.register_next_step_handler(msg, add_survey2)

def add_survey2(message):
    if message.text == 'Отменить':
        bot.reply_to(message, '<b>Добавление опроса отменено</b>', reply_markup = admin_menu)
    else:
        global link_survey
        link_survey = message.text

        connect_addsurvey = sqlite3.connect('data.db',check_same_thread = False)
        cursor_addsurvey = connect_addsurvey.cursor()
        cursor_addsurvey.execute("SELECT link FROM surveys WHERE link = '{link_survey}'")
        data = cursor_addsurvey.fetchone()[0]
        if data is None:

            #cursor_addsurvey.execute(f"""INSERT INTO table_name (name, link) VALUES ("{name_survey}" , "{link_survey}")""")
            cursor_addsurvey.execute(f"""INSERT INTO surveys(name, link) VALUES ("{name_survey}" , "{link_survey}")""")
            connect_addsurvey.commit()

            bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEJqqFkrlPbU6hYLDXodamV9_-4PNnlWQACfQsAAuQkGVDyfE-NPj2zKC8E')

            cursor_addsurvey.execute(f"SELECT id_survey FROM surveys WHERE link = '{link_survey}'")
            data = cursor_addsurvey.fetchone()[0]

            bot.reply_to(message, f'⚡️ <b>Опрос успешно добавлен.\n\nId: {data}🔗 Ссылка на опрос</b>: https://t.me/{bot.get_me().username}?start=survey_{data}', reply_markup = admin_menu, disable_web_page_preview = True)
        else:
            cursor_addsurvey.execute("SELECT name FROM surveys WHERE link = '{link_survey}'")
            name_repeat = cursor_addsurvey.fetchone()[0]

            bot.reply_to(message, f'Данный опрос уже добавлен.\nНазвание: {name_repeat}\nСсылка: {link_survey}')

#Все что связано с ОП
def opka_1(message):
	if message.text == '➕ Добавить канал':
		msg = bot.send_message(message.chat.id, 'Отправьте ID канала начинаю с -100\n\nПолучить ID тут: @getmyid_bot', reply_markup = back)
		bot.register_next_step_handler(msg, op_add)

	elif message.text == '➖ Убрать канал':
		msg = bot.send_message(message.chat.id, 'Отправьте ID канала начинаю с -100\n\nПолучить ID тут: @getmyid_bot', reply_markup = back)
		bot.register_next_step_handler(msg, del_op)

	elif message.text == '⛏ Изменить текст':
		#text = open(op_path, 'r', encoding = 'UTF-8')
		#bot.send_message(message.chat.id, text.read())
		msg = bot.send_message(message.chat.id, 'Введите текст для изменения.', reply_markup = back)
		bot.register_next_step_handler(msg, op_text)

	elif message.text == '🗑 Удалить все ОП':
		cursor_op1.execute("DELETE FROM op")
		connect_op1.commit()

		bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEJqqFkrlPbU6hYLDXodamV9_-4PNnlWQACfQsAAuQkGVDyfE-NPj2zKC8E')
		bot.send_message(message.chat.id, '✅ <b>Успешно добавлено</b>', reply_markup = d_key)

def del_op(message):
	#try:
	connect_op2 = sqlite3.connect('data.db', check_same_thread = False)
	cursor_op2 = connect_op2.cursor()
	if message.text == 'Отменить':
		bot.send_message(message.chat.id, 'Отменено.\n/start - запустить бота как обычно\n/admin - открыть админ-панель', reply_markup = d_key)

	else:
		del_id = message.text
		cursor_op2.execute("DELETE FROM op WHERE id = ?", (del_id,))
		connect_op2.commit()
		bot.reply_to(message, "Успешно", reply_markup = d_key)
	#except:
		##print('Ошибка')

def op_text(message):
	if message.text == 'Отменить':
		bot.send_message(message.chat.id, 'Отменено.\n/start - запустить бота как обычно\n/admin - открыть админ-панель', reply_markup = d_key)

	else:
		#Редактирование оп
		text = message.message_id
		fa = open(op_path, 'w', encoding = 'UTF-8')
		fa.write(str(text))
		fa.close()
		bot.send_message(message.chat.id, 'Успешно изменено. Для проверки начните диалог с ботом /start', reply_markup = d_key)

def op_add(message):
	connect_op3 = sqlite3.connect('data.db', check_same_thread = False)
	cursor_op3 = connect_op3.cursor()

	if message.text == 'Отменить':
		bot.send_message(message.chat.id, 'Отменено.\n/start - запустить бота как обычно\n/admin - открыть админ-панель', reply_markup = d_key)

	else:
		id_op = message.text
		cursor_op3.execute("""CREATE TABLE IF NOT EXISTS op(
			ch_id TEXT
		)""")
		connect_op3.commit()

		cursor_op3.execute(f"""INSERT INTO op VALUES ("{id_op}")""")
		connect_op3.commit()

		bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAEJqqFkrlPbU6hYLDXodamV9_-4PNnlWQACfQsAAuQkGVDyfE-NPj2zKC8E')
		bot.send_message(message.chat.id, '✅ <b>Успешно добавлено</b>', reply_markup = d_key)


bot.infinity_polling()
