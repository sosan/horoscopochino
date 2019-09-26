"""
HOROSCOPO CHINO
----
PROGRAMA DONDE INTRODUCIMOS EL AÑO DE NACIMIENTO
Y NOS DEVUELVE QUE HOROSCOPO CHINO SOMOS

"""

from flask import Flask, request, make_response, redirect, render_template, session, flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Regexp, InputRequired  # se puede modificar a nuestro gusto
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SECRET_KEY"] = "screto"
app.debug = True
toolbar = DebugToolbarExtension(app)

# constante
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


class FormularioHoroscopo(FlaskForm):
    campoAnyo = StringField("Año Nacimiento", validators=[DataRequired(),
                                                          Length(4, 5)
                                                          ])
    enviar = SubmitField("Enviar")


# RUTAS
# RUTA HOME
@app.route("/", methods=["GET", "POST"])
def home():
    formulario = FormularioHoroscopo()
    context = {
        "formulario": formulario

    }
    return render_template("index.html", datos=context)


# devolver datos del formualrio
@app.route("/rata", methods=["GET", "POST"])  # SI RECARGA LA PAGINA PODRIA DAR FALLO?
def rata():
    if request.method == "POST":

        try:
            datosFormulario = request.form

            anyoUsuario = int(datosFormulario["campoAnyo"])
            dato = calcularHoroscopoChino(anyoUsuario)
            # return "{0} / {1}" .format(dato[0], dato[1])
            nombreBicho = HOROSCOPO[dato[1]]

            context = {
                "error": dato[0],  # BOOL
                "data": dato[1],  # STR
                "nombreBicho": nombreBicho,  # STR
                "compatbilidad": COMPATIBLIDAD  # DIC

            }

            return render_template("rata.html", error=dato[0], data=dato[1], nombreBicho=nombreBicho,
                                   compatibilidad=COMPATIBLIDAD)  # dato0 es bool y dato1 es str
        except ValueError:
            return render_template("rata.html", error=True, data="Valor no posible convertir")

    else:
        redirect("/")


def calcularHoroscopoChino(añoNacimiento):
    if (añoNacimiento < 1900):
        return (True, "Año menor a 1900")
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
            return (False, count)
        else:
            return (True, "error. no ta en horoscopo")


# punot de entrada
if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
