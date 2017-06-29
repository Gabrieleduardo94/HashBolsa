#!/usr/bin/python3

# Este codigo tem como proposito de efetuar uma busca utilizando a estrutura de index
# sendo o Hash a opcao escolhida. Algumas informacoes deveram ser trocadas caso o arquivo
# de busca seja outra diferente do normal.
# 
# By:Gabriel Lima 
# 

import struct
import hashlib
import os
import sys
import time

ti = time.time()
 
hashSize = 15000001 #Tamanho da tabela de hash
fileName = "201701" #Arquivo onde as informacoes das pessoas estao.
indexName = "bolsa-hash201701.dat" #Arquivo onde contem indexado todas as entradas do bolsa familia
dataFormat = '2s30s14s50s6s2s' #Formato da estrutura do bolsa familia ja convertida de .dat
indexFormat = "14sLL" #Formato da estrutura do arquivo de hash
keyColumnIndex = 2 #Posicao do NIS (o que sera procurado e chave pelo qual foi indexado) na estrutura do bolsa familia
 
dataStruct = struct.Struct(dataFormat)
indexStruct = struct.Struct(indexFormat)

# Logica para descobrir em que posicao o nis foi armazenado no arquivo de hash.
def h(key):
    global hashSize
    return int(hashlib.sha1(key).hexdigest(),16)%hashSize
 
fi = open(indexName,"rb")
f = open(fileName,"rb")
 
if len(sys.argv) >= 2:
    nisProcurado = sys.argv[1]
else:
    nisProcurado = input("Entre com o NIS no seguinte formato 00000000000000 (14 digitos): ")
 
fi = open(indexName,"r+b")
p = h(bytearray(nisProcurado,encoding="cp1252"))
offset = p*indexStruct.size
i = 1
while True:
    fi.seek(offset,os.SEEK_SET)
    indexRecord = indexStruct.unpack(fi.read(indexStruct.size))
    if indexRecord[0].decode("cp1252") == nisProcurado:
        f.seek(indexRecord[1]*dataStruct.size,os.SEEK_SET)
        record = dataStruct.unpack(f.read(dataStruct.size))
        print ("Sigla estado: " + record[0].decode("cp1252"))
        print ("Rua: " + record[1].decode("cp1252"))
        print ("NIS: " + record[2].decode("cp1252"))
        print ("Nome: " + record[3].decode("cp1252"))
        print ("Valor: R$" + record[4].decode("cp1252"))
        print (i) #Contagem de acessos
        break
    offset = indexRecord[2]
    if offset == 0:
        print("Nis nao encontrado") #teste
        break
    i += 1
fi.close()

print(time.time() - ti)