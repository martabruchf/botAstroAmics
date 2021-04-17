# -*- coding: utf-8 -*-

from usuariAlta import *
from sqliteAstro import *
from enviarMail import *
import re

# Funcions per guardar totes les dades per donar
# d'alta a un usuari

element = Usuari()

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
    cid=m.chat.id
    mail = m.text
    valid = es_mail_valid(mail)
    if(valid):
        element.mail = mail        
        missatge = "Població:"
        bot.send_message(cid, missatge)
        userEstatus[cid]="poblacioAlta"
    else:
        missatge = "L'e-mail no és vàlid. Entra un correu electrònic correcte.\nE-mail:"
        bot.send_message(cid, missatge)
        userEstatus[cid]="emailAlta"


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
    cid=m.chat.id
    edat = m.text
    if (edat.isdigit()):
        edat = int(edat)
        if(edat >=0 and edat <=120):
            element.edat = m.text        
            missatge = "L'alta ha estat tramitada.\nEn breu rebràs un mail de confirmació."
            bot.send_message(cid, missatge)
            con = sql_connection()
            sql_insert(con, element)
            sql_selectAll(con)
            con.close()
            enviarMail(element, "alta")
            enviarMailAdmin(element, "alta")
        else:
            missatge = "Has d'entrar una edat vàlida.\nEdat:"
            bot.send_message(cid, missatge)
            userEstatus[cid]="edatAlta"
    else:
        missatge = "Has d'entrar una edat vàlida.\nEdat:"
        bot.send_message(cid, missatge)
        userEstatus[cid]="edatAlta"


def es_mail_valid(correo):
    """
    Funció que comprova si el correu electrònic
    és vàlid
    """
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None