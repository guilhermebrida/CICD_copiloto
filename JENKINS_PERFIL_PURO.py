from encodings import utf_8
import re
from pprint import pprint 
from tkinter import filedialog as dlg
import base64
import hashlib
from Crypto.Cipher import AES 
import json
from base64 import b64encode, b64decode
from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding
from datetime import date



class GeraPerfil():

    def main(self,caminho) -> None:
        self.path = caminho
        list_replace = [' VL12',' VL10',' VC5',' VL6',' VL8']
        self.tipo = 'Perfil'
        self.lista_comandos = []

        # self.path = dlg.askopenfilename()
        f=open(f'{self.path}', encoding='utf_8')
        self.tudo = f.read()
        self.tudo = re.sub('/.*','', self.tudo)
        comandos = (re.findall('>.*<',self.tudo))
        for i in range(len(comandos)):
            if i != (len(comandos)-1):
                self.lista_comandos.append(comandos[i]+';')
            if i == (len(comandos)-1):
                self.lista_comandos.append(comandos[i])

        self.buscaS3 = re.search('>TCFG13,9999<', self.tudo)
        self.buscaS1 = re.search('>SIS8.*<', self.tudo)
        self.buscaS4 = re.search('>SSB.*<', self.tudo)
        if self.buscaS4 is None:
            self.buscaS4 = re.search('VC5',self.path)

        self.buscaS8 = re.search('VL8', self.tudo)
        if self.buscaS8 is None:
            self.buscaS8 = re.search('VL8',self.path)

        self.path = str(self.path).split('\\')[-1].split('.')[0]
        self.idarquivo= self.path.replace('_',' ')
        for i in list_replace:
            self.idarquivo = self.idarquivo.replace(i,'')

        if self.buscaS3 is not None:
            ##### VARIAVEIS PARA CABEÇALHO 
            self.hardware = 'VIRLOC12'


            self.lim_vel= re.search('>SCT11.*<',self.tudo)
            if self.lim_vel is not None:
                self.lim_vel= re.search('>SCT11.*<',self.tudo).group()[7:-1]
                if str(len(self.lim_vel)) == '5':
                    self.lim_vel = self.lim_vel[0:2]
                else:
                    self.lim_vel = self.lim_vel[0:3]

            

            self.vel_evento= re.search('>SCT12.*<',self.tudo)
            if self.vel_evento is not None:
                self.vel_evento= re.search('>SCT12.*<',self.tudo).group()[7:-1]
                if str(len(self.vel_evento)) == '5':
                    self.vel_evento = self.vel_evento[0:2]
                if str(len(self.vel_evento)) == '6':
                    self.vel_evento = self.vel_evento[0:3]



            self.tempo_infra= re.search('>SCT06.*<',self.tudo)
            if self.tempo_infra is not None:
                self.tempo_infra= re.search('>SCT06.*<',self.tudo).group()[7:-1]



            self.mifare= re.search('>SSH11.*<',self.tudo)
            if self.mifare is not None:
                self.mifare= re.search('>SSH11.*<',self.tudo).group()[6]
                if self.mifare == '1':
                    self.mifare = 'Habilitado'
                else:
                    self.mifare = 'Desabilitado'
            else:
                self.mifare = 'Desabilitado' 


            self.versao= re.search('>STP01.*<',self.tudo)
            if self.versao is not None:
                self.versao1 = re.search('-+',self.versao.group())
                if self.versao1 is None:
                    self.versao1= re.search('>STP01.*<',self.tudo).group()
                    self.versao1= re.search('\d\d\d\d*',self.versao1).group()
                    self.versao = self.versao1
            else:
                self.versao = re.search('>STP03.*<',self.tudo)
                if self.versao is not None:
                    self.versao2 = re.search('-+',self.versao.group())
                    if self.versao2 is None:
                        self.versao2= re.search('\d\d\d\d*',self.versao.group()).group()
                        self.versao = self.versao2
            



            self.tablet = re.search('>SED169.*<', self.tudo)
            if self.tablet is not None:
                self.tablet = re.search('>SED169.*<', self.tudo).group()
                self.tabletN77 = re.search('TRM', self.tablet)
                if self.tabletN77 is not None:
                    self.tablet = 'N776/N77'
                self.tabletSAM = re.search('VCM_SL', self.tablet)
                if self.tabletSAM is not None:
                    self.tablet = 'SAMSUNG'
                self.SEMtablet = re.search('SGN NN', self.tablet)
                if self.SEMtablet is not None:
                    self.tablet = None
                
        elif self.buscaS1 is not None:
            ##### VARIAVEIS PARA CABEÇALHO 

            self.hardware = 'VIRLOC6'

            self.lim_vel= re.search('>VS08,100.*<',self.tudo)
            if self.lim_vel is not None:
                self.lim_vel= re.search('>VS08,100.*<',self.tudo).group()[10:13]
                if self.lim_vel[0] == '0':
                    self.lim_vel = re.sub(r'0', '', self.lim_vel, count = 1)


            

            self.tempo_infra= re.findall('>SCT06.*<',self.tudo)
            if ((self.tempo_infra is not None) and (self.tempo_infra !='0')):
                self.tempo_infra= re.findall('>SCT06.*<',self.tudo)[1]
                self.tempo_infra = self.tempo_infra[7:-1]



            self.mifare= re.search('>SSH11.*<',self.tudo)
            if self.mifare is not None:
                self.mifare= re.search('>SSH11.*<',self.tudo).group()[6]
                if self.mifare == '1':
                    self.mifare = 'Habilitado'
                else:
                    self.mifare = 'Desabilitado'
            else:
                self.mifare = 'Desabilitado' 


            self.versao= re.search('>SIS82.*<',self.tudo)
            if self.versao is not None:
                self.versao1 = re.search('-',self.versao.group())
                if self.versao1 is not None:
                    self.versao1 = re.search('-',self.versao1.group())
                else:    
                    self.versao1= re.search('>SIS82.*<',self.tudo).group()
                    self.versao1= re.search('\d\d\d\d*',self.versao1).group()
                    self.versao = self.versao1
            else:
                self.versao = re.search('>SIS84.*<',self.tudo)
                if self.versao is not None:
                    self.versao2 = re.search('>SIS84.*<',self.tudo).group()
                    if self.versao2 != '-':
                        self.versao2= re.search('\d\d\d\d*',self.versao2).group()
                        self.versao= self.versao2
            

            self.vel_evento = None
            self.tablet = None
            
        elif self.buscaS4 is not None:

            self.hardware = 'VIRCOM5'


            self.lim_vel= re.search('>SCT11.*<',self.tudo)
            if self.lim_vel is not None:
                self.lim_vel= re.search('>SCT11.*<',self.tudo).group()[7:-1]
                if str(len(self.lim_vel)) == '5':
                    self.lim_vel = self.lim_vel[0:2]
                else:
                    self.lim_vel = self.lim_vel[0:3]

            

            self.vel_evento= re.search('>SCT12.*<',self.tudo)
            if self.vel_evento is not None:
                self.vel_evento= re.search('>SCT12.*<',self.tudo).group()[7:-1]
                if str(len(self.vel_evento)) == '5':
                    self.vel_evento = self.vel_evento[0:2]
                if str(len(self.vel_evento)) == '6':
                    self.vel_evento = self.vel_evento[0:3]



            self.tempo_infra= re.search('>SCT06.*<',self.tudo)
            if self.tempo_infra is not None:
                self.tempo_infra= re.search('>SCT06.*<',self.tudo).group()[7:-1]


            self.mifare= re.search('>SSH11.*<',self.tudo)
            if self.mifare is not None:
                self.mifare= re.search('>SSH11.*<',self.tudo).group()[6]
                if self.mifare == '1':
                    self.mifare = 'Habilitado'
                else:
                    self.mifare = 'Desabilitado'
            else:
                self.mifare = 'Desabilitado'

            self.versao= re.search('>STP01.*<',self.tudo)
            if self.versao is not None:
                self.versao1 = re.search('-+',self.versao.group())
                if self.versao1 is None:
                    self.versao1= re.search('>STP01.*<',self.tudo).group()
                    self.versao1= re.search('\d\d\d\d*',self.versao1).group()
                    self.versao= self.versao1
            else:
                self.versao = re.search('>STP03.*<',self.tudo)
                if self.versao is not None:
                    self.versao2 = re.search('-+',self.versao.group())
                    if self.versao2 is None:
                        self.versao2= re.search('\d\d\d\d*',self.versao.group()).group()
                        self.versao = self.versao2

            self.tablet = None

        elif self.buscaS8 is not None:

            ##### VARIAVEIS PARA CABEÇALHO 
            self.hardware = 'VIRLOC8'

            self.lim_vel= re.search('>SCT11.*<',self.tudo)
            if self.lim_vel is not None:
                self.lim_vel= re.search('>SCT11.*<',self.tudo).group()[7:-1]
                if str(len(self.lim_vel)) == '5':
                    self.lim_vel = self.lim_vel[0:2]
                else:
                    self.lim_vel = self.lim_vel[0:3]

            

            self.vel_evento= re.search('>SCT12.*<',self.tudo)
            if self.vel_evento is not None:
                self.vel_evento= re.search('>SCT12.*<',self.tudo).group()[7:-1]
                if str(len(self.vel_evento)) == '5':
                    self.vel_evento = self.vel_evento[0:2]
                if str(len(self.vel_evento)) == '6':
                    self.vel_evento = self.vel_evento[0:3]



            self.tempo_infra= re.search('>SCT06.*<',self.tudo)
            if self.tempo_infra is not None:
                self.tempo_infra= re.search('>SCT06.*<',self.tudo).group()[7:-1]



            self.mifare= re.search('>SSH11.*<',self.tudo)
            if self.mifare is not None:
                self.mifare= re.search('>SSH11.*<',self.tudo).group()[6]
                if self.mifare == '1':
                    self.mifare = 'Habilitado'
                else:
                    self.mifare = 'Desabilitado'
            else:
                self.mifare = 'Desabilitado' 

            
            self.versao= re.search('>STP01.*<',self.tudo)
            if self.versao is not None:
                self.versao1 = re.search('-+',self.versao.group())
                if self.versao1 is None:
                    self.versao1= re.search('>STP01.*<',self.tudo).group()
                    self.versao1= re.search('\d\d\d\d*',self.versao1).group()
                    self.versao = self.versao1
            if self.versao is None:
                self.versao = re.search('>STP03.*<',self.tudo)
                if self.versao is not None:
                    self.versao2 = re.search('-+',self.versao.group())
                    if self.versao2 is None:
                        self.versao2= re.search('\d\d\d\d*',self.versao.group()).group()
                        self.versao = self.versao2
            print(self.versao)
            # versao =None
            # if versao is None:
            #     versao = str(date.today())
            #     versao = versao.replace('-','')[-6::]
            


            self.tablet = re.search('>SED169.*<', self.tudo)
            if self.tablet is not None:
                self.tablet = re.search('>SED169.*<', self.tudo).group()
                self.tabletN77 = re.search('TRM', self.tablet)
                if self.tabletN77 is not None:
                    self.tablet = 'N776/N77'
                self.tabletSAM = re.search('VCM_SL', self.tablet)
                if self.tabletSAM is not None:
                    self.tablet = 'SAMSUNG'
                self.SEMtablet = re.search('SGN NN', self.tablet)
                if self.SEMtablet is not None:
                    self.tablet = None
        
            
            
        else:

            ##### VARIAVEIS PARA CABEÇALHO 
            self.hardware = 'VIRLOC10"'+','+'"VIRLOC11'

            self.lim_vel= re.search('>SCT11.*<',self.tudo)
            if self.lim_vel is not None:
                self.lim_vel= re.search('>SCT11.*<',self.tudo).group()[7:-1]
                if str(len(self.lim_vel)) == '5':
                    self.lim_vel = self.lim_vel[0:2]
                else:
                    self.lim_vel = self.lim_vel[0:3]

            

            self.vel_evento= re.search('>SCT12.*<',self.tudo)
            if self.vel_evento is not None:
                self.vel_evento= re.search('>SCT12.*<',self.tudo).group()[7:-1]
                if str(len(self.vel_evento)) == '5':
                    self.vel_evento = self.vel_evento[0:2]
                if str(len(self.vel_evento)) == '6':
                    self.vel_evento = self.vel_evento[0:3]



            self.tempo_infra= re.search('>SCT06.*<',self.tudo)
            if self.tempo_infra is not None:
                self.tempo_infra= re.search('>SCT06.*<',self.tudo).group()[7:-1]


            self.mifare= re.search('>SSH11.*<',self.tudo)
            if self.mifare is not None:
                self.mifare= re.search('>SSH11.*<',self.tudo).group()[6]
                if self.mifare == '1':
                    self.mifare = 'Habilitado'
                else:
                    self.mifare = 'Desabilitado'
            else:
                self.mifare = 'Desabilitado'      



            self.versao= re.search('>STP01.*<',self.tudo)
            if self.versao is not None:
                self.versao1 = re.search('-+',self.versao.group())
                if self.versao1 is None:
                    self.versao1= re.search('>STP01.*<',self.tudo).group()
                    self.versao1= re.search('\d\d\d\d*',self.versao1).group()
                    self.versao = self.versao1
            else:
                self.versao = re.search('>STP03.*<',self.tudo)
                if self.versao is not None:
                    self.versao2 = re.search('-+',self.versao.group())
                    if self.versao2 is None:
                        self.versao2= re.search('\d\d\d\d*',self.versao.group()).group()
                        self.versao=self.versao2
            if self.versao is None:
                self.versao = str(date.today())
                self.versao = self.versao.replace('-','')[-6::]




            self.tablet = re.search('>SED169.*<', self.tudo)
            if self.tablet is not None:
                self.tablet = re.search('>SED169.*<', self.tudo).group()
                self.tabletN77 = re.search('TRM', self.tablet)
                if self.tabletN77 is not None:
                    self.tablet = 'N776/N77'
                self.tabletSAM = re.search('VCM_SL', self.tablet)
                if self.tabletSAM is not None:
                    self.tablet = 'SAMSUNG'
                self.SEMtablet = re.search('SGN NN', self.tablet)
                if self.SEMtablet is not None:
                    self.tablet = None

        self.cabeçalho = self.Json()
        self.Criar()
        comandos= self.message()
        AES_pkcs5_obj= AES_pkcs5(self.path,comandos)
        encrypted_message = AES_pkcs5_obj.encrypt(comandos)



    def Json(self,*args):
        if self.path is not None:
            idarq='{"idarquivo":"'+self.idarquivo+'",'
            Jtipo='"tipo":"'+self.tipo+'",'
            Jhardware='"hardware":["'+self.hardware+'"],'
            Jversao='"configs":[{"Versão":"'+self.versao+'"},'
            idarq2='{"idarquivo":"'+self.idarquivo+'"}'
            cabeçalho=idarq+Jtipo+Jhardware+Jversao+idarq2
            if self.tablet is not None:
                Jtablet=',{"Modelo Tablet":"'+self.tablet+'"}'
                cabeçalho=cabeçalho+Jtablet
            Jmifare=',{"Mifare":"'+self.mifare+'"}'
            cabeçalho = cabeçalho+Jmifare
            if self.lim_vel is not None:
                limiteVel=',{"limite Vel":"'+self.lim_vel+'"}'
                cabeçalho=cabeçalho+limiteVel
            if self.vel_evento is not None:
                velEvento=',{"limite Vel Evento":"'+self.vel_evento+'"}'
                cabeçalho=cabeçalho+velEvento
            if self.tempo_infra is not None:
                tempoInfra=',{"Tempo Infração":"'+self.tempo_infra+'"}'
                cabeçalho=cabeçalho+tempoInfra
            comandos='],"comandos":"'
            cabeçalho=cabeçalho+comandos
            print(cabeçalho)
        return cabeçalho

    def Criar(self,*args):
        f2=open (f'{self.path}.json','w',encoding='utf-8')
        f2.write(self.cabeçalho)
        for i in range(len(self.lista_comandos)):
            f2.write(self.lista_comandos[i]) 
        f2.write('"')
        hash = ',"hash":""}'
        f2.write(hash)
        f2.close()

    def message(self):
        f=open(f'{self.path}.json',encoding='utf_8')
        json_data=f.read()
        json_dict = json.loads(json_data)
        comandos=json_dict['comandos']
        return comandos

class AES_pkcs5():
    def __init__(self,path,key:str, mode:AES.MODE_CBC=AES.MODE_CBC,block_size:int=16):
        self.path = path
        self.key = self.setKey(key)
        self.mode = mode
        self.block_size = block_size



    def pad(self,byte_array:bytearray):
        pad_len = (self.block_size - len(byte_array) % self.block_size) *  chr(self.block_size - len(byte_array) % self.block_size)
        return byte_array.decode() +pad_len
    

    def unpad(self,byte_array:bytearray):
        return byte_array[:-ord(byte_array[-1:])]


    def setKey(self,key:str):
        self.key = key.encode('utf-8')
        md5 = hashlib.md5
        self.key = md5(self.key).digest()[:16]
        self.key = self.key.zfill(16)
        return self.key

    def encrypt(self,message:str)->str:
        iv = bytearray([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        byte_array = message.encode("UTF-8")
        padded = self.pad(byte_array)
        cipher = AES.new(self.key, AES.MODE_CBC,iv)
        encrypted = cipher.encrypt(padded.encode())
        encrypted64 = base64.b64encode(encrypted).decode('utf-8')
        f=open(f'{self.path}.json',encoding='utf_8')
        json_data=f.read()
        json_dict = json.loads(json_data)
        comandos=json_dict['comandos']
        json_dict.update(comandos=encrypted64)
        json_dict.update(hash=base64.b64encode(self.key).decode('utf-8'))
        f = open(f'{self.path}.json', 'w',encoding='utf-8')
        json.dump(json_dict, f,ensure_ascii=False)


        
# if __name__ == '__main__':
    # cabeçalho = Json()
    # Criar()
    # comandos=message()
    # AES_pkcs5_obj= AES_pkcs5(comandos)
    # encrypted_message = AES_pkcs5_obj.encrypt(comandos)



