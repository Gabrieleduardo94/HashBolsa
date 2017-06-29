#! /usr/bin/python3

# Codigo que possui a funcao de converter o arquivo que e baixado diretamente 
# do portal de transparencia do Brasil, sendo que o mesmo vem no formato de .csv
# sendo isso este codigo tem o objetivo de apenas converter de .csv para .dat
# arquivo este que estara em binario.

import struct
import csv

# Define o formato da estrutura
estrutura = '2s30s14s50s6s2s'

#Cria a estrutura
s = struct.Struct(estrutura)

#Abre a planilha de Janeiro
print('Abrindo a planilha de janeiro')
f = open('201701_BolsaFamiliaFolhaPagamento.csv', encoding = 'cp1252')

#Escreve o dat da planilha de janeiro
print('Criando o arquivo dat de janeiro')
t = open('BolsaFamiliaJan.dat', 'wb')
print('Lendo a planilha')
r = csv.reader(f)

i = 1

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

	t.write(s.pack(bytearray(info[0], encoding = 'cp1252'),
                   bytearray(info[2], encoding = 'cp1252'),
                   bytearray(info[7], encoding = 'cp1252'),
                   bytearray(info[8], encoding = 'cp1252'),
                   bytearray(info[10], encoding = 'cp1252'),
                   bytearray('\n', encoding = 'cp1252')))
t.close()