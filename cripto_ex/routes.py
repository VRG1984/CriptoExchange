import sqlite3
from cripto_ex import app
from cripto_ex.models import select_all, calc_result, disp_moneda_from, purchase_coin
from cripto_ex.forms import CriptoForm
from flask import render_template, flash, request, redirect, url_for

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
                dict_rate = calc_result(form.moneda_from.data, form.moneda_to.data)
                cantidad_to = dict_rate["rate"] * form.quantity_from.data
                pu = form.quantity_from.data / cantidad_to
                
                if request.values.get("calc") and form.validate():
                        if form.moneda_from.data != form.moneda_to.data:
                                return render_template("purchase.html", pageTitle="Inicio", pageNow=pageNow, formulario = form, cantidad_to = cantidad_to, pu=pu)

                        else:
                             flash("La moneda from y la moneda to no pueden ser la misma")
                             return render_template("purchase.html", pageTitle="Inicio", pageNow=pageNow, formulario = form)
                
                elif request.values.get("submit") and form.validate():
                        if form.moneda_from.data != "EUR":
                                disp_m = disp_moneda_from(form.moneda_from.data)
                                if disp_m > 0:
                        # Tengo que sacar el pu (y todo lo demás) arriba, fuera del elif
                                        purchase_coin(form.moneda_from.data, form.quantity_from.data, form.moneda_to.data, cantidad_to)
                                        return redirect(url_for("index"))
                                else:
                                        flash("No tiene suficientes {} para comprar".format(form.moneda_from.data))
                                        return render_template("purchase.html", pageTitle="Inicio", pageNow=pageNow, formulario = form)
                        else:
                                purchase_coin(form.moneda_from.data, form.quantity_from.data, form.moneda_to.data, cantidad_to)
                                return redirect(url_for("index"))  
                else:
                        flash("Se ha producido un error en la consulta, contacte con el administrador")
                        return render_template("purchase.html", pageTitle="Inicio", pageNow=pageNow, formulario = form)

                
@app.route("/status")
def status():
        pageNow = "status"
        return render_template("status.html", pageTitle="Inicio", pageNow=pageNow)