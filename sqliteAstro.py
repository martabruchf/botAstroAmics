import sqlite3
import os
from sqlite3 import Error

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


def sql_table(con):
    """
    Creem la taula
    """
    cur = con.cursor()
    cur.execute("CREATE TABLE usuaris(id varchar(255), nom varchar(255), mail varchar(255), poblacio varchar(255), telefon varchar(255), edat integer, alta char(1))")
    con.commit()


def sql_insert(con, x):
    """
    Funció que inserta un usuari a la base de dades
    """
    cur = con.cursor()
    cur.execute("INSERT INTO usuaris(id, nom, mail, poblacio, telefon, edat, alta) VALUES(?, ?, ?, ?, ?, ?, ?)", [x.id, x.nom, x.mail, x.poblacio, x.telefon, x.edat, "s"])
    con.commit()


def sql_selectAll(con):
    """
    Funció que retorna tota la llista dels usuaris
    """
    cur = con.cursor()
    query = "SELECT * FROM usuaris"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def sql_buscar(con, nom):
    """
    Funció que busca un usuari a la base de dades.
    Busca els noms que comencen amb el nom passat. 
    """
    cur = con.cursor()
    nomBuscar = nom + "*"
    query = "SELECT * FROM usuaris WHERE nom LIKE ?;"
    cur.execute(query, [ "%{}%".format(nom) ])
    rows = cur.fetchall()
    for row in rows:
        print(row)
