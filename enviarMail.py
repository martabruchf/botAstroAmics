# -*- coding: utf-8 -*-
from usuariAlta import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def enviarMail(mailDestinatari, tipus):
    # create message object instance
    msg = MIMEMultipart()
    
    if(tipus == "alta"):
        msg['Subject'] = "Alta AstroAmics"
        message = "T'has donat d'alta al Club AstroAmics.\nhttp://www.astroamics.tk"
    if(tipus == "baixa"):
        msg['Subject'] = "Baixa AstroAmics"
        message = "T'has donat de baixa al Club AstroAmics.\nhttp://www.astroamics.tk"

    # setup the parameters of the message
    password = config['mail']["password"]
    msg['From'] = config['mail']["email"]
    msg['To'] = mailDestinatari    
    
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()
    
    print ("successfully sent email to %s:" % (msg['To']))


def enviarMailAdmin(usuari):
    """
    Envia un mail a l'administrador
    informant-lo que un usuari s'ha donat de baixa.
    """
    # create message object instance
    msg = MIMEMultipart()
      
    # setup the parameters of the message
    password = config['mail']["password"]
    msg['From'] = config['mail']["email"]
    msg['To'] = config['mail']["email"]
    msg['Subject'] = "Usuari donat de baixa"
    message = "El següent usuari s'ha donat de baixa:\nID: " + usuari.id + " Nom: " + usuari.nom + " Població: " + usuari.poblacio

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()
    
    print ("successfully sent email to %s:" % (msg['To']))


def enviarMailAdminBaixa(m):
    """
    Envia un mail a l'administrador perquè doni de baixa
    a un usuari.
    """
    # create message object instance
    msg = MIMEMultipart()
      
    # setup the parameters of the message
    password = config['mail']["password"]
    msg['From'] = config['mail']["email"]
    msg['To'] = config['mail']["email"]
    msg['Subject'] = "Usuari per donar de baixa"
    message = "El següent usuari es vol donar de baixa:\n" + m.text

    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    server.quit()
    
    print ("successfully sent email to %s:" % (msg['To']))