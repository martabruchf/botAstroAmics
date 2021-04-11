# -*- coding: utf-8 -*-

from sqliteAstro import *

def poblacio(bot, chat_id):
    """
    Funció que mostra les estadístiques
    per població
    """
    con = sql_connection()
    llista = sql_poblacio(con)
    con.close()
    for x in llista:
        missatge = x[0] + ": " + str(x[1])
        bot.send_message(chat_id, missatge)


def edat(bot, chat_id):
    """
    Funció que mostra les estadístiques
    per edat
    """
    con = sql_connection()
    # Menors de 19 anys.
    total = sql_edat(con, 0, 19)
    missatge = "Menors de 19 anys: " + str(total[0])
    bot.send_message(chat_id, missatge)
    # De 20 a 29 anys.
    total = sql_edat(con, 20, 29)
    missatge = "De 20 a 29 anys: " + str(total[0])
    bot.send_message(chat_id, missatge)
    # De 30 a 39 anys.
    total = sql_edat(con, 30, 39)
    missatge = "De 30 a 39 anys: " + str(total[0])
    bot.send_message(chat_id, missatge)
    # De 40 a 49 anys.
    total = sql_edat(con, 40, 49)
    missatge = "De 40 a 49 anys: " + str(total[0])
    bot.send_message(chat_id, missatge)
    # De 50 a 59 anys.
    total = sql_edat(con, 50, 59)
    missatge = "De 50 a 59 anys: " + str(total[0])
    bot.send_message(chat_id, missatge)
    # De 60 a 69 anys.
    total = sql_edat(con, 60, 69)
    missatge = "De 60 a 69 anys: " + str(total[0])
    bot.send_message(chat_id, missatge)
    # Més grans de 70 anys
    total = sql_edat(con, 70, 120)
    missatge = "Més grans de 70 anys: " + str(total[0])
    bot.send_message(chat_id, missatge)
    con.close()