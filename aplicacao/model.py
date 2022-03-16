from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from aplicacao.app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Categorias(db.Model):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    artigos = relationship("Artigos", backref="Categorias", lazy='dynamic')

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


class Artigos(db.Model):
    __tablename__ = 'artigos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, default=0)
    iva = Column(Integer, default=21)
    descricao = Column(String(255))
    image = Column(String(255))
    stock = Column(Integer, default=0)
    CategoriaId = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    categoria = relationship("Categorias", backref="Artigos")

    def preco_final(self):
        return self.preco+(self.preco*self.iva/100)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))


class Usuarios(db.Model):
    """Usuarios"""
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(128), nullable=False)
    nome = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

    @property
    def password(self):
        return AttributeError('Senha não e um atributo legível')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
