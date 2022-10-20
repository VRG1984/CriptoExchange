import sqlite3
from config import ORIGIN_DATA, apikey
import requests, datetime

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

def calc_result(mfrom, mto):
    
    r = requests.get("https://rest.coinapi.io/v1/exchangerate/{}/{}?apikey={}".format(mfrom, mto, apikey))
    return r.json()

# Lo que tiene que viajar es el diccionario

def disp_moneda_from(mfrom):
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()

    result = cur.execute("SELECT (SELECT sum (cantidad_to) FROM movements WHERE moneda_to = '{}') - (SELECT sum (cantidad_from) FROM movements WHERE moneda_from = '{}') AS disp;".format(mfrom, mfrom))
    disp = result.fetchone()

    conn.close()

    if disp[0] == None:
        return 0
    else:
        return disp[0]


def purchase_coin(mfrom, qfrom, mto, qto):

    date_time = datetime.datetime.now()
    date = date_time.strftime("%Y-%m-%d")
    time = date_time.strftime("%H:%M:%S")
    
    conn =sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()

    sql = ("INSERT INTO movements (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) values (?, ?, ?, ?, ?, ?)")
    val = (date, time, mfrom, qfrom, mto, qto)

    cur.execute(sql, val)

    conn.commit()
    conn.close()


    
    # Si tienes más disp que el PU (rate), te dejo realizar la transacción y la grabo