# -*- coding: utf-8 -*-

"""
This is a detailed example using almost every command of the API
"""

import time

import telebot
from telebot import types
from usuariAlta import *
from baixaUsuari import *
from dadesAltaUsuari import *
from validarContrasenya import *
from sqliteAstro import *
import os

# Per gestionar el fitxer config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


# De config.ini importem la variable TOKEN
TOKEN = config['telegram']["TOKEN"]
nomBD = config['basedades']["nom"]
# Creem el bot
bot = telebot.TeleBot(TOKEN, num_threads=10)

# Per guardar que espera cada usuari
userEstatus = {}
# Llista dels usuaris administradors
llistaAdmin = list()
llistaUsuarisBaixa = list()

# Descripció de les comandes per la comanda "help" de l'usuari normal
comandesUsuari = {  
    'start'       : 'Per iniciar el bot',
    'help'        : 'Et diu quines comandes hi ha',
    'alta'        : 'Per donar d\'alta un usuari',
    'admin'       : 'Entrar la contrasenya d\'administrador'
}

# Descripció de les comandes per la comanda "help" de l'usuari administrador
comandesAdmin = { 
    'start'         : 'Per iniciar el bot',
    'help'          : 'Et diu quines comandes hi ha',
    'alta'          : 'Per donar d\'alta un usuari',
    'baixa'         : 'Per donar de baixa un usuari',
    'estadistiques' : 'Per veure les estadístiques'
}

# Comprovem si la base de dades existeix 
# si no existeix creem la taula
# os.remove(nomBD)
if os.path.isfile(nomBD):
    print("La base de dades ja existeix.")    
else:    
    con = sql_connection()
    sql_table(con)
    print("Taula creada.")


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


# Comanda alta
@bot.message_handler(commands=['alta'])
def command_alta(m):
    """
    Demana les dades per donar-se d'alta
    """
    cid = m.chat.id
    missatge = "Entra les dades per donar-te d'alta."
    bot.send_message(cid, missatge)
    missatge = "Nom i cognoms:"
    bot.send_message(cid, missatge)
    userEstatus[cid]="nomAlta"


# Comanda baixa
@bot.message_handler(commands=['baixa'])
def command_alta(m):
    """
    Demana les dades per donar un usuari de baixa
    """
    cid = m.chat.id
    missatge = "Entra el nom de l'usuari a donar de baixa."
    bot.send_message(cid, missatge)
    userEstatus[cid]="nomBaixa"


# Comanda estadistiques
@bot.message_handler(commands=['estadistiques'])
def command_estadistiques(m):
    """
    Mostra per pantalla les estadístiques dels usuaris
    Primer mostra 2 botons per triar quina estadística vols
    """
    bot.send_message(m.chat.id, "Escull una opció:",
                     reply_markup=mostraTeclat())


def mostraTeclat():
    """
    Funció que crea el teclat
    """
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Població", callback_data="bPoblacio"), types.InlineKeyboardButton("Edat", callback_data="bEdat"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print("funció "+str(call))
    opcio = call.data
    if (opcio == "bPoblacio"):
        pass
    elif (opcio == "bEdat"):
        pass


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
Aquest bot és per donar-se d'alta al grup d'AstroAmics.
Escriu /help per saber què pots fer.
""")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    """
    Funció que rep els missatges que no tenen la /
    """
    cid=m.chat.id
    global llistaUsuarisBaixa
    if userEstatus[cid] == "contrasenya":
        validarContrasenya(m, llistaAdmin, bot)
    elif userEstatus[cid] == "nomAlta":
        nomUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "emailAlta":
        mailUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "poblacioAlta":
        poblacioUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "telAlta":
        telUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "edatAlta":
        edatUsuari(m, bot)
    elif userEstatus[cid] == "nomBaixa":
       llistaUsuarisBaixa = nomUsuariBaixa(m, bot, userEstatus)
    elif userEstatus[cid] == "numBaixa":
        baixaUsuari(m, bot, cid, llistaUsuarisBaixa)



# PER FER EL TECLAT
#x = types.ReplyKeyboardMarkup([keyboard = ["a", "b", "c"], ["d", "e", "f"]])


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()



