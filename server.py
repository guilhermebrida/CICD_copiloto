from flask import Flask
from flask import request
from flask import json
from pprint import pprint
import re
# import JENKINS_PERFIL_PURO 


import os

def procurar_arquivo(nome_arquivo, caminho):
    for dirpath, dirnames, filenames in os.walk(caminho):
        for filename in filenames:
            if filename == nome_arquivo:
                return os.path.join(dirpath, filename)
    return None

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'welcome'

@app.route('/github', methods=['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        my_info = request.json
        pprint(my_info)
        file_name = (my_info['head_commit']['modified'])
        # print((file_name))        
        return file_name

if __name__ == '__main__':
    app.run(debug=True)
    caminho = 'C:\\Python scripts'
    nome_arquivo = api_message()
    print(nome_arquivo.strip(''))
    caminho_completo = procurar_arquivo(nome_arquivo, caminho)
    if caminho_completo is not None:
        print(f'O arquivo foi encontrado em: {caminho_completo}')
    else:
        print(f'O arquivo {nome_arquivo} não foi encontrado em {caminho}.')
    # if api_message() is not None:
    #     cabeçalho = JENKINS_PERFIL_PURO.Json()
    #     JENKINS_PERFIL_PURO.Criar(cabeçalho)
    #     comandos=JENKINS_PERFIL_PURO.message()
    #     AES_pkcs5_obj= JENKINS_PERFIL_PURO.AES_pkcs5(comandos)
    #     encrypted_message = AES_pkcs5_obj.encrypt(comandos)


