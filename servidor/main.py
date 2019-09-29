"""
HOROSCOPO CHINO
----
PROGRAMA DONDE INTRODUCIMOS EL AÑO DE NACIMIENTO
Y NOS DEVUELVE QUE HOROSCOPO CHINO SOMOS

"""
import os

from flask import Flask, request, make_response, redirect, render_template, session, flash, abort
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Regexp, InputRequired  # se puede modificar a nuestro gusto
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime

app = Flask(__name__)
# app.debug = True
# app.config["SECRET_KEY"] = "screto"
# toolbar = DebugToolbarExtension(app)

# constante

# dict: tuple
HOROSCOPO_v2 = {

    1: ("Rata", ("Dragon", 5), ("Mono", 9)),
    2: ("Buey", ("Serpiente", 6), ("Gallo", 10)),
    3: ("Tigre", ("Caballo", 7), ("Perro", 11)),
    4: ("Conejo", ("Cerdo", 12), ("Cabra", 8)),
    5: ("Dragon", ("Rata", 1), ("Mono", 9)),
    6: ("Serpiente", ("Buey", 2), ("Gallo", 10)),
    7: ("Caballo", ("Tigre", 3), ("Perro", 11)),
    8: ("Cabra", ("Conejo", 4), ("Cerdo", 12)),
    9: ("Mono", ("Rata", 1), ("Dragon", 5)),
    10: ("Gallo", ("Buey", 2), ("Serpiente", 6)),
    11: ("Perro", ("Tigre", 3), ("Caballo", 7)),
    12: ("Cerdo", ("Conejo", 4), ("Cabra", 8))

}

# mas adelante hacemos un zip entre horoscpoo y compatibilidad
HOROSCOPO = {
    1: "Rata",
    2: "Buey",
    3: "Tigre",
    4: "Conejo",
    5: "Dragon",
    6: "Serpiente",
    7: "Caballo",
    8: "Cabra",
    9: "Mono",
    10: "Gallo",
    11: "Perro",
    12: "Cerdo"

}

COMPATIBLIDAD = {
    1: ("Dragon", "Mono"),
    2: ("Serpiente", "Gallo"),
    3: ("Caballo", "Perro"),
    4: ("Cerdo", "Cabra"),
    5: ("Rata", "Mono"),
    6: ("Buey", "Gallo"),
    7: ("Tigre", "Perro"),
    8: ("Conejo", "Cerdo"),
    9: ("Rata", "Dragon"),
    10: ("Buey", "Serpiente"),
    11: ("Tigre", "Caballo"),
    12: ("Conejo", "Cabra")

}


class TemplateFormHoroscopo(FlaskForm):
    campoAnyo = StringField("Año Nacimiento", validators=[DataRequired(),
                                                          Length(4, 5)
                                                          ])

    enviar = SubmitField("Enviar")


# RUTAS
# RUTA HOME
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        templateFormulario = TemplateFormHoroscopo()

        # INICIO ---- insercion de diccionario HOROSCOPO Y los valores del dic COMPATIBILIDAD
        conjuntoDic = dict(zip(HOROSCOPO.values(), COMPATIBLIDAD.values()))
        for key in conjuntoDic:
            print("{0}=> {1}".format(key, conjuntoDic[key]))
        # --- FIN ----
        current_time = datetime.utcnow()
        print(current_time)

        context = {
            "templateFormulario": templateFormulario

        }
        return render_template("index.html", datos=context)
    else:
        abort(404)


# devolver datos del formualrio
@app.route("/rata", methods=["GET", "POST"])  # SI RECARGA LA PAGINA PODRIA DAR FALLO?
def rata():
    if request.method == "POST":

        try:
            datosFormulario = request.form

            anyoUsuarioInt = int(datosFormulario["campoAnyo"])
            # podria pasale tuplaDatos al jinja. mejor masticarlos? performance?
            tuplaDatos = calcularHoroscopoChino(anyoUsuarioInt)  # (True, str) o (True, int)

            context = {
                "errorBool": tuplaDatos[0],  # BOOL True / false
                "errorStr": tuplaDatos[1],  # STR del error
                "keyDict": tuplaDatos[2],  # INT. key del dict horoscopo 1,2,3,4,5...
                "dataHoroscopo": HOROSCOPO_v2[tuplaDatos[2]]  # ()
            }


            # se podria enviar mas masticado. pero para practicar lo complicamos un poco.

            # return render_template("rata.html", errorBool=tuplaDatos[0], errorStr=tuplaDatos[1],
            #             #                        dataHoroscopo=HOROSCOPO_v2[tuplaDatos[2]])

            return render_template("rata.html", datosHtml=context)


        except ValueError:
            return render_template("rata.html", errorBool=True, errorStr="Valor no posible convertir")

    else:
        redirect("/")


# funcion que calcula que horoscpo chinos eres
# ademas devuelve tuplas
# (BOOL, STR de error, INT key de horoscopo)
def calcularHoroscopoChino(añoNacimiento):
    if (añoNacimiento < 1900):
        return (True, "Año menor a 1900", 0)
    else:
        count = 1
        # mejor usar el añoNacimiento % len(HOROSCOPO)
        for i in range(1900, añoNacimiento):
            if añoNacimiento == i:
                # completado = True
                break;

            count += 1
            if count > 12:
                count = 1

        if count in HOROSCOPO:
            print("ERES DEL HOROSCOPO " + HOROSCOPO[count])
            return (False, "", count)
        else:
            return (True, "error. no ta en horoscopo", 0)


# errores
@app.errorhandler(404)
def error404(handler):
    return render_template("custom404.html")  # "Error custom 404"


# punot de entrada
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run("127.0.0.1", 5000, debug=True)
