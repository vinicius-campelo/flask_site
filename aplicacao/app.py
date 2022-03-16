from flask import Flask, render_template,redirect,url_for,request,abort
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from aplicacao import config
from aplicacao.forms import formCategoria, formArtigo,formSIMNAO, loginForm
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import os


app = Flask(__name__)
app.config.from_object(config)
csrf = CSRFProtect(app)
Bootstrap(app)
db = SQLAlchemy(app)

from aplicacao.model import Artigos, Categorias, Usuarios
from aplicacao.login import login_user, logout_user


@app.route('/categorias')
def categorias():
    categorias = Categorias.query.all()
    return render_template('categorias.html', categorias=categorias)


@app.route('/')
@app.route('/categoria/<id>')
def index(id = '0'):

    categoria = Categorias.query.get(id)
    if id == '0':
        artigos = Artigos.query.all()
    else:
        artigos = Artigos.query.filter_by(CategoriaId=id)
    categorias = Categorias.query.all()
    return render_template("index.html", artigos=artigos, categorias=categorias, categoria=categoria)


@app.route("/categorias/new/", methods=["GET", "POST"])
def categorias_new():
    form = formCategoria(request.form)
    if form.validate_on_submit():
        cat=Categorias(nome=form.nome.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for('categorias'))
    else:

        return render_template('categorias_new.html', form=form)


@app.route('/categorias/<id>/edit', methods=['GET','POST'])
def categorias_edit(id):
    cat = Categorias.query.get(id)
    if cat is None:
        abort(404)

    form = formCategoria(request.form, obj=cat)

    if form.validate_on_submit():

        form.id = cat
        cat.nome = form.nome.data
        form.populate_obj(cat)
        db.session.commit()
        return redirect(url_for('categorias'))

    return render_template('categorias_new.html', form=form)



@app.route('/categorias/<id>/delete', methods=["get","post"])
def categorias_delete(id):
    cat=Categorias.query.get(id)
    if cat is None:
        abort(404)
    form=formSIMNAO()
    if form.validate_on_submit():
        if form.sim.data:
            db.session.delete(cat)
            db.session.commit()
        return redirect(url_for("categorias"))
    return render_template("Categorias_delete.html", form=form, cat=cat)



@app.route('/artigos/new/', methods=['GET','POST'])
def artigos_new():
    form=formArtigo()
    categorias=[(c.id, c.nome) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        try:
            f=form.foto.data
            nome_ficheiro=secure_filename(f.filename)
            f.save(app.root_path+"/static/img/"+nome_ficheiro)
        except:
            nome_ficheiro=""
        art=Artigos()
        form.populate_obj(art)
        art.image=nome_ficheiro
        db.session.add(art)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('artigos_new.html', form=form)



@app.route('/artigos/<id>/edit',  methods=["GET","POST"])
def artigos_edit(id):
    art=Artigos.query.get(id)
    if art is None:
        abort(404)

    form=formArtigo(obj=art)
    categorias=[(c.id, c.nome) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = categorias

    if form.validate_on_submit():
        if form.foto.data:
            if art.image != "":
                if(os.path.isfile(app.root_path+"/static/img/"+art.image)):
                    os.remove(app.root_path+"/static/img/"+art.image)
            try:
                f = form.foto.data
                nome_ficheiro=secure_filename(f.filename)
                f.save(app.root_path+'/static/img/'+nome_ficheiro)
            except:
                nome_ficheiro =""
        else:
            nome_ficheiro=art.image

        form.populate_obj(art)
        art.image=nome_ficheiro
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('artigos_new.html', form=form)



@app.route('/artigos/<id>/delete', methods=['GET','POST'])
def artigos_delete(id):
    art=Artigos.query.get(id)
    if art is None:
        abort(404)

    form=formSIMNAO()
    if form.validate_on_submit():
        if form.sim.data:
            # if art.image != "":
            #     os.remove(app.root_path+"/static/img/"+art.image)
            db.session.delete(art)
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('artigos_delete.html', form=form, art=art)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user=Usuarios.query.filter_by(username=form.usuario.data).first()
        #if user and verify(form.senha.data) == True:
        if user and user.verify_password(form.senha.data):
            login_user(user)
            return redirect(url_for('index'))
        
        form.usuario.errors.append('Usuario ou senha incorretas!')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def error_page_404(error):
    return render_template("error.html", error="Página não encontrada..."), 404