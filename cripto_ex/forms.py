from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from cripto_ex.models import validate_moneda_from, validate_moneda_to, validate_quantity_from

class CriptoForm(FlaskForm):
    moneda_from = SelectField("Moneda FROM", choices = ["EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC"], validators=[DataRequired(), validate_moneda_from])
    hidden_moneda_from = HiddenField()
    moneda_to = SelectField("Moneda TO", choices = ["EUR", "BTC", "ETH", "USDT", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC"], validators=[DataRequired(), validate_moneda_to])
    hidden_moneda_to = HiddenField()
    quantity_from = FloatField("Cantidad FROM", validators=[DataRequired(), validate_quantity_from])
    hidden_quantity_from = HiddenField()
    
    calc = SubmitField("CALC")
    
    submit = SubmitField("✓")