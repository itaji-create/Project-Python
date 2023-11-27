import os
import csv
from flask import Flask, render_template, send_from_directory, redirect, url_for, request

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
    with open('tarefas.txt', 'r') as arquivo:
        tarefas = arquivo.readlines()
    return render_template("gerenciador.html", tarefas=tarefas)

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

    glossario_de_termos = []

    with open(
            'bd_glossario.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            glossario_de_termos.append(l)

    return render_template('glossario.html',
                           glossario=glossario_de_termos)


@app.route('/novo_termo')
def novo_termo():
    return render_template('adicionar_termo.html')


@app.route('/criar_termo', methods=['POST', ])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open(
            'bd_glossario.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_glossario.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # Encontrar e excluir o termo com base no ID
    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break

    # Salvar as alterações de volta no arquivo
    with open('bd_glossario.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('glossario'))

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
