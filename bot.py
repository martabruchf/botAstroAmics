# -*- coding: utf-8 -*-

"""
This is a detailed example using almost every command of the API
"""

from estadistiques import poblacio
import time

import telebot
from telebot import types
from usuariAlta import *
from baixaUsuari import *
from dadesAltaUsuari import *
from validarContrasenya import *
from estadistiques import *
from sqliteAstro import *
import os

# Per gestionar el fitxer config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


# De config.ini importem les variables
TOKEN = config['telegram']["TOKEN"]
nomBD = config['basedades']["nom"]

# Creem el bot
bot = telebot.TeleBot(TOKEN, num_threads=10)

# Per guardar que espera cada usuari
userEstatus = {}
# Llistes
llistaAdmin = list()
llistaUsuarisBaixa = list()

# Descripció de les comandes per l'ordre "help" de l'usuari normal
comandesUsuari = {      
    'help'        : 'Et diu quines ordres hi ha',
    'alta'        : 'Per donar d\'alta un usuari',
    'admin'       : 'Entrar la contrasenya d\'administrador'
}

# Descripció de les comandes per l'ordre "help" de l'usuari administrador
comandesAdmin = { 
    'help'          : 'Et diu quines ordres hi ha',
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
    sql_tableUsuaris(con)
    print("Taula usuaris creada.")
    sql_tableAdmin(con)
    print("Taula administradors creada.")


# Recuperem la llista d'administradors
con = sql_connection()
llistaAdmin = sql_selectAllAdmin(con)
con.close()

# Creació dels teclats
keyboardUsuari = types.ReplyKeyboardMarkup(True)
keyboardUsuari.row('/alta', '/baixa')
keyboardUsuari.row('/admin', '/help')
keyboardAdmin = types.ReplyKeyboardMarkup(True)
keyboardAdmin.row('/alta', '/admin', '/help')
keyboardAdmin.row('/baixa', '/estadistiques')
keyboardEsta = types.ReplyKeyboardMarkup(True)
keyboardEsta.row('/poblacio', '/edat')


# Ordre '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    msg = "Hola! Benvingut/da al bot d'AstroAmics! Aquest bot és per donar-se d'alta al grup d'AstroAmics."
    bot.send_message(cid, msg, reply_markup=keyboardUsuari)


# Ordre admin
@bot.message_handler(commands=['admin'])
def command_admin(m):
    """
    Demana la contrasenya d'usuari
    """
    cid = m.chat.id
    missatge = "Entra la contrasenya d'Administrador:"
    bot.send_message(cid, missatge)
    userEstatus[cid]="contrasenya"


# Ordre alta
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


# Ordre baixa
@bot.message_handler(commands=['baixa'])
def command_alta(m):
    """
    Demana les dades per donar un usuari de baixa
    """
    global llistaAdmin
    cid = m.chat.id
    admin = esAdmin(llistaAdmin, str(cid))
    if(admin == True):
        missatge = "Entra el nom de l'usuari a donar de baixa."
        bot.send_message(cid, missatge)
        userEstatus[cid]="nomBaixa"
    else:
        baixa(cid, bot, userEstatus)


# Ordre estadistiques
@bot.message_handler(commands=['estadistiques'])
def command_estadistiques(m):
    """
    Mostra per pantalla les estadístiques dels usuaris
    Primer mostra 2 botons per triar quina estadística vols
    """
    #bot.send_message(m.chat.id, "Escull quina estadística vols veure:", reply_markup=mostraTeclat())
    bot.send_message(m.chat.id, "Escull quina estadística vols veure:", reply_markup=keyboardEsta)


# Ordre Poblacio
@bot.message_handler(commands=['poblacio'])
def command_estadistiques(m):
    global llistaAdmin
    cid = m.chat.id
    poblacio(bot, cid)
    admin = esAdmin(llistaAdmin, str(cid))
    missatge = "Què més vols fer?"
    if(admin == True):
        bot.send_message(cid, missatge, reply_markup=keyboardAdmin)
    else:
        bot.send_message(cid, missatge, reply_markup=keyboardUsuari)


# Ordre Edat
@bot.message_handler(commands=['edat'])
def command_estadistiques(m):
    global llistaAdmin
    cid = m.chat.id
    edat(bot, cid)
    admin = esAdmin(llistaAdmin, str(cid))
    missatge = "Què més vols fer?"
    if(admin == True):
        bot.send_message(cid, missatge, reply_markup=keyboardAdmin)
    else:
        bot.send_message(cid, missatge, reply_markup=keyboardUsuari)


# def mostraTeclat():
#     """
#     Funció que crea el teclat
#     """
#     markup = types.InlineKeyboardMarkup()
#     markup.row_width = 2
#     markup.add(types.InlineKeyboardButton("Població", callback_data="bPoblacio"), types.InlineKeyboardButton("Edat", callback_data="bEdat"))
#     return markup


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     """
#     Funció que recull l'opció escollida del teclat estadística
#     """
#     print("funció "+str(call))
#     opcio = call.data
#     chat_id = call.from_user.id
#     if (opcio == "bPoblacio"):
#         poblacio(bot, chat_id)
#     elif (opcio == "bEdat"):
#         edat(bot, chat_id)


# Ordre help
@bot.message_handler(commands=['help'])
def command_help(m):
    global llistaAdmin
    cid = str(m.chat.id)
    admin = esAdmin(llistaAdmin, cid)
    help_text = "Pots utilitzar les següents ordres: \n"    
    if admin:
        for key in comandesAdmin:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += comandesAdmin[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page
    else:
        for key in comandesUsuari:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += comandesUsuari[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    """
    Funció que rep els missatges que no tenen la /
    """
    cid=m.chat.id
    global llistaUsuarisBaixa
    global llistaAdmin
    if userEstatus[cid] == "contrasenya":
        llistaAdmin = validarContrasenya(m, llistaAdmin, bot, keyboardAdmin)
    elif userEstatus[cid] == "nomAlta":
        nomUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "emailAlta":
        mailUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "poblacioAlta":
        poblacioUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "telAlta":
        telUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "edatAlta":
        edatUsuari(m, bot, userEstatus)
    elif userEstatus[cid] == "nomBaixa":
       llistaUsuarisBaixa = nomUsuariBaixa(m, bot, userEstatus)
    elif userEstatus[cid] == "numBaixa":
        baixaUsuari(m, bot, cid, llistaUsuarisBaixa)
    elif userEstatus[cid] == "dadesBaixa":
        dadesBaixa(m, bot, cid)
        




# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()
