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
    bot.send_message(cid, missatge)
    enviarMail(llistaUsuarisBaixa[idBaixa].mail, "baixa")
    print("Llista usuaris actuals")
    sql_selectAll(con)
    con.close()


def baixa(cid, bot, userEstatus):
    """
    Funció que dóna de baixa l'usuari actual
    """
    # Buscar si l'id està a la base de dades
    con = sql_connection()
    llista = sql_buscarID(con, cid)
    # Comprovar que només hi hagi un id
    if (len(llista) == 1):
        sql_baixa(con, llista[0])
        missatge = "La baixa s'ha fet amb èxit."
        bot.send_message(cid, missatge)
        enviarMailAdmin(llista[0])
    else:
        # Si hi ha més d'un id, demanar nom i població i enviar mail a l'administrador
        missatge = "Escriu el teu nom, cognoms i població:"
        bot.send_message(cid, missatge)
        userEstatus[cid]="dadesBaixa"
    con.close()


def dadesBaixa(m, bot, cid):
    """
    Continuació de la funció baixa.
    Envia el mail a l'administrador perquè doni de baixa
    a l'usuari.
    """
    enviarMailAdminBaixa(m)
    missatge = "S'ha enviat un mail a l'administrador perque et doni de baixa.\nUn cop donat de baixa rebràs un mail."
    bot.send_message(cid, missatge)