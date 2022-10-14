from cripto_ex import app
from cripto_ex.models import select_all
from flask import render_template

@app.route("/")
def index():
        pageNow = "index"
        registros = select_all()
        return render_template("index.html", pageTitle="Inicio", pageNow=pageNow, data=registros)

@app.route("/purchase")
def purchase():
        pageNow = "purchase"
        return render_template("purchase.html", pageTitle="Inicio", pageNow=pageNow)

@app.route("/status")
def status():
        pageNow = "status"
        return render_template("status.html", pageTitle="Inicio", pageNow=pageNow)