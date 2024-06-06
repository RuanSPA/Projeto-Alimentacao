from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configurações de conexão com o banco de dados SQL Server
server = 'NB-DATACOM-26'
database = 'ALIMENTACAO_TESTE'
username = 'ALIMENTACAO'
password = 'alitecsys'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Doacoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_doacao = db.Column(db.String(50))
    valor = db.Column(db.Float)
    cpf = db.Column(db.String(11), db.ForeignKey('dados_doador.cpf'))
    forma_pagamento = db.Column(db.String(50))

class DadosDoador(db.Model):
    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    sexo = db.Column(db.String(20))
    receber_impacto = db.Column(db.Boolean)

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), db.ForeignKey('dados_doador.cpf'))
    cep = db.Column(db.String(10))
    rua = db.Column(db.String(100))
    numero_casa = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))

# Rotas para inserção de dados
@app.route('/cadastrar_doador', methods=['POST'], url_prefix='http://127.0.0.1:5000/cadastrar_doador')
def cadastrar_doador():
    data = request.json

    novo_doador = DadosDoador(
        cpf=data['cpf'],
        nome=data['nome'],
        email=data['email'],
        telefone=data['telefone'],
        data_nascimento=data['data_nascimento'],
        sexo=data['sexo'],
        receber_impacto=data['receber_impacto']
    )

    db.session.add(novo_doador)
    db.session.commit()

    return jsonify({"message": "Doador cadastrado com sucesso!"}), 201

@app.route('/cadastrar_doacao', methods=['POST'], url_prefix='http://127.0.0.1:5000/cadastrar_doacao')
def cadastrar_doacao():
    data = request.json

    nova_doacao = Doacoes(
        tipo_doacao=data['tipo_doacao'],
        valor=data['valor'],
        cpf=data['cpf'],
        forma_pagamento=data['forma_pagamento']
    )

    db.session.add(nova_doacao)
    db.session.commit()

    return jsonify({"message": "Doação cadastrada com sucesso!"}), 201

@app.route('/cadastrar_endereco', methods=['POST'], url_prefix='http://127.0.0.1:5000/cadastrar_endereco')
def cadastrar_endereco():
    data = request.json

    novo_endereco = Endereco(
        cpf=data['cpf'],
        cep=data['cep'],
        rua=data['rua'],
        numero_casa=data['numero_casa'],
        complemento=data['complemento'],
        bairro=data['bairro'],
        cidade=data['cidade'],
        estado=data['estado']
    )

    db.session.add(novo_endereco)
    db.session.commit()

    return jsonify({"message": "Endereço cadastrado com sucesso!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
