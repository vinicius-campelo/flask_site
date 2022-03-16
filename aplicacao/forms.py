from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, TextAreaField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, PasswordField

class formCategoria(FlaskForm):
    nome = StringField("Nome:", validators=[InputRequired("Adicione o nome!")])
    submit = SubmitField('Enviar')


class formArtigo(FlaskForm):
    nome = StringField("Nome:", validators=[InputRequired("Adicione o nome!")])
    preco = DecimalField("Preco:", default=0, validators=[InputRequired("Adicione o preco!")])
    iva = IntegerField("IVA:", default=21, validators=[InputRequired("Adicione IVA!")])
    descricao = TextAreaField("Descricao:")
    foto = FileField("Selecione uma Imagem:")
    stock = IntegerField("Stock:", default=21, validators=[InputRequired("Adicione um valor")])
    CategoriaId=SelectField("Categoria:", coerce=int)
    submit = SubmitField('Enviar')

class formSIMNAO(FlaskForm):
    sim = SubmitField('Sim')
    nao = SubmitField('Não')

class loginForm(FlaskForm):
    usuario = StringField('Usuario', validators=[InputRequired()])
    senha = PasswordField('Senha', validators=[InputRequired()])
    submit = SubmitField('Logar')