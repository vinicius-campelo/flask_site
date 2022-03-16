#from flask_script import Manager
from aplicacao.app import app,db
from aplicacao.model import *
from getpass import getpass

#manager = Manager(app)

app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['DEBUG'] = True


#@manager.command
#def create_tables():
#     "Create relational database tables."
#     db.create_all()
#     categoria=Categorias(id=0,nombre="Todos")
#     db.session.add(categoria)
#     db.session.commit()


#@manager.command
#def create_admin():
#    usuario={
#        "username":input("Usuario:"),
#        "password":getpass("Senha:"),
#        "nome":input("Nome Completo:"),
#        "email":input("Email:"),
#        "admin":True
#    }
#    usu=Usuarios(**usuario)
#    db.session.add(usu)
#    db.session.commit()
    
  

if __name__ == '__main__':
     #manager.run()
     app.run(debug=True, port=5000)
