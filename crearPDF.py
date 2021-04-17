# -*- coding: utf-8 -*-

from sqliteAstro import *
from datetime import datetime
import os
from reportlab.platypus import Paragraph
from reportlab.platypus import Image
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
# Importamos clase de hoja de estilo de ejemplo.
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import *
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table

def crearPDF(cid):
    # Dia actual
    avui = datetime.today().strftime('%d/%m/%Y')

    # Llista d'usuaris
    con = sql_connection()
    usuaris = sql_selectAll(con)
    con.close()

    estilos = getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='Centrat', alignment=TA_CENTER))

    # Creamos un PageTemplate de ejemplo.
    estiloHoja = getSampleStyleSheet()
    # Inicializamos la lista Platypus Story.
    story = []
    # Definimos cómo queremos que sea el estilo de la PageTemplate.
    cabecera = estiloHoja['Heading2']
    # No se hará un salto de página después de escribir la cabecera (valor 1 en caso contrario).
    cabecera.pageBreakBefore=0
    # Se quiere que se empiece en la primera página a escribir. Si es distinto de 0 deja la primera hoja en blanco.
    cabecera.keepWithNext=0
    # Color de la cabecera.
    # cabecera.backColor=colors.oldlace
    fichero_imagen = "logo.jpeg"
    imagen_logo = Image(os.path.realpath(fichero_imagen),width=142,height=72)
    story.append(imagen_logo)
    # Incluimos un Flowable, que en este caso es un párrafo.
    text = "LLISTAT DE MEMBRES D'ASTROAMICS - " + avui
    # Lo incluimos en el Platypus story.
    story.append(Spacer(0,20))
    story.append(Paragraph(text, estilos["Title"]))
    story.append(Spacer(0,20))
    # Creem la taula amb el llistat
    fila1 = ['NOM I COGNOMS','POBLACIÓ','MAIL','TELÈFON','EDAT']
    files = ([fila1])
    for x in usuaris:
        fila = [x.nom, x.poblacio, x.mail, x.telefon, x.edat]
        files.append(fila)
    taula = Table(files)
    taula.setStyle([('BACKGROUND',(0,0),(5, 0),colors.orange)])
    taula.setStyle([('BACKGROUND',(0,1),(-1,-1),colors.antiquewhite)])
    story.append(taula)
    doc=SimpleDocTemplate("AstroAmics.pdf", pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
