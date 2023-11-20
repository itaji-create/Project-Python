import os
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)

# Definindo a variável de ambiente
os.environ['FLASK_DEBUG'] = 'True'

# Configurando o modo de depuração com base na variável de ambiente
app.debug = os.environ.get('FLASK_DEBUG') == 'True'


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/gerenciador')
def gerenciador():
    return render_template("gerenciador.html")

@app.route('/salvar', methods=['POST'])
def salvar():
    if request.method == 'POST':
        tarefa = request.form['tarefa']

        with open('tarefas.txt', 'a') as arquivo:
            arquivo.write(tarefa + '\n')

        print('Tarefa salva!')
        return render_template("gerenciador.html")

@app.route('/glossario')
def glossario():
    return render_template("glossario.html")

@app.route('/sobre')
def sobre():
    return render_template("sobre.html")

# Configurando a rota estática para arquivos CSS e imagens
@app.route('/css/<filename>')
def css(filename):
    return send_from_directory('templates/css', filename)

# Configurando a rota estática para arquivos de imagens na mesma pasta dos HTML
@app.route('/img/<filename>')
def img(filename):
    return send_from_directory('templates/img', filename)

if __name__ == "__main__":
    app.run()
