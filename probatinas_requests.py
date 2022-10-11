import requests
from config import apikey

r = requests.get("https://rest.coinapi.io/v1/exchangerate/{}?apikey={}".format("EUR", apikey))

monedas = ["BTC", "ETH", "BNB"]

resultados = r.json()
rates_now= []

for resultado in resultados["rates"]:
  if resultado["asset_id_quote"] in monedas:
    moneda = {resultado["asset_id_quote"] : resultado["rate"]}
    rates_now.append(moneda)

print(rates_now)

# Funciona, devuelve una lista con diccionarios {'nombre_moneda' : 'valor_moneda'} para cada una de las monedas
