# import pandas as pd
from multiprocessing.pool import TERMINATE
import numpy as np
import pandas as pd

from prettytable import PrettyTable
from collections import defaultdict

from Cabecote import Cabecote
from Furo import Furo

# Variáveis de configuração
nro_cabecotes = 16
nro_brocas = 21
distancia_pinos = 32 # mm

posicao_cabecotes = {
    'esquerda': [1],
    'direita': [10],
    'inferior': list(range(2, 10)),
    'superior': list(range(11, 16)),
    'traseiro': list(range(16, 20))
}
# ----------

# Arquivo
filename = 'DIVISÓRIA 12X387X1652.bpp'
filename = 'TAMPO MAL 15X440X2280.bpp'
file = open(filename, 'r', encoding='latin1')
# ----------

# Definições
# Side 0 : 0 - Horizontal inferior
# Side 0 : 1 - Vertical esquerda
# Side 0 : 2 - 
# Side 0 : 3 - Vertical direita
# Side 0 : 4 - 
# Side 0 : 5 - Frontal

cabecotes = []
for i in range(1, nro_cabecotes + 1):
	for j in posicao_cabecotes:
		if i in posicao_cabecotes[j]:
			cabecote = Cabecote(i, nro_brocas, distancia_pinos, j)
			cabecotes.append(cabecote)
			break
	
	# vetor = np.array([0 for i in range(nro_pinos)])
	# vetor = np.array([0, 1, 2, 3])
	# print(vetor)
	# cabecotes[cabecote] = vetor

# furos = {}
# furos = np.array([])
# ----------

furos = []
count = 0
flag_program = False

for line in file:
	if line.find("PAN=LPX") == 0:
		lpx = line.split('|')[1]
	if line.find("PAN=LPY") == 0:
		lpy = line.split('|')[1]
	if line.find("PAN=LPZ") == 0:
		lpz = line.split('|')[1]

	if line.find("[PROGRAM]") == 0:
		flag_program = True
	elif flag_program:
		nome = line.rstrip('\n').replace("'", "")
		flag_program = False

	if line.find("@ BG") == 0:
		# line[ 0]: '@ BG'
		# line[ 1]: '""'
		# line[ 2]: '""'
		# line[ 3]: '37127068'
		# line[ 4]: '""'
		# line[ 5]: side
		# line[ 6]: crn
		# line[ 7]: x
		# line[ 8]: y
		# line[ 9]: z
		# line[10]: dp
		# line[11]: diametro
		# line[12]: p
		# line[13]: cabeçote

		line = line.split(',')

		# Dados
		side = line[5].removeprefix(' ')
		crn = int(line[6].removeprefix(' ').replace('"', ''))
		x = float(line[7].removeprefix(' '))
		y = float(line[8].removeprefix(' '))
		z = float(line[9].removeprefix(' '))
		dp = float(line[10].removeprefix(' '))
		diametro = float(line[11].removeprefix(' '))
		p = int(line[12].removeprefix(' '))

		broca = str(diametro)
		if (p == 1):
			broca += 'T'

		# Cria o Furo
		furo = Furo(
			side,
			crn,
			x,
			y,
			z,
			dp,
			diametro,
			p,
			broca
		)

		furos.append(furo)

# --------------------------------------------------

# Tabela da Peça
peca = PrettyTable()
peca.title = nome
peca.field_names = ['Dimensão', 'Valor (mm)']
peca.align = 'l'
peca.add_row(['Comprimento (X)', lpx])
peca.add_row(['Largura (Y)', lpy])
peca.add_row(['Espessura (Z)', lpz])
print(peca)
# ----------

# Tabela de dados
data = PrettyTable()
data.title = nome
data.field_names = ["Side", "CRN", "X", "Y", "Z", "DP", "Diametro", "P", "Broca"]
# data.field_names = list(furos[0].__dict__.keys())

for i in furos:
	data.add_row(list(i.__dict__.values()))

print(data)
# ----------

# Tabela de cabeçotes
table = PrettyTable()
table.title = 'Cabeçotes'
table.field_names = list(cabecote.nro for cabecote in cabecotes)

# Brocas
for i in range(1, nro_brocas + 1):
	table.add_row(list(cabecote.brocas[i] for cabecote in cabecotes))

# Distancia x
table.add_row(list('-' for cabecote in cabecotes))
table.add_row(list(cabecote.x for cabecote in cabecotes))
table.add_row(list(cabecote.posicao[0] for cabecote in cabecotes))
print(table)
# ----------












furos_bkp = []
arrays = []

# Ordenar por side
furos.sort(key=lambda furo: furo.side)

# Agrupar por side
groups = defaultdict(list)
for obj in furos:
	groups[obj.side].append(obj)
furos = list(groups.values())

# Ordenar por X
for array in furos:
	groups = defaultdict(list)
	for obj in array:
		groups[obj.x].append(obj)
	array = list(groups.values())
	arrays.append(array)


for array in arrays:
	for group in array:
		for furo in group:
			furos_bkp.append(furo)

furos = furos_bkp

# Tabela de dados
data = PrettyTable()
data.title = nome
data.field_names = ["Side", "CRN", "X", "Y", "Z", "DP", "Diametro", "P", "Broca"]
for i in furos:
	data.add_row(list(i.__dict__.values()))
print(data)



# Agrupar por X
# groups = defaultdict(list)
# for obj in furos:
#	 groups[obj.side].append(obj)
# new_list = list(groups.values())


# print(new_list[1][0].side)
data = PrettyTable()
data.title = filename
data.field_names = ["Side", "CRN", "X", "Y", "Z", "DP", "Diametro", "P", "Broca"]

# for i in furos:
# 	# data.add_row(list(furos[i].values))
# 	data.add_row(list(i.__dict__.values()))

# print(data)
# furos.map(key=lambda furo: furo.x)


from operator import itemgetter
from itertools import groupby

lki = [["A",0], ["B",1], ["C",0], ["D",2], ["E",2]]
lki.sort(key=itemgetter(1))

# print(lki)
# print(furos)
glo = [[x for x,y in g]
	   for k,g in  groupby(lki,key=itemgetter(1))]

# print(glo)