from crypt import methods
from flask import Flask, render_template, url_for, redirect, request
from aplicacao.forms import formArtigo, formCategoria
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from aplicacao import config
from werkzeug.utils import secure_filename
from os import listdir

app = Flask(__name__)
app.config.from_object(config)
Bootstrap(app)
db = SQLAlchemy(app)

from aplicacao.model import Artigos, Categorias

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


@app.route('/categorias')
def categorias():
    categorias = Categorias.query.all()
    return render_template('categorias.html', categorias=categorias)


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



@app.route('/artigos/new/', methods=['GET','POST'])
def artigos_new():
    form=formArtigo()
    categorias=[(c.id, c.nome) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        try:
            f=form.foto.data
            nome_ficheiro=secure_filename(f.filename)
            f.save(app.root_path+"/static/upload/"+nome_ficheiro)
        except:
            nome_ficheiro=""
            art=Artigos()
            form.populate_obj(art)
            art.image=nome_ficheiro
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('artigos.html', form=form)
            
            

@app.errorhandler(404)
def error_page_404(error):
    return render_template("error.html", error="Página não encontrada..."), 404