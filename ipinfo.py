#!/usr/bin/python3
"""Módulo para conseguir los datos de geolocalización desde una dirección IP."""
import ipaddress
import requests

IP, COUNTRY_CODE, COUNTRY_NAME, REGION_CODE, REGION_NAME, CITY, ZIP, TIMEZONE, LAT, LON, METRO = range(0,11)

def get(ip_addr):
    try:
        ipv4obj = ipaddress.IPv4Address(ip_addr)
    except AddressValueError:
        raise ValueError

    if ipv4obj.is_private:
        return [ip_addr]+["PRIVATE"]*10
    if not ipv4obj.is_global:
        return [ip_addr]+["OTHER"]*10

    # la ip es pública
    # freegeoip.net: 10000 llamadas por hora como máximo
    # si se supera ese límite el resultado es HTTP 403 forbidden
    response = requests.get("https://freegeoip.net/csv/"+ip_addr)
    response.raise_for_status()

    return response.text.replace("\r\n", "").split(",")

    

