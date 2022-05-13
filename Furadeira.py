import math
from prettytable import PrettyTable
from collections import defaultdict
from typing import OrderedDict

from Cabecote import Cabecote

class Furadeira:
	def __init__(self, array):
		self.marca = array['marca']
		self.nome = array['nome']
		self.nro_cabecotes = array['nro_cabecotes']
		self.nro_pinos = array['nro_pinos']
		self.distancia_pinos = array['distancia_pinos']
		self.distancia_min_cabecotes = array['distancia_min_cabecotes']
		self.posicao_cabecotes = array['posicao_cabecotes']
		self.eixo_y = array['eixo_y']
		self.bipartido = array['bipartido']

		self.deslocamento_y = 0

		self.criar_cabecotes()
		# self.__calcular_posicao_cabecotes()
		# self.__calcular_posicao_brocas()

	# Cria os cabeçotes com base nas definições da furadeira
	def criar_cabecotes(self):
		cabecotes = []

		for nro in range(1, self.nro_cabecotes + 1):
			for posicao in self.posicao_cabecotes:
				if nro in self.posicao_cabecotes[posicao]:
					cabecote = Cabecote(nro,
						self.nro_pinos,
						self.distancia_pinos,
						self.distancia_min_cabecotes,
						posicao,
						self.bipartido)
					cabecotes.append(cabecote)
					break

		self.cabecotes = cabecotes

	# Distribuir furos para os cabeçotes
	def distribuir_furos(self, furos):
		
		# Agrupar por side
		groups = defaultdict(list)
		for array in furos:
			for furo in array:
				groups[furo.side].append(array)
				break
		furos = dict(groups.items())

		# Agrupa furos por alinhamento
		# for side in furos:
		# 	if side in ['0 : 0', '0 : 5']:
		# 		groups = defaultdict(list)
		# 		for array in furos[side]:
		# 			x_array = list(set(list(furo.x for furo in array)))
		# 			y_array = list(set(list(furo.y for furo in array)))

		# 			if len(x_array) == 1:
		# 				# Alinhado no eixo X
		# 				groups['alinhado_x'].append(array)
		# 				# groups[side].append(array)
		# 			elif len(y_array) == 1:
		# 				# Alinhado no eixo Y
		# 				groups['alinhado_y'].append(array)
		# 			else:
		# 				# Não alihado
		# 				groups['nao_alinhado'].append(array)
		# 		furos[side] = dict(groups.items())

		# Distribuir furos
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

				# Agrupar furos por alinhamento
				groups = defaultdict(list)
				for array in furos[side]:
					x_array = list(set(list(furo.x for furo in array)))
					y_array = list(set(list(furo.y for furo in array)))

					if len(x_array) == 1:
						# Alinhado no eixo X
						groups['alinhado_x'].append(array)

					elif len(y_array) == 1:
						# Alinhado no eixo Y
						groups['alinhado_y'].append(array)

					else:
						# Não alihado
						groups['nao_alinhado'].append(array)

				furos[side] = dict(groups.items())
				
				# Furos alinhados no eixo X e Y
				# -------------------------------------------------
				for alinhamento in ['alinhado_x', 'alinhado_y']:
					if alinhamento in furos[side]:
						# Agrupar por x
						groups = defaultdict(list)
						for array in furos[side][alinhamento]:
							for furo in array:
								middle = self.defineMiddleX(array)
								groups[middle].append(furo)

						groups = dict(groups.items())

						# Ordenar
						groups = dict(OrderedDict(sorted(groups.items())))
						furos[side][alinhamento] = groups

				# print(furos)
				# exit()


				# Selecionar o cabeçotes
				# -------------------------------------------------
				for alinhamento in furos[side]:
					for x in furos[side][alinhamento]:
						for cabecote in self.cabecotes:
							if cabecote.posicao == posicao and cabecote.used == False:
								break

						cabecote.use()
						cabecote.setX(x)

						if alinhamento == 'alinhado_y':
							cabecote.setUsedBipartido(True)

						# Aplica os furos
						for furo in furos[side][alinhamento][x]:
							cabecote.setBroca(furo, self.eixo_y)

		self.ordenar_cabecotes()


	# Ordena os cabeçotes que serão utilizados conforme a posição no eixo x
	def ordenar_cabecotes(self):

		for side in ['inferior', 'superior']:
			cabecotes = list(
				cabecote for cabecote in self.cabecotes 
				if cabecote.posicao == side and cabecote.used)

			if (len(cabecotes) > 0):
				distancia_x = list(cabecote.x for cabecote in cabecotes)
				distancia_x.sort()

				print(cabecotes)
				print(distancia_x)

				for i, cabecote in enumerate(cabecotes):
					print(i, cabecote, distancia_x[i])
					if (cabecote.x != distancia_x[i]):
						self.setCabecoteNro(cabecote, i)
					# 	cabecote.setX(distancia_x[i])
					# cabecote.setX(min(distancia_x))
					# distancia_x.remove(cabecote.x)

	def setCabecoteNro(self, cabecote, new_nro):
		if new_nro > cabecote.nro:
			for i in range(cabecote.nro, new_nro):
				self.cabecotes[i - 1].setNro(i)

			cabecote.setNro(new_nro)

	# Define o ponto X que os furos deverão ser aplicados
	def defineMiddleX(self, furos):
		ponto_x = []
		for furo in furos:
			ponto_x.append(furo.x)

		ponto_x = list(set(ponto_x))

		# Encontrar ponto médio em x para furação
		# if len(ponto_x) == 2:
			# Se a quantidade de furos na horizontal for 2 
			# (separados pela distancia de da broca), ao invés de girar o cabeçote
			# pode ser adicionado o agregado (ÚLTIMO RECURSO)

			# Adicionar agregado
			# middle = min(ponto_x)
		# 	continue
		# else:
		middle = min(ponto_x) + (len(ponto_x) // 2) * self.distancia_pinos

		return middle

	# Imprimir tabela de cabeçotes
	def imprimir_cabecotes(self):

		table = PrettyTable()
		table.title = 'Cabeçotes'
		table.field_names = list(cabecote.nro for cabecote in self.cabecotes)

		# Brocas
		for pino in range(1, self.nro_pinos + 1):
			
			row = list()
			for cabecote in self.cabecotes:
				if cabecote.used_bipartido:
					if pino in [math.ceil(self.nro_pinos * (1/4)), math.ceil(self.nro_pinos * (3/4))]:
						
						# print(list(cabecote.pinos[1]))
						# fila_dividida = list(cabecote.pinos)[
						# 	int(((pino // (self.nro_pinos / 2)) * (self.nro_pinos / 2))) 
						# 	: 
						# 	int((pino // (self.nro_pinos / 2)) * (self.nro_pinos / 2) + (self.nro_pinos / 2))
						# ]

						array = []
						for rotacionado in list(cabecote.pinos)[
								int(((pino // (self.nro_pinos / 2)) * (self.nro_pinos / 2))) 
								: 
								int((pino // (self.nro_pinos / 2)) * (self.nro_pinos / 2) + (self.nro_pinos / 2))
							]:
							
							array.append(cabecote.pinos[rotacionado])

						line = ' '.join(array)
						row.append(line)

						# row.append(fila_dividida)
					else:
						row.append(' ')
				else:
					row.append(cabecote.pinos[pino])


			# table.add_row(list(cabecote.pinos[pino] for cabecote in self.cabecotes))
			table.add_row(row)
				

			


		# Distancia x
		table.add_row(list('---' for cabecote in self.cabecotes))
		# Limites
		row = []
		for cabecote in self.cabecotes:
			if cabecote.used_bipartido:
				string = str(cabecote.limite['start']) + ' ← ' + str(cabecote.x) + ' → ' + str(cabecote.limite['end'])
				row.append(string)
			else:
				row.append(cabecote.x)
		table.add_row(row)
		# Limites totais
		row = []
		for cabecote in self.cabecotes:
			if cabecote.used:
				string = str(cabecote.limite['start']) + ' ↔ ' + str(cabecote.limite['end'])
			else:
				string = ' '
			row.append(string)
		# table.add_row(row)
		table.add_row(list(cabecote.posicao[0:3] for cabecote in self.cabecotes))

		# Índice
		indice = ''
		table._field_names.insert(0, indice)
		table._align[indice] = 'c'
		table._valign[indice] = 't'
		for i, _ in enumerate(table._rows):
			if i < self.nro_pinos:
				if self.eixo_y == 'invertido':
					table._rows[i].insert(0, (len(table._rows) - 3 - i) * self.distancia_pinos)
				else:
					table._rows[i].insert(0, (i+1) * self.distancia_pinos)
			else:
				table._rows[i].insert(0, '')

		print(table)

	# Imprimir tabela de cabeçotes
	def imprimir_cabecote(self, nro):

		cabecote = self.cabecotes[nro - 1]
		cabecote.imprimir_cabecote()