# -*- coding: utf-8 -*-

from usuariAlta import *
from sqliteAstro import *

# Funcions per guardar totes les dades per donar
# d'alta a un usuari

element = UsuariAlta()

def nomUsuari(m, bot, userEstatus):
    """
    Guardem el nom
    """
    cid=m.chat.id
    element.id = cid
    element.nom = m.text
    missatge = "E-mail:"
    bot.send_message(cid, missatge)
    userEstatus[cid]="emailAlta"


def mailUsuari(m, bot, userEstatus):
    """
    Guardem el mail
    """
    element.mail = m.text
    cid=m.chat.id
    missatge = "Població:"
    bot.send_message(cid, missatge)
    userEstatus[cid]="poblacioAlta"


def poblacioUsuari(m, bot, userEstatus):
    """
    Guardem la població
    """
    element.poblacio = m.text
    cid=m.chat.id
    missatge = "Número del mòbil:"
    bot.send_message(cid, missatge)
    userEstatus[cid]="telAlta"


def telUsuari(m, bot, userEstatus):
    """
    Guardem el telèfon
    """
    element.telefon = m.text
    cid=m.chat.id
    missatge = "Edat:"
    bot.send_message(cid, missatge)
    userEstatus[cid]="edatAlta"


def edatUsuari(m, bot, userEstatus):
    """
    Guardem l'edat
    """
    element.edat = m.text
    cid=m.chat.id
    con = sql_connection()
    sql_insert(con, element)
    sql_selectAll(con)
    con.close()

