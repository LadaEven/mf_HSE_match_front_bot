import telebot
import logging
#from pprint import pprint

bot = telebot.TeleBot("лала")
group_id = -лала


#дамп, чтобы не потерялись данные
import dill


try:
    with open("database_september.bin", "rb") as f:
        user_data = dill.load(f)
except EOFError:
    user_data = {}



#далее логика работы.

class User:
    def __init__(self, chat_id):
        self.first_name = ''
        self.course = ''
        self.chat_id = chat_id
        self.username = 'None'
        self.question = ''
        self.condition = 0
        self.add_info = 'None'
        #conditions 1 -- entered correct name
        # 2 -- entered correct course
        # 3 -- passed_captcha

condition_dict = {
                       0 : " should enter name",
                        1 : "entered correct name, should enter course",
                        2: "entered course, should add contacts",
                       3 : "entered contacts, should answer the question",
                       4 : "passed captcha, thank you!" }

logger = telebot.logger  # set logger
telebot.logger.setLevel(logging.WARNING) # Outputs debug messages to console.

@bot.message_handler(commands=['start'])
def welcome_message(message):
    if(message.chat.id not in user_data):
        user = User(message.chat.id)
        user_data[message.chat.id] = user
        if ( message.from_user.username ):
                user.username = message.from_user.username
        try:
            bot.send_message(message.chat.id, "Напишите свои имя и фамилию")
            bot.send_message(group_id, str(message.chat.id)+ " " + user.username + " Начал регистрацию")
        except telebot.apihelper.ApiException:
            print("blocked")

    else:
        bot.send_message(message.chat.id, "Вы уже начали регистрацию, вы остановились на шаге " + condition_dict[user_data[message.chat.id].condition])

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id ,"Вопросы, предложения, сообщить, что бот упал: пишите Ладе @OrangeLine.")

    if(message.chat.id not in user_data):
        bot.send_message(message.chat.id, "такие дела")
    else:
        bot.send_message(message.chat.id, "Вы уже начали регистрацию, вы остановились на шаге " + condition_dict[user_data[message.chat.id].condition]+
         " если хотите исправить данные, отправьте команду /reset")

@bot.message_handler(commands=['about'])
def about(message):
 bot.send_message(message.chat.id , "Код на github: LadaEven/mf_HSE_match_front_bot" +
 " Этот бот познакомит старшекурсников и младшекурсников матфака. Вы отправляете заявку, заявка сохраняется в питоновском словаре," +
 "и через неделю я мэтчу людей -- по два контакта, если их будет не слишком много - я сделаю это вручную." )


@bot.message_handler(commands=['reset'])
def reset_registration(message):
    if message.chat.id in user_data:
        user_data[message.chat.id].condition = 0
        bot.send_message(message.chat.id, "Окей, теперь можно перерегаться, напишите имя и фамилию")
        bot.send_message(group_id, str(message.chat.id) + " Перерегистрируется")
    else:
        bot.send_message(message.chat.id, "Вы ещё не регались")

# markups to keyboard
keyboard_course = telebot.types.ReplyKeyboardMarkup()
keyboard_course.row("1й курс", "2й курс", "3-4й курс, магистр, аспирант")
# markup to hide previous markup
markupHide = telebot.types.ReplyKeyboardRemove(selective=False)

import random

@bot.message_handler(content_types=['text'])
def change_condition(message):
    if(message.chat.id in user_data):
        user = user_data[message.chat.id]
        condition = user.condition
        if condition == 0:
            if len(message.text.split()) == 2:
                bot.send_message(message.chat.id, "Записал имя и фамилию")
                user.first_name = message.text
                user.condition = 1
                bot.send_message(message.chat.id, "Вы первый курс или старше?", reply_markup=keyboard_course)
            else:
                bot.send_message(message.chat.id, "Вы ввели не два слова")
        elif condition == 1:
            if message.text in ["1й курс", "2й курс", "3-4й курс, магистр, аспирант"]:
                bot.send_message(message.chat.id, "Записал курс", reply_markup=markupHide)
                user.course = message.text
                bot.send_message(message.chat.id, "При желании, укажите дополнительные контакты: почта, инстаграм, вк. ")
                user.condition = 2

            else:
                bot.send_message(message.chat.id, "Пожалуйста, воспользуйтесь встроенной клавиатурой")

        elif condition == 2:
            #contacts
            user.add_info = message.text
            bot.send_message(message.chat.id , "Записал доп.контакты")
            user.condition = 3
            bot.send_message(message.chat.id, "Вопрос-капча: прошу ответить русскими буквами, начиная с большой буквы, тестируется хэш от строки")
            the_question = random.choice(list(question_dict.keys()))
            bot.send_message(message.chat.id, the_question)
            user.question = the_question


        elif condition == 3:
            msg_who = str(message.chat.id)+ " " + user.first_name + " @" + user.username+ " "  + user.add_info  + " " + user.course
            if captcha(message, user.question):
                user.condition = 4
                bot.send_message(group_id, msg_who + " зарегался")
                bot.send_message(message.chat.id,  " Вы успешно зарегистрированы! Ждите ответа через неделю" )
                with open("database.bin", "wb") as f:
                    dill.dump(user_data, f)
            else:
                bot.send_message(message.chat.id, "Вы не прошли капчу, попробуйте ещё раз")
                bot.send_message(group_id, msg_who  + " не прошёл капчу")
import base64

def captcha(message, the_question):
    text_binary = message.text.encode(encoding='utf_8')

    if base64.b64encode(text_binary) == question_dict[the_question]:
        return True
    else:
        return False


question_dict = { "Имя первого декана матфака: " : b'0KHQtdGA0LPQtdC5',
                    "Имя декана матфака с 2015 года:" : b'0JLQu9Cw0LTQu9C10L0=',
                    # "Имя декана матфака с 2020 года:" : b'0KHQsNCx0LjRgA=='
                    }
bot.polling()



