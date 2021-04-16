# -*- coding: utf-8 -*-

from usuariAlta import *
from sqliteAstro import *
from enviarMail import *

# Funcions per guardar totes les dades per donar
# de baixa a un usuari

element = Usuari()

def nomUsuariBaixa(m, bot, userEstatus):
    """
    Guardem el nom a buscar
    i recuperem tots els noms que coincideixen
    a la base de dades
    """
    cid=m.chat.id
    element.id = cid
    element.nom = m.text # Guardem el nom a buscar
    con = sql_connection()
    llistaUsuaris = sql_buscar(con, element.nom)
    # Mostrem la llista d'usuaris al bot
    if(len(llistaUsuaris) > 0):
        i=1
        for x in llistaUsuaris:
            missatge = str(i) + ": " + x.nom + " - " + x.poblacio
            bot.send_message(cid, missatge)
            i = i + 1
        missatge = "Escriu el número de l'usuari a donar de baixa:"
        bot.send_message(cid, missatge)
        userEstatus[cid]="numBaixa"
        return llistaUsuaris
    else:
        missatge = "No hi ha cap usuari amb aquest nom."
        bot.send_message(cid, missatge)
    con.close()


def baixaUsuari(m, bot, cid, llistaUsuarisBaixa):
    """
    Funció que recupera l'usuari que es vol donar de baixa
    i el dóna de baixa.
    """
    cid=m.chat.id
    idBaixa = m.text
    idBaixa = int(idBaixa) - 1
    con = sql_connection()
    sql_baixa(con, llistaUsuarisBaixa[idBaixa])
    missatge = "L'usuari ha estat donat de baixa."
    enviarMail(llistaUsuarisBaixa[idBaixa].mail, "baixa")
    bot.send_message(cid, missatge)
    print("Llista usuaris actuals")
    sql_selectAll(con)
    con.close()
