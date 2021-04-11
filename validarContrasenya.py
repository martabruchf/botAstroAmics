# -*- coding: utf-8 -*-

# Per gestionar el fitxer config.ini
import configparser
from sqliteAstro import *
config = configparser.ConfigParser()
config.read('config.ini')


def validarContrasenya(m, llistaAdmin, bot, keyboardAdmin):
    """
    Validem si el password entrat és correcte.
    Si és correcte s'afageix el id a la llista.
    Si és incorrecte se l'avisa.
    """
    cid = str(m.chat.id)
    if m.text == config['main']["password"]:
        admin = esAdmin(llistaAdmin, cid)
        if(admin == False):
            con = sql_connection()
            sql_insertAdmin(con, m.chat.id)
            con.close()
            llistaAdmin.append(m.chat.id)
        bot.send_message(m.chat.id,  "Ara ets administrador.\nEscriu /help per veure què pots fer.", reply_markup=keyboardAdmin)
    else:
        bot.send_message(m.chat.id, "Contrasenya incorrecta.")
    return llistaAdmin


def esAdmin(llistaAdmin, cid):
    """
    Funció que comprova si el cid és administrador
    """
    esAdmin = False
    for x in llistaAdmin:
        id = x[0]
        if (id == cid):
            esAdmin = True
    return esAdmin