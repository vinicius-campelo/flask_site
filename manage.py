# from flask_script import Manager
from aplicacao.app import app, db
from aplicacao.model import *

# manager = Manager(app)
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['DEBUG'] = True


# @manager.command
# def create_tables():
#     "Create relational database tables."
#     db.create_all()
#     categoria=Categorias(id=0,nombre="Todos")
#     db.session.add(categoria)
#     db.session.commit()




if __name__ == '__main__':
    # manager.run()
     app.run(debug=True, port=5000)
