import sqlite3
from cripto_ex import app
from cripto_ex.models import select_all
from cripto_ex.forms import CriptoForm
from flask import render_template, flash, request

@app.route("/")
def index():
        try:
                pageNow = "index"
                registros = select_all()
                return render_template("index.html", pageTitle="Inicio", pageNow=pageNow, data=registros)
        except sqlite3.Error as e:
                flash ("Se ha producido un error en la base de datos, contacte con el administrador")
                print(e)
                pageNow = "index"
                return render_template("index.html", pageTitle="Inicio", pageNow=pageNow, data=[])

@app.route("/purchase", methods= ["GET", "POST"])
def purchase():
        pageNow = "purchase"
        form = CriptoForm()

        if request.method == "GET":
                return render_template("purchase.html", pageTitle="Inicio", pageNow=pageNow, formulario = form)
        else:
                if form.validate():
                        # aquí cantidad_to y PU tienen que salir a partir del diccionario enviado
                        cantidad_to = calc_result(form.moneda_from.data, form.moneda_to.data, form.quantity_from.data)
                        return render_template("purchase.html", pageTitle="Inicio", pageNow=pageNow, formulario = form, cantidad_to = cantidad_to)



@app.route("/status")
def status():
        pageNow = "status"
        return render_template("status.html", pageTitle="Inicio", pageNow=pageNow)