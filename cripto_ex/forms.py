from multiprocessing.sharedctypes import Value
from optparse import Values
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class CriptoForm(FlaskForm):
    moneda_from = SelectField("Moneda FROM", choices = ["EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC"], validators=[DataRequired()])
    moneda_to = SelectField("Moneda TO", choices = ["EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC"], validators=[DataRequired()])
    quantity_from = FloatField("Cantidad FROM", validators=[DataRequired()])
    calc = SubmitField("CALC")
    
    submit = SubmitField("✓")
    