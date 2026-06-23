import psycopg2
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

clientes = []

DATABASE_URL = os.getenv("DATABASE_URL")

# 1 - Conectar ao banco de dados 
# 2 - Buscar todos os clientes 
# 3 - Retornar o resultado com todos os cliente (OBS: nesse caso como tem poucos registros podemos retornar todos, mas em um Banco que tem milhares podemos fazer por lote) 

try:

    connection = psycopg2.connect(DATABASE_URL)

    cursor = connection.cursor();

    cursor.execute('SELECT * FROM "Clientes" ')

    clientes = cursor.fetchall();
 

except:
    print('Erro ao conectar no banco de dados')


print("=========================Base de Clientes==========================")
print(*clientes,sep='\n');


#Envia Messagem via z-api

# 4 - Configurar a URL com o ID da instancia e o token 
# 5 - Selecionar cliente ou clientes 
# 6 -Enviar Mensagem viz z-api



ID_INSTANCIA = os.getenv("ID_INSTANCIA")
TOKEN_INSTANCIA = os.getenv("TOKEN_INSTANCIA")

url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN_INSTANCIA}/send-text"


# Aqui pode enviar para um cliente ou coloca o loop para enviar para todos os clientes da lista


#cliente_nome,cliente_numero = [clientes[2][2],clientes[2][3]]; #enviar para um unico cliente

for _,_,cliente_nome,cliente_numero in clientes: #Aqui vou enviar para varios contatos

    print("Cliente: " +cliente_nome + "Numero Contato: "+ cliente_numero)

    payload = json.dumps({
    "phone": "55"+cliente_numero,
    "message": "Olá, "+ cliente_nome+" tudo bem com você?",
    "delayMessage": 5
    })
    headers = {
    'Client-Token': '',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)





