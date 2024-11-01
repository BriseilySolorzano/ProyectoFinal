from flask import Flask, render_template

app = Flask(__name__)

@app.route('/inicio')
def index():
    return render_template('index.html')

@app.route('/grupo')
def pag1():
    return render_template('grupo.html')

@app.route('/jugar')
def pag2():
    return render_template('jugar.html')

@app.route('/letras')
def pag3():
    return render_template('letras.html')

@app.route('/selcNivel')
def pag4():
    return render_template('selecNivel.html')

@app.route('/nivelPri')
def pag5():
    return render_template('nivelPri.html')

if __name__ == '__main__':
    app.run(debug=True)
