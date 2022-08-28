import telebot
import requests # Модуль для обработки URL
# from bs4 import BeautifulSoup # Модуль для работы с HTML
# import time # Модуль для остановки программы
import smtplib # Модуль для работы с почтой
from telebot import types
# from openpyxl import load_workbook
# from openpyxl.drawing.image import Image
import time
# import colorama
# from colorama import Fore, Back, Style
import secrets
import string


bot = telebot.TeleBot("5694829327:AAE6Sz6xEsbN7QHeq8-QjiaPtUtu-tUAOW0")

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
    mesg = bot.send_message(message.chat.id, f"Для начала введите своё имя *транслитом*", parse_mode = 'Markdown')
    bot.register_next_step_handler(mesg, register_surname)
def register_surname(message):
    mesg = bot.send_message(message.chat.id, f"Теперь введите фамилию (также транслитом)")
    data.add({'name': message.text})
    bot.register_next_step_handler(mesg, register_end)
def register_end(message):
    data.add({"surname": message.text})
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))
    text = f"""
    Я проверил, и вы действительно не имеете почты в доменной зоне radiotech\\.su и являетесь студентом ЧРТ 
    Ваша новая почта  {data.data['name']}\\.{data.data['surname']}@radiotech\\.su  Пароль \\- ||{password}||"""
    #print(text)
    bot.send_message(message.chat.id, text, parse_mode='MarkdownV2')

@bot.message_handler(commands=['recovery'])
def recovery_mail(message):
    mesg = bot.send_message(message.chat.id, f'Вас понял. Для заявки на восстановление почты введите свой адрес электронной почты вида name.surname@radiotech.su')
    bot.register_next_step_handler(mesg, recovery_idphoto)
def recovery_idphoto(message):
    data.add({"mail": message.text})
    photo = open("studentid.png",'rb')
    textmesg = f'Теперь введите номер студенческого билета, чтобы найти его, посмотрите на фотографию'
    mesg = bot.send_photo(message.chat.id, photo, caption = txtmesg, parse_mode='MarkdownV2' )
    bot.register_next_step_handler(mesg, recovery_accepting)
def recovery_accepting()
    data.add({"id": message.text})
    bot.send_message(message.chat.id, f"Заявка на восстановление пароля передана администрации. Ожидайте")
    adminID = 1594231051
    bot.send_message(adminID, f"Заявка на восстановление пароля\n Почтв")
bot.polling(none_stop=True, interval=0)
try:
    bot.polling(none_stop=True)
except Exception as e:
    logger.exception("Fail startup:", e)
