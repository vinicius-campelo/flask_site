import sqlite3

connection = sqlite3.connect('dbase.db')
c = connection.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER UNIQUE, username TEXT NOT NULL, password_hash TEXT NOT NULL, nome TEXT NOT NULL, email TEXT NOT NULL, admin INTEGER DEFAULT 0, PRIMARY KEY(id AUTOINCREMENT))')

create_table()


def data_values():
    c.execute("INSERT INTO usuarios (username, password_hash, nome, email, admin) VALUES ('campelo', '260000$Nso4Os2lGQ8Rcfd0$1a24a3b145cb174b4de612d30ef24cd008390369846779fb871554d1105dd9b5', 'vinicius Campelo', 'autanbr@gmail.com', 0)")
    connection.commit()

data_values()



# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
