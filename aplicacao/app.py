import json

from flask import Flask, render_template, redirect, url_for, request, abort, session, make_response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from aplicacao import config
from aplicacao.forms import FormCategoria, FormArtigo, FormSIMNAO, LoginForm, FormUsuario, FormChangePassword, FormCarrinhoDeCompras
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.config.from_object(config)
Bootstrap(app)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from aplicacao.model import Artigos, Categorias, Usuarios


# from aplicacao.login import login_user, logout_user, is_login, is_admin


@app.route('/categorias')
def categorias():
    cat = Categorias.query.all()
    return render_template('categorias.html', categorias=cat)


@app.route('/')
@app.route('/categoria/<id>')
def index(id='0'):
    cat = Categorias.query.get(id)
    if id == '0':
        artigos = Artigos.query.all()
    else:
        artigos = Artigos.query.filter_by(CategoriaId=id)
    cats = Categorias.query.all()
    return render_template("index.html", artigos=artigos, categorias=cats, categoria=cat)


@app.route("/categorias/new/", methods=["GET", "POST"])
@login_required
def categorias_new():
    # controle de permissão
    if not current_user.is_admin():
        abort(404)

    form = FormCategoria(request.form)
    if form.validate_on_submit():
        cat = Categorias(nome=form.nome.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for('categorias'))
    else:

        return render_template('categorias_new.html', form=form)


@app.route('/categorias/<id>/edit', methods=['GET', 'POST'])
@login_required
def categorias_edit(id):
    if not current_user.is_admin():
        abort(404)

    cat = Categorias.query.get(id)
    if cat is None:
        abort(404)

    form = FormCategoria(request.form, obj=cat)

    if form.validate_on_submit():
        form.id = cat
        cat.nome = form.nome.data
        form.populate_obj(cat)
        db.session.commit()
        return redirect(url_for('categorias'))

    return render_template('categorias_new.html', form=form)


@app.route('/categorias/<id>/delete', methods=["get", "post"])
@login_required
def categorias_delete(id):
    if not current_user.is_admin():
        abort(404)

    cat = Categorias.query.get(id)
    if cat is None:
        abort(404)
    form = FormSIMNAO()
    if form.validate_on_submit():
        if form.sim.data:
            db.session.delete(cat)
            db.session.commit()
        return redirect(url_for("categorias"))
    return render_template("Categorias_delete.html", form=form, cat=cat)


@app.route('/artigos/new/', methods=['GET', 'POST'])
@login_required
def artigos_new():
    if not current_user.is_admin():
        abort(404)

    form = FormArtigo()
    cat = [(c.id, c.nome) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = cat
    if form.validate_on_submit():
        try:
            f = form.foto.data
            nome_ficheiro = secure_filename(f.filename)
            f.save(app.root_path + "/static/img/" + nome_ficheiro)
        except:
            nome_ficheiro = ""
        art = Artigos()
        form.populate_obj(art)
        art.image = nome_ficheiro
        db.session.add(art)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('artigos_new.html', form=form)


@app.route('/artigos/<id>/edit', methods=["GET", "POST"])
@login_required
def artigos_edit(id):
    if not current_user.is_admin():
        abort(404)

    art = Artigos.query.get(id)
    if art is None:
        abort(404)

    form = FormArtigo(obj=art)
    cat = [(c.id, c.nome) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = cat

    if form.validate_on_submit():
        if form.foto.data:
            if art.image != "":
                if os.path.isfile(app.root_path + "/static/img/" + art.image):
                    os.remove(app.root_path + "/static/img/" + art.image)
            try:
                f = form.foto.data
                nome_ficheiro = secure_filename(f.filename)
                f.save(app.root_path + '/static/img/' + nome_ficheiro)
            except:
                nome_ficheiro = ""
        else:
            nome_ficheiro = art.image

        form.populate_obj(art)
        art.image = nome_ficheiro
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('artigos_new.html', form=form)


@app.route('/artigos/<id>/delete', methods=['GET', 'POST'])
@login_required
def artigos_delete(id):
    if not current_user.is_admin():
        abort(404)

    art = Artigos.query.get(id)
    if art is None:
        abort(404)

    form = FormSIMNAO()
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
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.usuario.data).first()
        if user and user.verify_password(form.senha.data):
            login_user(user)
            return redirect(url_for('index'))

        form.usuario.errors.append('Usuario ou senha incorretas!')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = FormUsuario()
    if form.validate_on_submit():
        existe_usuario = Usuarios.query.filter_by(username=form.username.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        form.username.errors.append("Nome de usuario não existe.")
    return render_template('usuario_new.html', form=form)


@app.route('/perfil/<username>', methods=['GET', 'POST'])
@login_required
def perfil(username):
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    form = FormUsuario(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('usuario_new.html', form=form, perfil=True)


@app.route('/changepassword/<username>', methods=['GET', 'POST'])
@login_required
def changepassword(username):
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)

    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('changepassword.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))


@app.route('/carrinho/add/<id>', methods=['GET', 'POST'])
@login_required
def carrinho_add(id):
    art = Artigos.query.get(id)
    form = FormCarrinhoDeCompras()
    form.id.data = id
    if form.validate_on_submit():
        if art.stock >= int(form.quantidade.data):
            try:
                dados_de_carrinho = json.loads(request.cookies.get(str(current_user.id)))
            except:
                dados_de_carrinho = []
            atualizar = False
            for dado in dados_de_carrinho:
                if dado['id'] == id:
                    dado['quantidade'] = form.quantidade.data
                    atualizar = True
            if not atualizar:
                dados_de_carrinho.append({'id': form.id.data, 'quantidade': form.quantidade.data})
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie(str(current_user.id), json.dumps(dados_de_carrinho))
            return resp
        form.quantidade.errors.append('Não tem produtos suficiente.')
    return render_template('carrinho_add.html', form=form, art=art)


@app.route('/carrinho')
@login_required
def carrinho():
    try:
        dados_de_carrinho = json.loads(request.cookies.get(str(current_user.id)))
    except:
        dados_de_carrinho = []
    artigos = []
    quantidade = []
    total = 0
    for artigo in dados_de_carrinho:
        artigos.append(Artigos.query.get(artigo['id']))
        quantidade.append(artigo['quantidade'])
        total = total+Artigos.query.get(artigo['id']).preco*artigo['quantidade']
    artigos = zip(artigos, quantidade)
    return render_template('carrinho.html', artigos=artigos, total=total)


@app.route('/carrinho_delete/<id>')
@login_required
def carrinho_delete(id):
    try:
        dados_de_carrinho = json.loads(request.cookies.get(str(current_user.id)))
    except:
        dados_de_carrinho = []
    dados_novos = []
    for dado in dados_de_carrinho:
        if dado['id'] != id:
            dados_novos.append(dado)
    resp = make_response(redirect(url_for('carrinho')))
    resp.set_cookie(str(current_user.id), json.dumps(dados_novos))
    return resp


@app.context_processor
def conta_carrinho():
    if not current_user.is_authenticated:
        return {'numero_do_artigo': 0}
    if request.cookies.get(str(current_user.id)) is None:
        return {'numero_do_artigo': 0}
    else:
        dados = json.loads(request.cookies.get(str(current_user.id)))
        return {'numero_do_artigo': len(dados)}


@app.route('/pedido')
@login_required
def pedido():
    try:
        dados_de_carrinho = json.loads(request.cookies.get(str(current_user.id)))
    except:
        dados_de_carrinho = []
    total = 0
    for artigo in dados_de_carrinho:
        total = total+Artigos.query.get(artigo['id']).preco*artigo['quantidade']
        Artigos.query.get(artigo['id']).stock-=artigo['quantidade']
        db.session.commit()
    resp = make_response(render_template('pedido.html', total=total))
    resp.set_cookie(str(current_user.id), "", expires=0)
    return resp


@app.errorhandler(404)
def error_page_404(error):
    return render_template("error.html", error="Página não encontrada..."), 404
