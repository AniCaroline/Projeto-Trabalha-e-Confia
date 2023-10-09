from flask import Flask, Response
import mysql.connector
import json

app = Flask(__name__)
app.debug = True


@app.route('/dados', methods=['GET'])
def obter_dados():
    # Criar a conexão com o banco de dados
    cnx = mysql.connector.connect(
        user='root',
        host='localhost',
        database='sistemasweb'
    )
    
    # Criar o cursor
    cursor = cnx.cursor()
    
    # Executar a consulta SQL para obter os dados do banco de dados
    query = "SELECT * FROM vagas"
    cursor.execute(query)
    
    # Obter os dados do resultado da consulta
    dados = cursor.fetchall()
    
    # Converter os dados em formato JSON
    dados_json = []
    for registro in dados:
        dados_json.append({
            'id': registro[0],
            'idOrigem': registro[1],
            'funcao': registro[2],
            'municipio': registro[3],
            'experiencia': registro[4],
        })
    
    # Fechar o cursor e a conexão
    cursor.close()
    cnx.close()

    json_data = json.dumps(dados_json, ensure_ascii=False).encode('utf-8')
    
    # Retornar os dados em formato JSON
    response = Response(json_data, content_type='application/json; charset=utf-8')
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    return response

if __name__ == '__main__':
    app.run()