#!/usr/bin/python3
"""Programa para conseguir la dirección IP pública de la máquina y enviarlo mediante correo electrónico cada vez que cambia.
También guarda un histograma de todas las IP-s públicas asignadas a este ordenador en el archivo '.pubiplist'.
"""
import requests
import gemail
import time
import ipinfo
import logging
import os

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s <%(levelname)s> %(message)s")

response = requests.get("http://icanhazip.com")
response.raise_for_status()
new_ip = response.text.strip("\n ")

basepath = os.path.dirname(os.path.realpath(__file__))
pubiplistpath = basepath + "/" + ".pubiplist"

try:
    f = open(pubiplistpath, "r")
except FileNotFoundError:
    logging.debug("'.pubiplist' no existe, creando...")
    f = open(pubiplistpath, "w")
    f.write("creado: {}\nactual: 0.0.0.0\n".format(time.asctime()))
    f.close()
    f = open(pubiplistpath, "r")

fecha = f.readline()
old_ip = f.readline().split(":")[1].strip("\n ")
hist = {}
for line in f:
    l = line.split(":")
    hist.setdefault(l[1].strip("\n "), int(l[0]))
f.close()

if new_ip != old_ip:
    logging.debug("la IP publica ha cambiado de {} a {}".format(old_ip, new_ip))
    try:
        msg = "\n".join(ipinfo.get(new_ip))
    except:
        logging.warning("No se ha podido conseguir informacion sobre {}".format(new_ip))
        msg = new_ip + "\n[Error en freegeoip.net]"
    gemail.sendme("public ip", msg)
    logging.debug("mensaje enviado por email")

    hist[new_ip] = hist.get(new_ip, 0) + 1
    f = open(pubiplistpath, "w")
    f.write(fecha)
    f.write("actual: {}\n".format(new_ip))
    for ip, cnt in sorted(hist.items(), key = lambda l : l[1], reverse = True):
        f.write("{}: {}\n".format(cnt, ip))
    f.close()
    logging.debug("histograma de IP-s actualizado")
