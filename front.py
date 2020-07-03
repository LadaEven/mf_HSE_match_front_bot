import telebot
import logging
#from pprint import pprint

bot = telebot.TeleBot("Your ACESS_TOKEN")
group_id = "here goes the group ID where the forms go"

user_data = {}

class User:
    def __init__(self, first_name, user_name):
        self.first_name = first_name
        self.course = ''
        self.username = user_name

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
        bot.send_message(message.chat.id, "Вы уже зарегистрировались, ждите письма через неделю")


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




def process_course_step(message):
    user_id = message.from_user.id
    user = user_data[user_id]
    user.course = message.text
    bot.send_message(message.chat.id, "Вы успешно зарегистрированы! Ждите ответа через неделю" , reply_markup=markupHide)
    bot.send_message(group_id, user.first_name+ " @" + user.username + " зарегался. Это" + user.course, parse_mode="Markdown")

bot.polling()
