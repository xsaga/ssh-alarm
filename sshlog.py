#!/usr/bin/python3
"""Programa para controlar los intentos de acceso mediante SSH y enviar los resultados mediante correo electrónico.
El programa monitoriza '/var/log/auth.log' y extrae las entradas relevantes de sshd, extrae los nombres de usuario y
las direcciones IP para la geolocalización. El programa genera dos archivos '.ipdb' y 'sshlog.html'.
'.ipdb' es un archivo de texto con todas las direcciones IP que han intentado conectarse al ordenador y los datos de geolocalización.
'sshlog.html' contiene los datos relevantes de SSH, cada evento está codificado con colores según la importancia. Se envía por email.
"""
import re
import gemail
import ipinfo
import logging
import sys
import os

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s <%(levelname)s> %(message)s")

basepath = os.path.dirname(os.path.realpath(__file__))
ipdbpath = basepath + "/" + ".ipdb"
sshlogpath = basepath + "/" + "sshlog.html"

try:
    logfile = open(basepath+"/auth.log.example", "r") # CHANGE TO /var/log/auth.log
except:
    logging.error("No existe o incapaz de abrir '/var/log/auth.log'")
    sys.exit(1)

sshre = re.compile(r"sshd.*(Accepted|Invalid|Failed) password for (.*) from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
matches = []
for line in logfile:
    match = sshre.search(line)
    if match:
        matches.append((line, match))

logfile.close()

try:
    outfile = open(sshlogpath, "r")
except FileNotFoundError:
    logging.debug("'sshlog.html' no existe, creando...")
    open(sshlogpath, "w").close()
    outfile = open(sshlogpath, "r")


oldlog = outfile.readlines()
outfile.close()

try:
    ipfile = open(ipdbpath, "r")
except FileNotFoundError:
    logging.debug("'.ipdb' no existe, creando...")
    open(ipdbpath, "w").close()
    ipfile = open(ipdbpath, "r")

ipdb = {}
for line in ipfile:
    l = line.split(":")
    ipdb.setdefault(l[0].strip("\n "), eval(l[1].strip("\n ")))
ipfile.close()

if len(oldlog)-4 != len(matches): # len(oldlog) - 4 para no tener en cuenta los tags de html
    logging.debug("Actualizando 'sshlog.html'")
    outfile = open(sshlogpath, "w")
    
    outfile.write("<html>\n<body>\n")

    for line, match in matches:
        l = line.split()

        status = match.group(1)
        user = match.group(2)
        ip = match.group(3)

        if ip not in ipdb:
            logging.debug("No hay informacion sobre {} en '.ipdb', buscando...".format(ip))
            try:
                ipdb[ip] = ipinfo.get(ip)
            except:
                logging.warning("No se ha podido conseguir informacion sobre {}".format(ip))
                ipdb[ip] = [ip]+[""]*10

        location = " " + ipdb.get(ip)[ipinfo.COUNTRY_NAME] 
        if ipdb.get(ip)[ipinfo.CITY] not in ("PRIVATE", "OTHER", ""):
            location += ", city: {}".format(ipdb.get(ip)[ipinfo.CITY])

        color = "black"
        if status == "Accepted":
            if ipdb.get(ip)[ipinfo.COUNTRY_CODE] == "PRIVATE":
                color = "darkorange"
            else:
                color = "red"
        elif status == "Failed":
            if user.startswith("invalid user"):
                color = "blue"
            else:
                color = "gold"

        # " ".join(l[:len(l)-3]) para quitar la informacion del numero de puerto de ssh
        outfile.write("<p><font color={}>".format(color) + " ".join(l[:len(l)-3]) + location + "</font></p>\n")

    outfile.write("</body>\n</html>")
    outfile.close()

    outfile = open(sshlogpath, "r")
    message = outfile.read()
    outfile.close()
    gemail.sendme("ssh log", message, "html")
    logging.debug("mensaje enviado por email")

    ipfile = open(ipdbpath, "w")
    for ip, dsc in ipdb.items():
        ipfile.write("{}: {}\n".format(ip, dsc))
    ipfile.close()
    logging.debug("'.ipdb' actualizado")
