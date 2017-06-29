#!/usr/bin/python3

# Codigo que tem como proposito responder quantos registros possuem em um arquivo
# que nao possuem em outro. Neste caso seriam os reistro de Fevereiro do Bolsa Familia 
# e descobrir quantos estao em Fevereiro e nao estao em Janeiro. 
# Fazendo essa comparacao com o arquivo de Janeiro ja indexado com Hash.
# 
# By:Gabriel Lima

import struct
import hashlib
import os
import sys
import time

ti = time.time()
 
hashSize = 15000001
fileName2 = "201702"
indexName = "bolsa-hash201701.dat"
dataFormat = '2s30s14s50s6s2s'
indexFormat = "14sLL"
keyColumnIndex = 2
countEquals = 0
countDiference = 0
 
dataStruct = struct.Struct(dataFormat)
indexStruct = struct.Struct(indexFormat)
 
def h(key):
    global hashSize
    return int(hashlib.sha1(key).hexdigest(),16)%hashSize
 
f = open(fileName2,"rb")
fi = open(indexName,"r+b")
compare = f.read(dataStruct.size)
while len(compare) == 104:
    line = dataStruct.unpack(compare)
    nisProcurado = line[2]
    
    p = h(nisProcurado)
    offset = p*indexStruct.size
    while True:
        fi.seek(offset,os.SEEK_SET)
        indexRecord = indexStruct.unpack(fi.read(indexStruct.size))
        if indexRecord[0].decode("cp1252") == nisProcurado.decode("cp1252"):
            countEquals = countEquals + 1
            break      
        offset = indexRecord[2]
        if offset == 0:
            countDiference = countDiference + 1
            break
    compare = f.read(dataStruct.size)
print ("Quantidade de pessoas que estao em ambas as listas: %d" %countEquals) #Numero de acertos, possui nas duas tabelas
print ("Quantidade de pessoas que estao na lista de Fevereiro e nao estao em Janeiro: %d" %countDiference) #Numero de pessoas em Fevereiro que nao estao em Janeiro
f.close()
fi.close()

print(time.time() - ti)
