from flask import Flask


app = Flask(__name__)
# from flask_script import Manager
#from aplicacao.app import app
#from aplicacao.model import *
#from getpass import getpass

# manager = Manager(app)
#app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#app.config['DEBUG'] = True

# @manager.command
# def create_tables():
#     "Create relational database tables."
#     db.create_all()
#     categoria=Categorias(id=0,nombre="Todos")

#     db.session.add(categoria)
#     db.session.commit()


# @manager.command
# def create_tables():
#     "Create table"
#     db.create_all()
#
#
# @manager.command
# def drop_tables():
#     "Drop table"
#     db.drop_all()
#
#
# @manager.command
# def add_data_tables():
#     "Add table"
#     db.create_all()
#
#     categorias = ("Todos", "Esporte", "Arcade", "Carreiras", "Ação")
#
#     for cat in categorias:
#         categoria = Categorias(nome=cat)
#         db.session.add(categoria)
#         db.session.commit()
#
#     jogos = [
#         {"nome": "Fernando Martín Basket", "preco": 12,
#          "descricao": "Fernando Martín Basket Master es un videojuego de baloncesto, uno contra uno, publicado por Dinamic Software en 1987",
#          "stock": 10, "CategoriaId": 1},
#         {"nome": "Hyper Soccer", "preco": 10,
#          "descricao": "Konami Hyper Soccer fue el primer videojuego de fútbol de Konami para una consola Nintendo, y considerado la semilla de las posteriores sagas International Superstar Soccer y Winning Eleven.",
#          "stock": 7, "CategoriaId": 1},
#         {"nome": "Arkanoid", "preco": 15,
#          "descricao": "Arkanoid es un videojuego de arcade desarrollado por Taito en 1986. Está basado en los Breakout de Atari de los años 70.",
#          "stock": 1, "CategoriaId": 2},
#         {"nome": "Tetris", "preco": 6,
#          "descricao": "Tetris es un videojuego de puzzle originalmente diseñado y programado por Alekséi Pázhitnov en la Unión Soviética.",
#          "stock": 5, "CategoriaId": 2},
#         {"nome": "Road Fighter", "preco": 15,
#          "descricao": "Road Fighter es un videojuego de carreras producido por Konami y lanzado en los arcades en 1984. Fue el primer juego de carreras desarrollado por esta compañía.",
#          "stock": 10, "CategoriaId": 3},
#         {"nome": "Out Run", "preco": 10,
#          "descricao": "Out Run es un videojuego de carreras creado en 1986 por Yū Suzuki y Sega-AM2, y publicado inicialmente para máquinas recreativas.",
#          "stock": 3, "CategoriaId": 3},
#         {"nome": "Army Moves", "preco": 8,
#          "descricao": "Army Moves es un arcade y primera parte de la trilogía Moves diseñado por Víctor Ruiz, de Dinamic Software para Commodore Amiga, Amstrad CPC, Atari ST, Commodore 64, MSX y ZX Spectrum en 1986.",
#          "stock": 8, "CategoriaId": 4},
#         {"nome": "La Abadia del Crimen", "preco": 4,
#          "descricao": "La Abadía del Crimen es un videojuego desarrollado inicialmente de forma freelance y publicado por la Academia Mister Chip en noviembre de 1987, posteriormente se publica bajo el sello de Opera Soft ya entrado 1988.",
#          "stock": 10, "CategoriaId": 4},
#     ]
#
#     for objJogo in jogos:
#         jogo = Artigos(**objJogo)
#         db.session.add(jogo)
#         db.session.commit()
#
#
# @manager.command
# def create_admin():
#    usuario={
#        "username": input("Usuario:"),
#        "password": getpass("Senha:"),
#        "nome": input("Nome Completo:"),
#        "email": input("Email:"),
#        "admin": True
#    }
#    usu = Usuarios(**usuario)
#    db.session.add(usu)
#    db.session.commit()

@app.route('/')
def ola_mundo():
    return "Ola mundo em python"


if __name__ == '__main__':
    # manager.run()
    app.run()
