from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, TextAreaField, SelectField, PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, NumberRange


class FormCategoria(FlaskForm):
    nome = StringField("Nome:", validators=[InputRequired("Adicione o nome!")])
    submit = SubmitField('Enviar')


class FormArtigo(FlaskForm):
    nome = StringField("Nome:", validators=[InputRequired("Adicione o nome!")])
    preco = DecimalField("Preco:", default=0, validators=[InputRequired("Adicione o preco!")])
    iva = IntegerField("IVA:", default=21, validators=[InputRequired("Adicione IVA!")])
    descricao = TextAreaField("Descricao:")
    foto = FileField("Selecione uma Imagem:")
    stock = IntegerField("Stock:", default=21, validators=[InputRequired("Adicione um valor")])
    CategoriaId = SelectField("Categoria:", coerce=int)
    submit = SubmitField('Enviar')


class FormSIMNAO(FlaskForm):
    sim = SubmitField('Sim')
    nao = SubmitField('Não')


class LoginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[InputRequired()])
    senha = PasswordField('Senha', validators=[InputRequired()])
    submit = SubmitField('Logar')


class FormUsuario(FlaskForm):
    username = StringField('Login', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    nome = StringField('Nome Completo')
    email = EmailField('Email')
    submit = SubmitField('Enviar')


class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Enviar')


class FormCarrinhoDeCompras(FlaskForm):
    id = HiddenField()
    quantidade = IntegerField('Quantidade', default=1, validators=[NumberRange(min=1, message="Deve ser um numero positivo"), InputRequired("Deve inserir um valor")])
    submit = SubmitField('Enviar')
