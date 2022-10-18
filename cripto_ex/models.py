import sqlite3
from config import ORIGIN_DATA, apikey
import requests

def select_all():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()

    result = cur.execute("SELECT id, date, time, moneda_from, cantidad_from, moneda_to, cantidad_to, (SELECT ROUND (cantidad_from / cantidad_to, 8)) as PU from movements order by date;")

    filas = result.fetchall() # lista de tuplas
    columnas = result.description #tupla de tuplas, description es un atributo del cursor

    resultado = []
    for fila in filas:
        posicion_columna = 0
        d = {}
        for campo in columnas:
            d[campo[0]] = fila[posicion_columna]
            posicion_columna += 1
        resultado.append(d)
    
    conn.close()
    
    return resultado

def calc_result(mfrom, mto, qnty):
    
    r = requests.get("https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}".format(mfrom, mto, apikey))
    dict_rate = r.json()

    rate = dict_rate["rate"]

    calc = rate * qnty

    return calc

# Lo que tiene que viajar es el diccionario

    
