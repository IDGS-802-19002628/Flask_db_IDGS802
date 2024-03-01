from flask import Flask, request, render_template, Response, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelomentConfig
from models import Alumnos

import forms
from flask import flash
from models import db
app = Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/index", methods=["GET", "POST"])
def index():
    alum_form = forms.UserForm(request.form)

    if request.method == 'POST' :
        alum = Alumnos(nombre=alum_form.nombre.data,
                       apaterno=alum_form.apaterno.data,
                       email=alum_form.email.data)
        # Insert
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template("index.html", form=alum_form)

@app.route("/eliminar", methods=("GET", "POST"))
def eliminar():

    alum_form = forms.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum_form.id.data = request.args.get('id')
        alum_form.nombre.data = alum1.nombre
        alum_form.apaterno.data = alum1.apaterno
        alum_form.email.data = alum1.email
    if request.method == "POST":
        id=alum_form.id.data
        alum=Alumnos.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('eliminar.html', form = alum_form)

@app.route("/modificar", methods=("GET", "POST"))
def modificar():

    alum_form = forms.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum_form.id.data = request.args.get('id')
        alum_form.nombre.data = alum1.nombre
        alum_form.apaterno.data = alum1.apaterno
        alum_form.email.data = alum1.email
    if request.method == "POST":
        id=alum_form.id.data

        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre = alum_form.nombre.data
        alum.apaterno = alum_form.apaterno.data
        alum.email = alum_form.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('eliminar.html', form = alum_form)

@app.route("/ABC_Completo",  methods=("GET", "POST"))
def ABCompleto():
    alum_form = forms.UserForm(request.form)
    alumno= Alumnos.query.all()
    return render_template('ABC_Completo.html', alumno=alumno)

@app.route("/alumnos", methods=("GET", "POST"))
def alumnos():
    print('dentro de ruta 2')
    nom = ''
    apaterno = ''
    correo = ''
    alum_forms = forms.UserForm(request.form)
    if request.method == 'POST':
        nom = alum_forms.nombre.data
        apaterno = alum_forms.apaterno.data
        correo = alum_forms.email.data
        messages = 'Bienvenido {}'.format(nom)
        flash(messages)
        print("Nombre: {}".format(nom))
        print("apaterno: {}".format(apaterno))
        print("correo: {}".format(correo))
        print(alum_forms.validate())
    return render_template("alumnos.html", form=alum_forms, nom=nom, apa=apaterno, c=correo)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
