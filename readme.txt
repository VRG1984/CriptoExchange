Para un correcto de funcionamiento de CriptoExchange, sigue atentamente estos sencillos pasos:

1.	Descarga el repositorio (“CriptoExchange”) de GitHub en tu PC.

2.	La carpeta “Data” contiene el fichero “movements.db”, no cambies el nombre de este fichero, se trata de la BBDD donde se grabará tus movimientos de criptos.

3.	Abre la carpeta “CriptoExchange” en tu editor de código.

4.	Abre un terminal de Python en tu editor de código y ejecuta el comando 'pip install -r requeriments.txt' para instalar todos los paquetes necesarios para el funcionamiento de CriptoExchange.

5.	Localiza el fichero “config_template” y renómbralo como “config.py”. Una vez hecho el cambio abre “config.py” en tu editor de código y edita, siguiendo las indicaciones y ejemplos, los 3 primeros campos: apikey, ORIGIN_DATA, SECRET_KEY.

•	Para obtener una apikey de CoinAPI.io pincha el siguiente enlace y completa el sencillo formulario que aparece en pantalla: https://www.coinapi.io/pricing?apikey. Una vez lo hagas, recibirás un email con tu apikey.
•	ORIGIN_DATA debe contener la ruta de tu PC donde se encuentra el fichero “movements.db” (si no realizas ningún cambio estará dentro de la carpeta “CriptoExchange” y la ruta será: “data/cripto_movements.db”) 
•	SECRET_KEY es una clave secreta a tú elección, intenta que contenga números, letras, mayúsculas y minúsculas y algún carácter especial para mayor seguridad. Ejemplos: ejemplo: “fghLY78_oP”

6.	Para finalizar, abre un terminal en tu editor de código y ejecuta el comando “flask run”. Esto creará un servicio virtual temporal para CriptoExchange. Observa que, una vez editado el comando, te devolverá una línea como esta “* Running on http://127.0.0.1:5000”. Quédate con los 4 últimos dígitos (en este caso sería “5000”) e introduce la siguiente dirección en tu navegador web: “localhost:5000”.

7.	Listo, ya estás ejecutando CriptoExchange, disfruta de la compra-venta de humo.
