import sqlite3
import os
from sqlite3 import Error
from usuariAlta import *

# Per gestionar el fitxer config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

nomBD = config['basedades']["nom"]

def sql_connection():
    """
    Crea la connexió a la base de dades
    """
    try:
        con = sqlite3.connect(nomBD)
        return con
    except Error:
        print(Error)


def sql_tableUsuaris(con):
    """
    Creem la taula usuaris
    """
    cur = con.cursor()
    cur.execute("CREATE TABLE usuaris(id varchar(255), nom varchar(255), mail varchar(255), poblacio varchar(255), telefon varchar(255), edat integer, alta char(1))")
    con.commit()


def sql_tableAdmin(con):
    """
    Creem la taula admin
    """
    cur = con.cursor()
    cur.execute("CREATE TABLE admin(id varchar(255))")
    con.commit()


def sql_insertAdmin(con, id):
    """
    Funció que inserta l'id de l'administrador
    """
    cur = con.cursor()
    cur.execute("INSERT INTO admin(id) VALUES(?)", [id])
    con.commit()


def sql_insert(con, x):
    """
    Funció que inserta un usuari a la base de dades
    """
    cur = con.cursor()
    cur.execute("INSERT INTO usuaris(id, nom, mail, poblacio, telefon, edat, alta) VALUES(?, ?, ?, ?, ?, ?, ?)", [x.id, x.nom, x.mail, x.poblacio, x.telefon, x.edat, "s"])
    con.commit()


def sql_selectAllAdmin(con):
    """
    Funció que recupera tota la llista d'administradors
    """
    cur = con.cursor()
    query = "SELECT * FROM admin"
    cur.execute(query)
    rows = cur.fetchall()
    llista = list()
    for row in rows:
        llista.append(row)
    return llista
    

def sql_selectAll(con):
    """
    Funció que retorna tota la llista dels usuaris
    que estan donats d'alta
    """
    cur = con.cursor()
    query = "SELECT * FROM usuaris WHERE alta = 's'"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def sql_buscar(con, nom):
    """
    Funció que busca un usuari (pel nom) a la base de dades.
    Busca els noms que comencen amb el nom passat. 
    """
    cur = con.cursor()    
    query = "SELECT * FROM usuaris WHERE nom LIKE ? and alta like 's';"
    cur.execute(query, [ "%{}%".format(nom) ])
    rows = cur.fetchall()
    llista = list()
    for row in rows:
        element = Usuari()
        element.id=row[0]
        element.nom=row[1]
        element.mail=row[2]
        element.poblacio=row[3]
        element.telefon=row[4]
        element.edat=row[5]
        element.alta=row[6]
        llista.append(element)
    return llista


def sql_buscarID(con, id):
    """
    Funció que busca un usuari per l'id.
    """
    cur = con.cursor()
    cur.execute("SELECT * FROM usuaris WHERE id LIKE ?", [id])
    rows = cur.fetchall()
    llista = list()
    for row in rows:
        element = Usuari()
        element.id=row[0]
        element.nom=row[1]
        element.mail=row[2]
        element.poblacio=row[3]
        element.telefon=row[4]
        element.edat=row[5]
        element.alta=row[6]
        llista.append(element)
    return llista


def sql_baixa(con, x):
    """
    Funció que dóna de baixa a un usuari.
    Canvia el camp alta per 'n'
    """
    cur = con.cursor()
    cur.execute("UPDATE usuaris SET alta = 'n' WHERE id like ? AND nom like ?", [x.id, x.nom])
    con.commit()


def sql_poblacio(con):
    """
    Funció que cerca el total d'usuaris
    que hi ha a cada població
    """
    cur = con.cursor()
    cur.execute("SELECT DISTINCT poblacio, count(poblacio) FROM usuaris WHERE alta = 's' GROUP by poblacio")
    rows = cur.fetchall()
    llista = list()
    for row in rows:
        llista.append(row)
    return llista


def sql_edat(con, edat_min, edat_max):
    """
    Funció que cerca el total d'usuaris
    que hi ha en una franja d'edat
    """
    cur = con.cursor()
    cur.execute("SELECT count(edat) FROM usuaris WHERE edat >= ? and edat <= ? and alta = 's'", [edat_min, edat_max])
    rows = cur.fetchall()
    row = rows[0]
    return row
