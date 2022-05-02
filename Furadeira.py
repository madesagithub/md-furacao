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

				if 'alinhado_y' in furos[side]:
					

					# Agrupar por x
					# groups = defaultdict(list)
					# for array in furos[side]['alinhado_y']:
					# 	for furo in array:

					
					
					# Agrupar por x
					groups = defaultdict(list)
					for array in furos[side]['alinhado_x']:
						for furo in array:
							groups[furo.x].append(furo)
					groups = dict(groups.items())

					# Ordenar
					groups = dict(OrderedDict(sorted(groups.items())))
					furos[side]['alinhado_x'] = groups

				print(furos[side])
				exit()

				# Selecionar o cabeçotes
				for x in groups:

					for cabecote in self.cabecotes:
						if cabecote.posicao == posicao and cabecote.used == False:
							break

					cabecote.use()
					cabecote.setX(x)

					# Aplica os furos
					for furo in groups[x]:
						cabecote.setBroca(furo, self.eixo_y)

	# Ordena os cabeçotes que serão utilizados conforme a posição no eixo x
	def ordenar_cabeocotes(self):
		distancia_x = list(cabecote.x for cabecote in self.cabecotes)

	# Imprimir tabela de cabeçotes
	def imprimir_cabecotes(self):

		table = PrettyTable()
		table.title = 'Cabeçotes'
		table.field_names = list(cabecote.nro for cabecote in self.cabecotes)

		# Brocas
		for pino in range(1, self.nro_pinos + 1):
			table.add_row(list(cabecote.brocas[pino] for cabecote in self.cabecotes))

		# Distancia x
		table.add_row(list('---' for cabecote in self.cabecotes))
		table.add_row(list(cabecote.x for cabecote in self.cabecotes))
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