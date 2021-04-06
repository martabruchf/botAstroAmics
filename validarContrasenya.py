# -*- coding: utf-8 -*-

# Per gestionar el fitxer config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


def validarContrasenya(m, llistaAdmin, bot):
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