import config
from config import token
import telebot
from telebot import types
from openpyxl import load_workbook
import time
import secrets
import string
from datetime import date
import pandas as pd
from pandas import DataFrame
from transliterate import translit

bot = telebot.TeleBot(config.token)

class Data(object):
    def __init__(self) -> None:
        self.data:dict={}
        self.i_obj2=0
        self.i_obj1=0
    def add(self,data:dict) -> None:
        self.data.update(data)
    def obj(self,num):
        if num==1:self.i_obj1+=1
        else: self.i_obj2+=1
data:object=Data()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"""Приветствую, `{message.from_user.username}`. Вы попали к почтовому боту ЧРТ
    Для регистрации почты введите команду /register
    Для восстановления пароля введите команду /recovery
    Для предоставления списка проектов введите /prjlist
    """, parse_mode = "Markdown")

@bot.message_handler(commands=['register'])
def register_name(message):
    mesg = bot.send_message(message.chat.id, f"Для начала введите своё имя", parse_mode = 'Markdown')
    bot.register_next_step_handler(mesg, register_surname)
def register_surname(message):
    mesg = bot.send_message(message.chat.id, f"Теперь введите фамилию")
    en_text = translit(message.text, language_code='ru', reversed=True)
    en_text = en_text.lower()
    data.add({'name': en_text})
    bot.register_next_step_handler(mesg, register_id)
def register_id(message):
    en_text = translit(message.text, language_code='ru', reversed=True)
    en_text = en_text.lower()
    data.add({"surname": en_text})
    photo = open("studentid.png", 'rb')
    textmesg = f'Напоследок введите номер студенческого билета'
    mesg = bot.send_photo(message.chat.id, photo, caption = textmesg, parse_mode='Markdown')
    bot.register_next_step_handler(mesg, register_end)
def register_end(message):
    data.add({"id": message.text})
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    text = f"""
    Я проверил, и вы действительно не имеете почты в доменной зоне radiotech\\.su и являетесь студентом ЧРТ 
    Ваша новая почта  {data.data['name']}\\.{data.data['surname']}@radiotech\\.su  Пароль \\- ||{password}||
    Ваша почта скоро будет активна и вход по ней будет доступен\\!
    """
    chektext = f'*Проверка в базе данных учеников\\.\\.\\.*'
    chekmsg = bot.send_message(message.chat.id, chektext, parse_mode='MarkdownV2')
    time.sleep(5)
    bot.edit_message_text(text, chekmsg.chat.id, chekmsg.message_id, parse_mode='MarkdownV2')
    mail = f"{data.data['name']}.{data.data['surname']}@radiotech.su"
    wb = openpyxl.open("registerdata.xlsx")
    wb.active = 0
    sheet = wb.active
    sheet.append([data.data['id'], mail, password, message.from_user.id, message.from_user.username])
    wb.save("registerdata.xlsx")
@bot.message_handler(commands=['recovery'])
def recovery_mail(message):
    mesg = bot.send_message(message.chat.id, f'Вас понял. Для заявки на восстановление почты введите свой адрес электронной почты вида name.surname@radiotech.su')
    bot.register_next_step_handler(mesg, recovery_idphoto)
def recovery_idphoto(message):
    data.add({"mail": message.text})
    photo = open("studentid.png",'rb')
    textmesg = f'Теперь введите номер студенческого билета, чтобы найти его, посмотрите на фотографию'
    mesg = bot.send_photo(message.chat.id, photo, caption = textmesg, parse_mode='MarkdownV2' )
    bot.register_next_step_handler(mesg, recovery_accepting)
def recovery_accepting(message):
    data.add({"id": message.text})
    bot.send_message(message.chat.id, f"Заявка на восстановление пароля передана администрации. Ожидайте")
    adminID = 1594231051
    mail = data.data['mail']
    id = data.data['id']
    bot.send_message(adminID, f"""
    *Заявка* на восстановление пароля
    *Почта* - `{mail}`
    *Номер* - `{id}`
    *TGUN* - @{message.from_user.username}
    *TGID* - `{message.from_user.id}`
    """, parse_mode='Markdown')

@bot.message_handler(commands=['prjlist'])
def prjlist(message):
    today = date.today()
    bot.send_message(message.chat.id, f'''Актуальные на *{today}* проекты:
    [Почтовый ТГ бот](https://t.me/mailcrt_bot)
    [ATREI - Файлообменник с расширенными функциями для студентов техникума] (https://github.com/Foxius/atrei)
    ''', parse_mode='Markdown')
bot.polling(none_stop=True, interval=0)
try:
    bot.polling(none_stop=True)
except Exception as e:
    logger.exception("Fail startup:", e)
