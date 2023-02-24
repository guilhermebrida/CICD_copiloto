# from flask import Flask
# from flask import request
# from flask import json
# from pprint import pprint
# import re
# import JENKINS_PERFIL_PURO 
# import os
# from flask import redirect, url_for



# def procurar_arquivo(nome_arquivo, caminho):
#     for dirpath, dirnames, filenames in os.walk(caminho):
#         for filename in filenames:
#             if filename == nome_arquivo:
#                 return os.path.join(dirpath, filename)
#     return None

# app = Flask(__name__)

# @app.route('/')
# def api_root():
#     return 'API GIT'



# @app.route('/github', methods=['POST'])
# def api_message():
#     if request.headers['Content-Type'] == 'application/json':
#         my_info = request.json
#         pprint(my_info)
#         file_name = my_info['head_commit']['modified'][0]  # pega o primeiro arquivo modificado
#         print(file_name)        
#         caminho = 'C:\\'
#         caminho_completo = procurar_arquivo(file_name, caminho)
#         if caminho_completo is not None:
#             print(f'O arquivo foi encontrado em: {caminho_completo}')
#             JENKINS_PERFIL_PURO.GeraPerfil().main(caminho_completo)
#         else:
#             print(f'O arquivo {file_name} não foi encontrado em {caminho}.')
#         return file_name
    
# # @app.route('/encontrar-arquivo', methods=['POST'])
# # def encontrar_arquivo():
# #     my_info = request.json
# #     file_name = my_info['head_commit']['modified'][0]  # pega o primeiro arquivo modificado
# #     caminho = 'C:\\Python scripts'
# #     caminho_completo = procurar_arquivo(file_name, caminho)
# #     if caminho_completo is not None:
# #         print(f'O arquivo foi encontrado em: {caminho_completo}')
# #         return redirect(url_for('arquivo_encontrado', nome=file_name))
# #     else:
# #         print(f'O arquivo {file_name} não foi encontrado em {caminho}.')
# #         return f'O arquivo {file_name} não foi encontrado em {caminho}.'

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, request, json, redirect, url_for
from pprint import pprint
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
    return 'Bem-vindo!'

@app.route('/arquivo-encontrado')
def arquivo_encontrado():
    nome_arquivo = request.args.get('nome')
    return f'O arquivo encontrado é: {nome_arquivo}'

@app.route('/encontrar-arquivo', methods=['POST'])
def encontrar_arquivo():
    my_info = request.json
    file_name = my_info['head_commit']['modified'][0]  # pega o primeiro arquivo modificado
    caminho = 'C:\\'
    caminho_completo = procurar_arquivo(file_name, caminho)
    if caminho_completo is not None:
        print(f'O arquivo foi encontrado em: {caminho_completo}')
        return redirect(url_for('arquivo_encontrado', nome=file_name))
    else:
        print(f'O arquivo {file_name} não foi encontrado em {caminho}.')
        return f'O arquivo {file_name} não foi encontrado em {caminho}.'

if __name__ == '__main__':
    app.run(debug=True)



