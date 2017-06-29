#!/usr/bin/python3
import struct
import hashlib
import os
import csv
import sys
import time
 
ti = time.time()
hashSize = 15000001
dataFormat = '2s30s14s50s6s2s' #Formato da estrutura do arquivo do bolsa Familia ja convertido.
indexFormat = "14sLL" #Formato da estrutura que vai ser indexada 14s espaco do nis, L numero da linha, L ponteiro do registro no arquivo binario
keyColumnIndex = 2 #Posicao do nis na estrutura do arquivo do Bolsa Familia
 
dataStruct = struct.Struct(dataFormat)
indexStruct = struct.Struct(indexFormat)

#Verificacao se o comando possui argumentos
if len(sys.argv) != 2:
    print ("Comando incorreto! Tente: COMANDO [NOME_ARQUIVO]")
    quit()

try:
    #Abre a planilha de Janeiro
    print('Analisando o arquivo!')
    f = open(sys.argv[1], encoding = 'cp1252')
except:
    print ("Erro ao tentar abrir o Arquivo %s" %sys.argv[1])
    quit()

#Automatiza a nomeclatura dos arquivos
fileNameHash = sys.argv[1].split("_")
fileNameHash = fileNameHash[0]
fileName = fileNameHash
indexName = "bolsa-hash%s.dat" %fileNameHash

try:
    #Escreve o dat da planilha de janeiro
    print('Criando o arquivo dat do mes')
    t = open(fileNameHash, 'wb')
except:
    print ("Erro ao tentar abrir o Arquivo %s" %fileNameHash)
    quit()

print('Lendo a planilha')
r = csv.reader(f)

#Contador de linhas
i = 1

#Logica de conversao de .CSV para arquivos .DAT
for linha in r:
	if i == 1:
		i += 1
		continue
	
	if linha == "":  #EOF
		break

	i += 1

	info = linha[0].split('\t')
	
	if len(info[2]) < 30:
		info[2] = info[2] + ' ' * (30 - len(info[2]))

	if len(info[8]) < 50:
		info[8] = info[8] + ' ' * (50 - len(info[8]))

	if len(info[10]) < 6:
		info[10] = info[10] + ' ' * (6 - len(info[10]))

	t.write(dataStruct.pack(bytearray(info[0], encoding = 'cp1252'),
                   bytearray(info[2], encoding = 'cp1252'),
                   bytearray(info[7], encoding = 'cp1252'),
                   bytearray(info[8], encoding = 'cp1252'),
                   bytearray(info[10], encoding = 'cp1252'),
                   bytearray('\n', encoding = 'cp1252')))
t.close()

#Inicio da parte de indexacao da planilha do Bolsa Familia
##Classe que gera o numero hash
def h(key):
    global hashSize
    return int(hashlib.sha1(key).hexdigest(),16)%hashSize

try:
    fi = open(indexName,"wb+")
except:
    print ("Erro ao tentar abrir o Arquivo de hash")
    quit()

#Alocacao do arquivo de Hash com estrutura nulas
emptyIndexRecord = indexStruct.pack(bytearray("", encoding = 'cp1252'),0,0)
for i in range(0,hashSize):
    fi.write(emptyIndexRecord)
fi.close()

#abertura do arquivo do Bolsa Familia
try:
    f = open(fileName,"rb")
except:
    print ("Erro ao tentar abrir o Arquivo de hash")
    quit()

#Abertura do arquivo de Hash
try:
    fi = open(indexName,"r+b")
except:
    print ("Erro ao tentar abrir o Arquivo de hash")
    quit()


#Adquirindo o tamanho final do arquivo 
fi.seek(0,os.SEEK_END)
fileIndexSize = fi.tell()

#Logica de insercao no arquivo hash
recordNumber = 0
while True:
    line = f.read(dataStruct.size)
    if len(line) < 104: # EOF
        break
    record = dataStruct.unpack(line)
    p = h(record[keyColumnIndex])
    fi.seek(p*indexStruct.size,os.SEEK_SET)
    indexRecord = indexStruct.unpack(fi.read(indexStruct.size))
    fi.seek(p*indexStruct.size,os.SEEK_SET)
    print (indexRecord[0])
    print (indexRecord[0][0])
    if indexRecord[0][0] == 0:  #A comparacao tem que ser com zero, pois e retornado 0 como send o digito da tbela ascii
        fi.write(indexStruct.pack(record[keyColumnIndex],recordNumber,0))
    else:
        nextPointer = indexRecord[2]
        fi.write(indexStruct.pack(indexRecord[0],indexRecord[1],fileIndexSize))
        fi.seek(0,os.SEEK_END)
        fi.write(indexStruct.pack(record[keyColumnIndex],recordNumber,nextPointer))
        fileIndexSize = fi.tell()
    recordNumber += 1
f.close()
fi.close()

#Imprime o tempo que o codigo levou rodando na escala de segundos. 
print (time.time() - ti)  