import sqlite3
from cripto_ex import app
from cripto_ex.models import select_all
from flask import render_template, flash

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

@app.route("/purchase")
def purchase():
        pageNow = "purchase"
        return render_template("purchase.html", pageTitle="Inicio", pageNow=pageNow)

@app.route("/status")
def status():
        pageNow = "status"
        return render_template("status.html", pageTitle="Inicio", pageNow=pageNow)