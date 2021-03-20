# -*- coding: utf-8 -*-

"""
This is a detailed example using almost every command of the API
"""

import time

import telebot
from telebot import types

# Per gestionar el fitxer config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


# De config.ini importem la variable TOKEN
TOKEN = config['telegram']["TOKEN"]
# Creem el bot
bot = telebot.TeleBot(TOKEN)

# Per guardar que espera cada usuari
userEstatus = {}
# Llista dels usuaris administradors
llistaAdmin = list()


class UsuariAlta:
    """
    Classe que conté les dades per donar d'alta un usuari
    """
    def __init__(self):
        self.nom = None
        self.mail = None
        self.poblacio = None
        self.telefon = None
        self.edat = None


comandesUsuari = {  # Descripció de les comandes per la comanda "help" de l'usuari normal
    'start'       : 'Per iniciar el bot',
    'help'        : 'Et diu quines comandes hi ha',
    'alta'        : 'Per donar d\'alta un usuari',
    'admin'       : 'Entrar la contrasenya d\'administrador'
}

comandesAdmin = { # Descripció de les comandes per la comanda "help" de l'usuari administrador
    'start'         : 'Per iniciar el bot',
    'help'          : 'Et diu quines comandes hi ha',
    'alta'          : 'Per donar d\'alta un usuari',
    'baixa'         : 'Per donar de baixa un usuari',
    'estadistiques' : 'Per veure les estadístiques'
}

# Comanda admin
@bot.message_handler(commands=['admin'])
def command_admin(m):
    """
    Demana la contrasenya d'usuari
    """
    cid = m.chat.id
    missatge = "Entra la contrasenya d'Administrador:"
    bot.send_message(cid, missatge)
    userEstatus[cid]="contrasenya"


# Comanda help
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Pots utilitzar les següents comandes: \n"
    if cid in llistaAdmin:
        for key in comandesAdmin:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += comandesAdmin[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page
    else:
        for key in comandesUsuari:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += comandesUsuari[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hola! Benvingut/da al bot d'AstroAmics!
Escriu /help per saber què pots fer.
""")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    """
    Funció que rep els missatges que no tenen la /
    """
    cid=m.chat.id
    if userEstatus[cid] == "contrasenya":
        validarContrasenya(m)


def validarContrasenya(m):
    """
    Validem si el password entrat és correcte.
    Si és correcte s'afageix el id a la llista.
    Si és incorrecte se l'avisa.
    """
    if m.text == config['main']["password"]:
        llistaAdmin.append(m.chat.id)
        bot.send_message(m.chat.id,  "Ara ets administrador.\nEscriu /help per veure què pots fer.")
    else:
        bot.send_message(m.chat.id, "Contrasenya incorrecta.")


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()
