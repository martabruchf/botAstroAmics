# -*- coding: utf-8 -*-

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