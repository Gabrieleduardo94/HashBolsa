#!/usr/bin/python3

# Este codigo tem como objetivo realizar uma comparacao de forca bruta entre dois arquivos 
# do bolsa familia, no qual ambos possuem pouco mais de 14 Milhoes de registros, ou seja,
# 14 milhoes de linhas sendo comparadas uma a uma com outras 14 milhoes.
# Atraves de comparacao podemos dizer quantos registros temos a mais em Fevereiro
# em relacao a Janeiro.
#
# By: Gabriel Lima

import struct
import hashlib
import os
import sys
import time

ti = time.time()
 
hashSize = 15000001
fileName1 = "201701" #Arquivo do bolsa familia .dat do mes de Janeiro
fileName2 = "201702" #Arquivo do bolsa familia .dat do mes de Fevereiro
dataFormat = '2s30s14s50s6s2s'
keyColumnIndex = 2
countEquals = 0
countDiference = 0

dataStruct = struct.Struct(dataFormat)

try:
    f = open(fileName1,"rb")
except:
    print("Erro ao tentar abrir o arquivo %s ! Verifique as permissoes do arquivo!" %fileName1)

try:
    fi = open(fileName2,"rb")
except:
    print("Erro ao tentar abrir o arquivo %s ! Verifique as permissoes do arquivo!" %fileName2)

lineJan = f.read(dataStruct.size)
lineFev = fi.read(dataStruct.size)
countin = 0
countout = 0

#while len(lineFev) == dataStruct.size:
while fi.tell() != (dataStruct.size*100001):
    
    while len(lineJan) >= 104 and fi.tell() != (dataStruct.size*100000): #EOF
        #while f.tell() != (dataStruct.size*1000000):
        if len(lineJan) < 104:
            break
        recordJan = dataStruct.unpack(lineJan)
        recordFev = dataStruct.unpack(lineFev)
        if (recordJan[keyColumnIndex] == recordFev[keyColumnIndex]):
            countEquals = countEquals + 1
            f.seek(0,os.SEEK_SET)
            lineJan = f.read(dataStruct.size)
            lineFev = fi.read(dataStruct.size)
            countin = countin + 1
            print (fi.tell())
            
        else:
            lineJan = f.read(dataStruct.size)
        
    countDiference = countDiference + 1
    countout = countout + 1
    print (countin)
    print (countout)
    f.seek(0,os.SEEK_SET)
    lineJan = f.read(dataStruct.size)
    lineFev = fi.read(dataStruct.size)
f.close()
fi.close()
print ("Esta e o numero de diferencas: %d" %countDiference)
print ("Esta e o numero de iguais: %d" %countEquals)
print (time.time() - ti)