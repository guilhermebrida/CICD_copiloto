from flask import Flask
from flask import request
from flask import json
from pprint import pprint
import re
import JENKINS_PERFIL_PURO 
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
    return 'API GIT'


@app.route('/github', methods=['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        my_info = request.json
        pprint(my_info)
        file_name = my_info['head_commit']['modified'][0]  # pega o primeiro arquivo modificado
        print(file_name)        
        caminho = 'C:\\Python scripts'
        caminho_completo = procurar_arquivo(file_name, caminho)
        if caminho_completo is not None:
            print(f'O arquivo foi encontrado em: {caminho_completo}')
            JENKINS_PERFIL_PURO.GeraPerfil().main(caminho_completo)
        else:
            print(f'O arquivo {file_name} não foi encontrado em {caminho}.')
        return file_name

if __name__ == '__main__':
    app.run(debug=True)



