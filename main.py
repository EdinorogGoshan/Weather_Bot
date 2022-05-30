from config import weather_token
from telebot import types
from MenuBot import Menu
import datetime
import requests
import telebot
import config

bot = telebot.TeleBot(config.tg_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    text_message = f'Привет, {message.from_user.first_name}!\nВыбери желаемое действие.'
    bot.send_message(message.chat.id, text=text_message, reply_markup=Menu.getMenu('Главное меню').markup)


@bot.message_handler(content_types=['text'])
def get_messages(message):
    chat_id = message.chat.id
    ms_text = message.text
    result = goto_menu(chat_id, ms_text)

    if result is True:
        return

    if Menu.cur_menu is not None and ms_text in Menu.cur_menu.buttons:
        if ms_text == 'Помощь':
            send_help(chat_id)

        if ms_text == 'Погода':
            enter = bot.send_message(chat_id, text='Введите название города:')
            bot.register_next_step_handler(enter, get_weather)

        elif ms_text == 'Да или Нет':
            bot.send_animation(chat_id, animation=yes_or_no(message))


def goto_menu(chat_id, name_menu):
    if name_menu == "Выход" and Menu.cur_menu is not None and Menu.cur_menu.parent is not None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)

    if target_menu is not None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        if target_menu.name == 'Развлечения':
            return True
    else:
        return False


def yes_or_no(message):
    ans_data = {
        'yes': 'Да \U0001F44D',
        'no': 'Нет \U0001F44E',
        'maybe': 'Может быть \U0001F937'
    }

    url = ''
    req = requests.get('https://yesno.wtf/api')

    if req.status_code == 200:
        data_json = req.json()
        url = data_json['image']
        answer = data_json['answer']
        if answer in ans_data:
            ans = ans_data[answer]
            bot.send_message(message.chat.id, text=ans)
    return url


def get_weather(message):
    chat_id = message.chat.id
    ms_text = message.text

    smiles_data = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    if ms_text == 'Выход':
        goto_menu(chat_id, 'Главное меню')

    else:
        req = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={ms_text}&appid={weather_token}&units=metric&lang=rus')
        if req.status_code == 200:
            data = req.json()

            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            speed = data['wind']['speed']
            sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
            sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            day_length = sunset - sunrise

            w_description = data['weather'][0]['main']
            if w_description in smiles_data:
                description = smiles_data[w_description]
            else:
                description = 'Не могу понять что за погода!'

            text_data = (f'Погода в городе: {ms_text}\n'
                         f'Температура: {temp} С° {description}\n'
                         f'Ощущается как: {feels_like} С°\n'
                         f'Влажность: {humidity}%\n'
                         f'Скорость ветра: {speed} м/с\n'
                         f'Восход: {sunrise}\n'
                         f'Закат: {sunset}\n'
                         f'Продолжительность дня: {day_length}')

            bot.send_message(chat_id, text=text_data)


def send_help(chat_id):
    bot.send_message(chat_id, "Автор: Комар Виктория")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/Little_Dirty_Snake")
    markup.add(btn1)
    img = open('photo.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)


bot.polling(none_stop=True, interval=0)
