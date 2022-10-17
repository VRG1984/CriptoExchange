from flask import Flask

app = Flask(__name__, instance_relative_config=True) # Le dices a Flask que la configuración será relativa, esto es, que la vas a poder modificar parcialmente
app.config.from_object("config") # Método que le inyecta la clave que hay en "config.py", vía "from_object" autorizado relativamente (eso, vía "from_object") por el relative_config

from cripto_ex.routes import *