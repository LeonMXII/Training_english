import os
import telebot
import random


from telebot import types, StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
token = os.getenv("token")
TOKEN = token
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)

buttons = []
secret_words = {}
new_users = []
users = {}

def show_hint(*lines):
    return '\n'.join(lines)

def show_target(data):
    return f"{data['word']} -> {data['word_ru']}"

class Command:
    ADD_WORD = 'Добавить слово 🤬'
    DELETE_WORD = 'Удалить слово🚽'
    NEXT = 'Дальше 🙄'


class MyStates(StatesGroup):
    word = State()
    word_ru = State()
    another_words = State()

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.send_message(message.chat.id, "Привет! Я буду обучать тебя английскому!")

@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):
    cid = message.chat.id
    if cid not in new_users:
        new_users.append(cid)
        users[cid] = 0
        bot.send_message(cid, "Привет! Я обучающий бот! Хочу обучить тебя базовым словам английского языка")
    markup = types.ReplyKeyboardMarkup(row_width=2)

    global buttons
    buttons = []
    target_word = 'Peace'  # брать из БД
    translate = 'Мир'  # брать из БД
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    others = ['Green', 'White', 'Hello', 'Car']  # брать из БД
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others



if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling()



