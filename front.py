import telebot
import logging
#from pprint import pprint

bot = telebot.TeleBot("")
group_id = ...

user_data = {}

#import pickle




class User:
    def __init__(self, first_name, user_name):
        self.first_name = first_name
        self.course = ''
        self.username = user_name
        self.passed_captcha = False

logger = telebot.logger  # set logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.


@bot.message_handler(commands=['help', 'about'])
def helper(message):
    if(message.chat.id not in user_data):
        bot.send_message(message.chat.id, "Я бот, который зарегистрирует вас, а потом вам придёт два ника в телеграме, кто сделал также.")
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрировались, ждите письма через неделю. Если что-то пошло не так, пишите Ладе @OrangeLine")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if(message.chat.id not in user_data):
        msg = bot.send_message(message.chat.id, "Напишите свои имя и фамилию")
        bot.register_next_step_handler(msg, process_firstname_step)
    else:
        bot.send_message(message.chat.id, "Вы уже регистрировались, ждите письма через неделю, или напишите Ладе, если сомневаетесь в успехе.")


# markups to keyboard
keyboard_course = telebot.types.ReplyKeyboardMarkup()
keyboard_course.row('1-2 курс', '3-4 курс, магистр, аспирант')
# markup to force reply
force_reply = telebot.types.ForceReply(selective=False)
# markup to hide previous markup
markupHide = telebot.types.ReplyKeyboardRemove(selective=False)




def process_firstname_step(message):
    user_id = message.from_user.id
    user_data[user_id] = User(message.text, message.from_user.username)
    msg = bot.send_message(message.chat.id, "Вы первый-второй курс или старше?", reply_markup=keyboard_course)
    bot.register_next_step_handler(msg, process_course_step)

import random

def process_course_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.course = message.text
    bot.send_message(message.chat.id, "Вопрос-капча: прошу ответить русскими буквами, начиная с большой буквы, тестируется хэш от строки", reply_markup=markupHide)
    the_question = random.choice(list(question_dict.keys()))
    msg = bot.send_message(message.chat.id, the_question)
    bot.register_next_step_handler(msg, lambda m: registration_fail_success(m, the_question))

def bare_captcha(message):
    the_question = random.choice(list(question_dict.keys()))
    msg = bot.send_message(message.chat.id, the_question)
    bot.register_next_step_handler(msg, lambda m: registration_fail_success(m, the_question))

import base64

def registration_fail_success(message, the_question):
    user_id = message.from_user.id
    user = user_data[user_id]
    text = message.text
    text_binary = text.encode(encoding='utf_8')

    if base64.b64encode(text_binary) == question_dict[the_question]:
        bot.send_message(group_id, user.first_name+ " @" + user.username + " зарегался. Это" + user.course, parse_mode="Markdown")
        bot.send_message(message.chat.id, "Вы успешно зарегистрированы! Ждите ответа через неделю" )
        user.passed_captcha = True
    else:
         bot.send_message(message.chat.id, "Ответ не принят, ещё один случайный вопрос: ")
         bot.send_message(group_id, user.first_name+ " @" + user.username + " не ответил на капчу. Это" + user.course, parse_mode="Markdown")
         bare_captcha(message)

question_dict = { "Имя первого декана матфака: " : b'0KHQtdGA0LPQtdC5',
                    "Имя декана матфака с 2015 года:" : b'0JLQu9Cw0LTQu9C10L0=',
                    "Имя декана матфака с 2020 года:" : b'0KHQsNCx0LjRgA=='
                    }


bot.polling()

