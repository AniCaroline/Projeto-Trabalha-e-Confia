import requests
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

url = "https://trabalhavix.vitoria.es.gov.br/search.json"

querystring = {"length":"1000","start":"0"}

payload = "=funcao%3D&=escolaridade%3D&=municipio%3D&deficienciaFisica%5BvagaParaDeficiente%5B%5D%5D%5B%5D=1&deficienciaFisica%5BvagaParaDeficiente%5B%5D%5D%5B%5D=0&formulario=funcao%3D%26escolaridade%3D%26municipio%3D%26vinculo%3D%26_token%3D-y4w6txJI2YNx6lv2uqWnAg4TgSbew2udzXJHRGFPpQ"
headers = {
    "cookie": "TS01505dcc=01eac3dcd9228dedd7ae136f78db3b17e1b1f363de82d118e799fbd17479c5a6a9b70812f3150b5f28a33961cebd31c16c30eadf50d1c59ff4d84b783689d709c1aeb98775f6c731f011f3d724a5bc1e1d2a03d776dcd80e0de6a66ada6745edb1e3e19fe6",
    "Accept": "*/*",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_gid=GA1.4.1514089391.1696693879; _ga_J7WQCE6MYC=GS1.1.1696693908.1.0.1696693912.0.0.0; PHPSESSID=68q9tcc85q8sfi6cu8fr1v2aiv; _ga_WDTG4685XT=GS1.1.1696705481.1.1.1696705775.0.0.0; _ga_JMPB6Y7PZH=GS1.1.1696710149.3.1.1696710151.0.0.0; _ga=GA1.4.1543303145.1696693879; f5_cspm=1234; TS01505dcc=01eac3dcd98124e6b071879fcd2616a3f161a07d8fb5abf00ec25ea18d50f1ed7329d025229149cbfa8e5c39c0a0f57754606eacfeba57407a251540e63a3af3ac7e35822a49a4bb633be68c366576dcce0250ccae381cd013a3250342982fef035d3e3ad5",
    "Origin": "https://trabalhavix.vitoria.es.gov.br",
    "Referer": "https://trabalhavix.vitoria.es.gov.br/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

retornoAPI = response.json()

#cria uma lista vazia pra inserir as vagas
listaVagas = []

#percorre o retorno em JSON e vai inserindo os dados dentro da lista com os atributos que a gente precisa
for vaga in retornoAPI['data']:

    experiencia = 'Não'
    
    if(vaga['experiencia'] == True):
        experiencia = 'Sim'


    listaVagas.append([vaga['id'],vaga['idOrigem'],vaga['funcao']['descricao'],vaga['municipio']['descricao'],experiencia])

cnx = mysql.connector.connect(
    user='root',
    host='localhost',
    database='sistemasweb'
)

cursor = cnx.cursor()

delete = "DELETE FROM Vagas"
cursor.execute(delete)
cnx.commit()

query = "INSERT INTO vagas (id, idOrigem, funcao, municipio, experiencia) VALUES (%s, %s, %s, %s, %s)"

cursor.executemany(query, listaVagas)

cnx.commit()

cursor.close()
cnx.close()

print("Executado com sucesso")
