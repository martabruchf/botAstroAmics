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
    msg['From'] = "bruchfigols@gmail.com"
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