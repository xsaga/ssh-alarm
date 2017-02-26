#!/usr/bin/python3
"""Módulo para enviar mensajes de correo desde una cuenta de Gmail usando smtplib.
Las credenciales de la cuenta de Gmail tienen que estar en un archivo '.gmail_login' en el mismo directorio que este módulo,
la primera línea del archivo tiene que ser la cuenta de correo (ej. cuenta@gmail.com) y la seguna línea la contraseña (ej. pass123).
"""

import smtplib
import sys
from email.mime.text import MIMEText

def getcredentials():
    """ Lee la cuenta de Gmail y la contraseña desde el archivo '.gmail_login'. """
    credentials = []
    try:
        f = open(".gmail_login", "r")
        for line in f:
            credentials.append(line.strip("\n "))
        f.close()
    except FileNotFoundError:
        sys.exit("No existe el archivo '.gmail_login' con los datos de la cuenta.")

    return credentials


def send(to_address, subject, message, content="plain"):
    """ Enviar el mensaje """
    login = getcredentials()
    if not to_address:
        to_address = login[0]

    msg = MIMEText(message, content)
    msg["Subject"] = subject
    msg["From"] = login[0]
    msg["To"] = to_address

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(login[0], login[1])
    server.send_message(msg)
    server.quit()
    login = []


def sendme(subject, message, content="plain"):
    send(None, subject, message, content)
