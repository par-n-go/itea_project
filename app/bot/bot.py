from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import random
from app.models.models import Category

TOKEN = '1277024755:AAG9C8JXFTbeITCZn8wQ9wIqPm6ngPcysRM'
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_greetings(message):
    kb = InlineKeyboardMarkup()
    categories = Category.objects()
    button_list = []
    for category in categories:
        cat_button = InlineKeyboardButton(text=category.title, callback_data=f'cat={category.title}')
        kb.add(cat_button)
    greetings_list = ['Hi!', 'Привет!', 'Добро пожаловать!', 'Рад Вас приветствовать!']
    reply_text = str(random.choice(greetings_list)) + '\nВыберите категорию из списка ниже:'
    bot.send_message(
        message.chat.id,
        reply_text,
        reply_markup=kb
    )


@bot.callback_query_handler(lambda x: 'cat=' in x.data)
def category_callback(call):
    #print (call)
    description = Category.objects.get(title=call.data[4:]).description
    bot.send_message(call.from_user.id, description)


@bot.message_handler(commands=['create_category'])
def create_category(message):
    category={
        'title':'Планшеты',
        'description':'Здесь представлены планшеты'
    }
    user_obj = Category.objects.create(**category)
    category = {
        'title': 'Компьютеры',
        'description': 'Здесь представлены компьютеры'
    }
    user_obj = Category.objects.create(**category)
    bot.send_message(message.chat.id, 'Категория создана!')


bot.polling()