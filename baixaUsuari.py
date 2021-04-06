# -*- coding: utf-8 -*-

from usuariAlta import *
from sqliteAstro import *

# Funcions per guardar totes les dades per donar
# de baixa a un usuari

element = Usuari()

def nomUsuariBaixa(m, bot, userEstatus):
    """
    Guardem el nom
    """
    cid=m.chat.id
    element.id = cid
    element.nom = m.text
    con = sql_connection()
    sql_buscar(con, element.nom)

    # missatge = "E-mail:"
    # bot.send_message(cid, missatge)
    # userEstatus[cid]="emailAlta"
 #   con.close()
