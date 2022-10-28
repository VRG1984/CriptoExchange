import sqlite3
from cripto_ex import app
from cripto_ex.models import select_all, calc_result, disp_moneda_from, purchase_coin, eur_inv, eur_rec, valor_cartera
from cripto_ex.forms import CriptoForm
from flask import render_template, flash, request, redirect, url_for

@app.route("/")
def index():
        try:
                pageNow = "index"
                registros = select_all()
                return render_template("index.html", pageTitle="Inicio", pageNow=pageNow, data=registros)
        except Exception as e:
                flash ("Se ha producido un error en la base de datos, contacte con el administrador")
                print(e)
                pageNow = "index"
                return render_template("index.html", pageTitle="Inicio", pageNow=pageNow, data=[])

@app.route("/purchase", methods= ["GET", "POST"])
def purchase():
        pageNow = "purchase"
        form = CriptoForm()

        if request.method == "GET":
                return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
        else:   
                if request.values.get("calc"): 
                        if form.moneda_from.data != form.moneda_to.data:
                                if form.quantity_from.data is None:
                                        flash("La cantidad FROM debe ser un número decimal o entero")
                                        return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
                                else:
                                        form.hidden_moneda_from.data = form.moneda_from.data
                                        form.hidden_moneda_to.data = form.moneda_to.data
                                        form.hidden_quantity_from.data = form.quantity_from.data
                                
                                        if form.validate():
                                                try:
                                                        dict_rate = calc_result(form.moneda_from.data, form.moneda_to.data)
                                                        cantidad_to = dict_rate["rate"] * form.quantity_from.data
                                                        pu = form.quantity_from.data / cantidad_to
                                                        return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form, cantidad_to = cantidad_to, pu=pu)
                                                except Exception as e:
                                                        flash ("Se ha producido un error en la consulta de la API, contacte con CoinAPI.io")
                                                        print(e)
                                                        pageNow = "purchase"
                                                        return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
                                        else:
                                                flash("Se ha producido un error en la validación del formulario, inténtelo de nuevo")
                                                return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)      
                        else:       
                                flash("La moneda from y la moneda to no pueden ser la misma")
                                return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
                
                elif request.values.get("submit") and form.validate():
                        if form.moneda_from.data != "EUR":
                                
                                try:
                                        disp_m = disp_moneda_from(form.moneda_from.data)
                                        if disp_m > 0:
                                                try:
                                                        purchase_coin(form.moneda_from.data, form.quantity_from.data, form.moneda_to.data, cantidad_to)
                                                        return redirect(url_for("index"))
                                                except Exception as e:
                                                        flash("Se ha producido un error en la base de datos, contacte con el administrador")
                                                        print(e)
                                                        pageNow = "purchase"
                                                        return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
                                        else:
                                                flash("No tiene suficientes {} para comprar".format(form.moneda_from.data))
                                                return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
                                
                                except Exception as e:
                                        flash ("Se ha producido un error en la base de datos, contacte con el administrador")
                                        print(e)
                                        pageNow = "purchase"
                                        return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
                                
                        else:
                                
                                try:
                                        dict_rate = calc_result(form.moneda_from.data, form.moneda_to.data)
                                except Exception as e:
                                        flash ("Se ha producido un error en la consulta de la API, contacte con CoinAPI.io")
                                        print(e)
                                        pageNow = "purchase"
                                        return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
                                cantidad_to = dict_rate["rate"] * form.quantity_from.data
                                
                                try:
                                        purchase_coin(form.moneda_from.data, form.quantity_from.data, form.moneda_to.data, cantidad_to)
                                        return redirect(url_for("index"))
                                except Exception as e:
                                        flash ("Se ha producido un error en la base de datos, contacte con el administrador")
                                        print(e)
                                        pageNow = "purchase"
                                        return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)
                else:
                        return render_template("purchase.html", pageTitle="Purchase", pageNow=pageNow, formulario = form)

# TODOS LOS ERRORES CONTROLADOS HASTA AQUÍ

@app.route("/status")
def status():
        pageNow = "status"
        euros_inv = eur_inv()
        euros_rec = eur_rec()
        valor_compra = euros_inv-euros_rec
        valor_actual = valor_cartera()
        ganancia = valor_actual - valor_compra
        
        return render_template("status.html", pageTitle="Status", pageNow=pageNow, euros_inv=euros_inv, euros_rec=euros_rec, valor_compra=valor_compra, valor_actual=valor_actual, ganancia = ganancia)

        #terminar la parte optativa de status, gestión de errores y al readme 