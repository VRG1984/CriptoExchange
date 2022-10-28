import sqlite3
from tkinter import N
from config import CONSULTA_MONEDERO, ORIGIN_DATA, apikey
import requests, datetime
from wtforms.validators import ValidationError

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

def validate_moneda_from(form, field):
    if field.data != form.hidden_moneda_from.data:
        raise ValidationError("Debes volver a recalcular la transacción")

def validate_moneda_to(form, field):
    if field.data != form.hidden_moneda_to.data:
        raise ValidationError("Debes volver a recalcular la transacción")

def validate_quantity_from(form, field):
    # meter validación por si intentan calzar texto
    if field.data != float(form.hidden_quantity_from.data):
        raise ValidationError("Debes volver a recalcular la transacción")


#result = cur.execute("SELECT (SELECT sum (cantidad_from) FROM movements WHERE moneda_from = 'EUR' AS eur_inv;")

def eur_inv():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()

    result = cur.execute("SELECT (SELECT sum (cantidad_from) FROM movements WHERE moneda_from = 'EUR') AS eur_inv;")
    eur_inv = result.fetchone()

    conn.close()

    if eur_inv[0] == None:
        return 0
    else:
        return eur_inv[0]

def eur_rec():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()

    result = cur.execute("SELECT (SELECT sum (cantidad_to) FROM movements WHERE moneda_to = 'EUR') AS eur_rec;")
    eur_rec = result.fetchone()

    conn.close()

    if eur_rec[0] == None:
        return 0
    else:
        return eur_rec[0]

def valor_act():
    conn = sqlite3.connect(ORIGIN_DATA)
    cur = conn.cursor()

    result = cur.execute(CONSULTA_MONEDERO)

    filas = result.fetchone() # lista de tuplas
    columnas = result.description #tupla de tuplas, description es un atributo del cursor

    monedero = []

    posicion_fila = 0
    for campo in columnas:
        d = {}
        d[campo[0]] = filas[posicion_fila]
        posicion_fila += 1
        monedero.append(d)
    
    conn.close()
    
    return monedero
    

def get_rates():
    r = requests.get("https://rest.coinapi.io/v1/exchangerate/{}?apikey={}".format("EUR", apikey))

    monedas = ["BTC", "ETH", "BNB", "ADA", "DOT", "BTC", "USDT", "XRP", "SOL", "MATIC"]

    resultados = r.json()
    rates_now= []

    for resultado in resultados["rates"]:
        if resultado["asset_id_quote"] in monedas:
            moneda = {resultado["asset_id_quote"] : resultado["rate"]}
            rates_now.append(moneda)

    return rates_now

def valor_cartera():
    rates_now = get_rates()
    monedero = valor_act()

    valor_cartera = rates_now[0]['ADA'] * monedero[6]['ada'] + rates_now[1]['BNB'] * monedero[4]['bnb'] + rates_now[2]['BTC'] * monedero[1]['btc'] + rates_now[3]['DOT'] * monedero[8]['dot'] + rates_now[4]['ETH'] * monedero[2]['eth'] + rates_now[5]['MATIC'] * monedero[9]['matic'] + rates_now[6]['SOL'] * monedero[7]['sol'] + rates_now[7]['USDT'] * monedero[3]['usdt'] + rates_now[8]['XRP'] * monedero[5]['xrp']

    return valor_cartera
