from aplicacao.app import app

app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['DEBUG'] = True


if __name__ == '__main__':
    app.run(debug=True, port=5000)