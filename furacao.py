# import pandas as pd
from typing import OrderedDict
import numpy as np
import pandas as pd

from prettytable import PrettyTable
from collections import defaultdict

from Cabecote import Cabecote
from Furo import Furo

# Arquivo
filename = 'DIVISÓRIA 12X387X1652.bpp'
filename = 'TAMPO MAL 15X440X2280.bpp'
file = open(filename, 'r', encoding='latin1')
# ----------

# Variáveis de configuração
furadeira = 'furadeira-2'

# Configuração de furadeiras
furadeiras = {
	'furadeira-1': {
		'nro_cabecotes': 19,
		'nro_brocas': 21,
		'distancia_pinos': 32,
		'posicao_cabecotes': {
			'esquerda': [1],
			'direita': [10],
			'inferior': list(range(2, 10)),
			'superior': list(range(11, 16)),
			'traseiro': list(range(16, 20)),
		},
	},
	'furadeira-2': {
		'nro_cabecotes': 16,
		'nro_brocas': 21,
		'distancia_pinos': 32,
		'posicao_cabecotes': {
			'esquerda': [1],
			'direita': [16],
			'inferior': list(range(2, 10)),
			'superior': list(range(10, 16)),
		},
	}
}
# ----------

# Definição de variáveis
nro_cabecotes = furadeiras[furadeira]['nro_cabecotes']
posicao_cabecotes = furadeiras[furadeira]['posicao_cabecotes']
nro_brocas = furadeiras[furadeira]['nro_brocas']
distancia_pinos = furadeiras[furadeira]['distancia_pinos']

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
		side = line[5].strip()
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
# --------------------
peca = PrettyTable()
peca.title = nome
peca.field_names = ['Dimensão', 'Valor (mm)']
peca.align = 'l'
peca.add_row(['Comprimento (X)', lpx])
peca.add_row(['Largura (Y)', lpy])
peca.add_row(['Espessura (Z)', lpz])
print(peca)
# --------------------


# Tabela de dados
# --------------------
data = PrettyTable()
data.title = nome
data.field_names = ["Side", "CRN", "X", "Y", "Z", "DP", "Diametro", "P", "Broca"]
# data.field_names = list(furos[0].__dict__.keys())

for i in furos:
	data.add_row(list(i.__dict__.values()))

print(data)
# --------------------













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














# Agrupar por side
groups = defaultdict(list)
for furo in furos:
	groups[furo.side].append(furo)
furos = dict(groups.items())






for side in furos:

	# Define a posição
	if side == '0 : 0':
		posicao = 'inferior'
	elif side == '0 : 1':
		posicao = 'esquerda'
	elif side == '0 : 2':
		posicao = ''
	elif side == '0 : 3':
		posicao = 'direita'
	elif side == '0 : 4':
		posicao = ''
	elif side == '0 : 5':
		posicao = 'superior'


	# Inferior
	# Superior
	# --------------------
	if side == '0 : 0' or side == '0 : 5':
		# Agrupar por x
		groups_x = defaultdict(list)
		for furo in furos[side]:
			groups_x[furo.x].append(furo)
		groups_x = dict(groups_x.items())

		# Ordenar
		groups_x = dict(OrderedDict(sorted(groups_x.items())))

		# Provávelmente não haverá casos onde x tenha multiplos e nçao multiplos
		# Agrupar por múltiplos de distancia_pinos
		# groups_x_dp = {}
		# for x in list(groups_x.keys()):
		# 	groups_x_dp[x] = {'multiplos': [], 'não multiplos': []}
		# 	for furo in groups_x[x]:
		# 		if furo.y % distancia_pinos == 0:
		# 			groups_x_dp[x]['multiplos'].append(furo)
		# 		else:
		# 			groups_x_dp[x]['não multiplos'].append(furo)

		# Selecionar cabeçotes
		for x in groups_x:

			for cabecote in cabecotes:
				if cabecote.posicao == posicao and cabecote.used == False:
					break
					
			cabecote.use()
			cabecote.setX(x)

			# Aplica os furos
			for furo in groups_x[x]:
				cabecote.setBroca(furo)
	

	# Esquerda
	# Direita
	# --------------------
	# Inverte x e y????
	elif side == '0 : 1' or side == '0 : 3':
		# Agrupar por y
		groups_y = defaultdict(list)
		for furo in furos[side]:
			groups_y[furo.y].append(furo)
		groups_y = dict(groups_y.items())

		# Ordenar
		groups_y = dict(OrderedDict(sorted(groups_y.items())))
		
		# Selecionar cabeçotes
		for y in groups_y:

			for cabecote in cabecotes:
				if cabecote.posicao == posicao and cabecote.used == False:
					break
					
			cabecote.use()
			cabecote.setX(y)

			# Aplica os furos
			for furo in groups_y[y]:
				cabecote.setBroca(furo, 'x')


	# Traseira
	# Frontal



# Ordenar por X
# for array in furos:
# 	groups = defaultdict(list)
# 	for obj in array:
# 		groups[obj.x].append(obj)
# 	array = list(groups.values())
# 	arrays.append(array)





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

# Tabela de cabeçotes
# --------------------
table = PrettyTable()
table.title = 'Cabeçotes'
table.field_names = list(cabecote.nro for cabecote in cabecotes)

# Brocas
for i in range(1, nro_brocas + 1):
	table.add_row(list(cabecote.brocas[i] for cabecote in cabecotes))

# Distancia x
table.add_row(list('-' for cabecote in cabecotes))
table.add_row(list(cabecote.x for cabecote in cabecotes))
table.add_row(list(cabecote.posicao[0:3] for cabecote in cabecotes))

# Índice
indice = ''
table._field_names.insert(0, indice)
table._align[indice] = 'c' 
table._valign[indice] = 't' 
for i, _ in enumerate(table._rows): 
	if i < nro_brocas: 
		table._rows[i].insert(0, (i+1) * distancia_pinos) 
	else:
		table._rows[i].insert(0, '') 

print(table)
# --------------------