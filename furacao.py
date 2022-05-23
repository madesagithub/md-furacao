# import pandas as pd
import os
from typing import OrderedDict
import numpy as np
import pandas as pd

from prettytable import PrettyTable
from collections import defaultdict

from furadeiras import furadeiras	# lista de furadeiras
from Furadeira import Furadeira		# classe Furadeira
from Furo import Furo				# classe Furo
from Peca import Peca				# classe Peca		


# Arquivo
# --------------------
filename = 'DIVISÓRIA 12X387X1652.bpp'
filename = 'TAMPO MAL 15X440X2280.bpp'
filename = 'BASE 15X400X1046/BASE 15X400X1046.bpp'
filename = 'DIVISÓRIA BALCÃO 12X400X645/DIVISÓRIA BALCÃO 12X400X645.bpp'
filename = 'BASE AÉREO 12X266X1174/BASE AÉREO 12X266X1174.bpp'
filename = 'LATERAL DIR 15X544X2175/LATERAL DIR 15X544X2175.bpp'				# Complexo
dir = os.path.dirname(__file__) + '/Peças/'
file = open(dir + filename, 'r', encoding='latin1')
# --------------------


# Variáveis de configuração
# --------------------
furadeira = 'F500-B'
# --------------------


# Definição de variáveis
# --------------------
nro_cabecotes = furadeiras[furadeira]['nro_cabecotes']
posicao_cabecotes = furadeiras[furadeira]['posicao_cabecotes']
nro_mandris = furadeiras[furadeira]['nro_mandris']
distancia_mandris = furadeiras[furadeira]['distancia_mandris']
eixo_y = furadeiras[furadeira]['eixo_y']
# --------------------


# Cria furadeira
# --------------------
furadeira = Furadeira(furadeiras[furadeira])
# furadeira.imprimir_cabecotes()
# --------------------


# Varrer arquivo e encontrar furos
# --------------------
furos = []
array_furos = []
count = 0

# Varredura do arquivo
for line in file:
	if line.find("PAN=LPX") == 0:
		lpx = float(line.split('|')[1])
		lpx = round(lpx, 1)
	if line.find("PAN=LPY") == 0:
		lpy = float(line.split('|')[1])
		lpy = round(lpy, 1)
	if line.find("PAN=LPZ") == 0:
		lpz = float(line.split('|')[1])
		lpz = round(lpz, 1)

	if line.find("[PROGRAM]") == 0:
		flag_program = True
	elif 'flag_program' in locals() and flag_program:
		if line != '\n':
			nome = line.rstrip('\n').replace("'", "")
			flag_program = False

	if 'nome' in locals():
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
			# line[37]: "id"

			line = line.split(',')

			# Dados
			id = line[37].strip().replace('"', '')
			side = line[5].strip()
			crn = int(line[6].strip().replace('"', ''))
			x = float(line[7].strip())
			y = float(line[8].strip())
			z = float(line[9].strip())
			dp = float(line[10].strip())
			diametro = float(line[11].strip())
			p = int(line[12].strip())

			broca = str(diametro)
			if (p == 1):
				broca += 'T'

			# Cria o Furo
			furo = Furo(
				id,
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

			array_furos.append(furo)
		elif line == '\n' and len(array_furos) > 0:
			furos.append(array_furos)
			array_furos = []
# --------------------


# Imprimir tabela de dados da peça
# --------------------
peca = Peca(nome, lpx, lpy, lpz)
peca.imprimir_peca()


# Imprimir tabela de dados de furos
# --------------------
data = PrettyTable()
data.title = nome
data.field_names = ["Id", "Side", "CRN", "X", "Y", "Z", "DP", "Diametro", "P", "Broca"]
for array in furos:
	for i in array:
		data.add_row(list(i.__dict__.values()))
indice = ''
data._field_names.insert(0, indice)
data._align[indice] = 'c'
data._valign[indice] = 't'
for i, _ in enumerate(data._rows):
	data._rows[i].insert(0, i+1)
print(data)
# --------------------




furadeira.imprimir_furadeira()
furadeira.distribuir_furos(furos)
furadeira.imprimir_cabecotes()
furadeira.imprimir_cabecote(5)
exit()
# print(furos)







for side in furos:

	# Define a posição
	if side == '0 : 0':
		posicao = 'inferior'
		atributo = 'x'
	elif side == '0 : 1':
		posicao = 'esquerda'
		atributo = 'y'
	elif side == '0 : 2':
		posicao = ''
		atributo = ''
	elif side == '0 : 3':
		posicao = 'direita'
		atributo = 'y'
	elif side == '0 : 4':
		posicao = ''
		atributo = ''
	elif side == '0 : 5':
		posicao = 'superior'
		atributo = 'x'


	# Inferior
	# Superior
	# --------------------
	if side in ['0 : 0', '0 : 5']:
		# Agrupa furos por alinhamento
		groups = defaultdict(list)
		for array in furos[side]:
			x_array = list(set(list(furo.x for furo in array)))
			y_array = list(set(list(furo.y for furo in array)))

			if len(x_array) == 1:
				# Alinhado no eixo X
				groups['alinhado_x'].append(array)
				# groups[side].append(array)
			elif len(y_array) == 1:
				# Alinhado no eixo Y
				groups['alinhado_y'].append(array)
			else:
				# Não alinhado
				groups['nao_alinhado'].append(array)
		furos[side] = dict(groups.items())
		
		
		# print(groups)
		# exit()
		
		if 'alinhado_x' in furos[side]:
			# Agrupar por x
			groups = defaultdict(list)
			for array in furos[side]['alinhado_x']:
				for furo in array:
					groups[furo.x].append(furo)
			groups = dict(groups.items())

			# Ordenar
			groups = dict(OrderedDict(sorted(groups.items())))
			furos[side]['alinhado_x'] = groups


		# Ordenar
		# groups = dict(OrderedDict(sorted(groups.items())))

		print(furos[side])
		exit()

		# Provavelmente não haverá casos onde x tenha multiplos e não multiplos
		# Agrupar por múltiplos de distancia_mandris
		# groups_x_dp = {}
		# for x in list(groups_x.keys()):
		# 	groups_x_dp[x] = {'multiplos': [], 'não multiplos': []}
		# 	for furo in groups_x[x]:
		# 		if furo.y % distancia_mandris == 0:
		# 			groups_x_dp[x]['multiplos'].append(furo)
		# 		else:
		# 			groups_x_dp[x]['não multiplos'].append(furo)

		# Selecionar cabeçotes
		for x in groups:

			for cabecote in cabecotes:
				if cabecote.posicao == posicao and cabecote.used == False:
					break

			cabecote.use()
			cabecote.setX(x)

			# Aplica os furos
			for furo in groups[x]:
				cabecote.setMandril(furo, eixo_y)


























exit()



# Aplicar furos alinhados no eixo x
# Aplicar furos alinhados no eixo y


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



# Imprimir tabela de dados de furos
# --------------------
data = PrettyTable()
data.title = nome
data.field_names = ["Id", "Side", "CRN", "X", "Y", "Z", "DP", "Diametro", "P", "Broca"]
for i in furos:
	data.add_row(list(i.__dict__.values()))
indice = ''
data._field_names.insert(0, indice)
data._align[indice] = 'c'
data._valign[indice] = 't'
for i, _ in enumerate(data._rows):
	data._rows[i].insert(0, i+1)
print(data)
# --------------------














# Agrupar por side
groups = defaultdict(list)
for furo in furos:
	groups[furo.side].append(furo)
furos = dict(groups.items())






for side in furos:

	# Define a posição
	if side == '0 : 0':
		posicao = 'inferior'
		atributo = 'x'
	elif side == '0 : 1':
		posicao = 'esquerda'
		atributo = 'y'
	elif side == '0 : 2':
		posicao = ''
		atributo = ''
	elif side == '0 : 3':
		posicao = 'direita'
		atributo = 'y'
	elif side == '0 : 4':
		posicao = ''
		atributo = ''
	elif side == '0 : 5':
		posicao = 'superior'
		atributo = 'x'


	# Inferior
	# Superior
	# --------------------
	if side in ['0 : 0', '0 : 5']:
		# Agrupar por x
		groups = defaultdict(list)
		for furo in furos[side]:
			groups[furo.x].append(furo)
		groups = dict(groups.items())

		# Ordenar
		groups = dict(OrderedDict(sorted(groups.items())))

		# Provavelmente não haverá casos onde x tenha multiplos e não multiplos
		# Agrupar por múltiplos de distancia_mandris
		# groups_x_dp = {}
		# for x in list(groups_x.keys()):
		# 	groups_x_dp[x] = {'multiplos': [], 'não multiplos': []}
		# 	for furo in groups_x[x]:
		# 		if furo.y % distancia_mandris == 0:
		# 			groups_x_dp[x]['multiplos'].append(furo)
		# 		else:
		# 			groups_x_dp[x]['não multiplos'].append(furo)

		# Selecionar cabeçotes
		for x in groups:

			for cabecote in cabecotes:
				if cabecote.posicao == posicao and cabecote.used == False:
					break

			cabecote.use()
			cabecote.setX(x)

			# Aplica os furos
			for furo in groups[x]:
				cabecote.setMandril(furo, eixo_y)


	# Esquerda
	# Direita
	# --------------------
	# Inverte x e y????
	elif side == '0 : 1' or side == '0 : 3':
		# Agrupar por y
		groups = defaultdict(list)
		for furo in furos[side]:
			groups[furo.y].append(furo)
		groups = dict(groups.items())

		# Ordenar
		groups = dict(OrderedDict(sorted(groups.items())))

		# Selecionar cabeçotes
		for y in groups:

			for cabecote in cabecotes:
				if cabecote.posicao == posicao and cabecote.used == False:
					break

			cabecote.use()

			# Define a posição do primeiro e último cabeçote
			if posicao == 'esquerda':
				cabecote.setX(0)
			elif posicao == 'direita':
				cabecote.setX(lpx)

			# Aplica os furos
			for furo in groups[y]:
				cabecote.setMandril(furo, eixo_y, 'x')


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

# Imprimir tabela de cabeçotes
# --------------------
table = PrettyTable()
table.title = 'Cabeçotes'
table.field_names = list(cabecote.nro for cabecote in cabecotes)

# Brocas
for i in range(1, nro_mandris + 1):
	table.add_row(list(cabecote.brocas[i] for cabecote in cabecotes))

# Distancia x
table.add_row(list('---' for cabecote in cabecotes))
table.add_row(list(cabecote.x for cabecote in cabecotes))
table.add_row(list(cabecote.posicao[0:3] for cabecote in cabecotes))

# Índice
indice = ''
table._field_names.insert(0, indice)
table._align[indice] = 'c'
table._valign[indice] = 't'
for i, _ in enumerate(table._rows):
	if i < nro_mandris:
		if eixo_y == 'invertido':
			table._rows[i].insert(0, (len(table._rows) - 3 - i) * distancia_mandris)
		else:
			table._rows[i].insert(0, (i+1) * distancia_mandris)
	else:
		table._rows[i].insert(0, '')

print(table)
# --------------------