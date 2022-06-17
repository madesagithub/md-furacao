import json
from prettytable import PrettyTable
from collections import defaultdict
from typing import OrderedDict

from Cabecote import Cabecote

class Furadeira:
	def __init__(self, array):
		self.marca = array['marca']
		self.nome = array['nome']
		self.nro_cabecotes = array['nro_cabecotes']
		self.nro_mandris = array['nro_mandris']
		self.distancia_mandris = array['distancia_mandris']
		self.distancia_min_cabecotes = array['distancia_min_cabecotes']
		self.posicao_cabecotes = array['posicao_cabecotes']
		self.batente_fundo = array['batente_fundo']
		self.eixo_y = array['eixo_y']
		self.bipartido = array['bipartido']

		# ----------
		self.posicoes = list(self.posicao_cabecotes.keys())
		self.deslocamento_y = 0
		self.default_mandril = '×'

		self.criar_cabecotes()
		# self.__calcular_posicao_cabecotes()
		# self.__calcular_posicao_brocas()


	# Cria os cabeçotes com base nas definições da furadeira
	def criar_cabecotes(self):
		self.cabecotes = []

		for nro in range(1, self.nro_cabecotes + 1):
			for posicao in self.posicao_cabecotes:
				if nro in self.posicao_cabecotes[posicao]:
					cabecote = Cabecote(
						nro,
						posicao,
						self
					)
					self.cabecotes.append(cabecote)
					break


	# Define o batente de fundo com base nas peças laterais
	def define_batente_fundo(self, furos):
		
		if self.batente_fundo:
			self.batente_fundo = 0
			side = '0 : 1'

			furos = [item for sublist in furos for item in sublist]
			furos = list(
					furo.x for furo in furos
					if furo.side == side)

			if len(furos) > 0:
				furo = min(furos)
				diferenca = furo % self.distancia_mandris

				if diferenca != 0:
					self.batente_fundo = diferenca


	# Distribuir furos para os cabeçotes
	def distribuir_furos(self, furos, peca):
		
		self.define_batente_fundo(furos)

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
		# 				# Não alinhado
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
						# Não alinhado
						groups['nao_alinhado'].append(array)

				furos[side] = dict(groups.items())
				
				# Furos alinhados nos eixos X e Y
				# -------------------------------------------------
				for alinhamento in ['alinhado_x', 'alinhado_y']:
					if alinhamento in furos[side]:
						# Agrupar por x
						groups = defaultdict(list)
						for array in furos[side][alinhamento]:
							for furo in array:
								middle = self.define_middle_x(array)
								groups[middle].append(furo)

						groups = dict(groups.items())

						# Ordenar
						groups = dict(OrderedDict(sorted(groups.items())))
						furos[side][alinhamento] = groups

				# print(furos[side])
				# exit()


				# Há um caso onde os furos podem estar alinhados em X
				# porém, pode ser que um destes precise deslocamento em Y e outro não.
				# Este caso deve receber atenção.


				# Selecionar o cabeçotes
				# -------------------------------------------------
				for alinhamento in furos[side]:
					for x in furos[side][alinhamento]:
						cabecote = list(cabecote for cabecote in self.cabecotes
							if cabecote.posicao == posicao 
							and cabecote.used == False)[0]

						cabecote.use()
						cabecote.set_x(x)

						if alinhamento == 'alinhado_y':
							cabecote.use_bipartido()

						# Aplica os furos
						for furo in furos[side][alinhamento][x]:
							cabecote.set_mandril(furo, self.eixo_y)


			# Esquerda
			# Direita
			# --------------------
			elif side in ['0 : 1', '0 : 3']:

				# Define o valor de x
				if side == '0 : 1':
					x = 0
				else:
					x = peca.comprimento

				# Selecionar o cabeçotes
				# -------------------------------------------------
				for array in furos[side]:
					cabecote = list(cabecote for cabecote in self.cabecotes
							if cabecote.posicao == posicao 
							and cabecote.used == False)[0]

					cabecote.use()
					cabecote.set_x(x)

					# print(x)
					# Aplica os furos
					for furo in array:
						cabecote.set_mandril(furo, self.eixo_y, 'x')


			# Traseira
			# Frontal
			# --------------------
			elif side in ['0 : 2', '0 : 4']:
				continue

		self.resolver_limites()


	# Resolve os problemas relacionados aos limites
	def resolver_limites(self):
		problemas = self.verificar_limites()

		while len(problemas) > 0:
			for cabecote in problemas:
				self.mover_cabecote(cabecote, 'superior')
			problemas = self.verificar_limites()

		self.ordenar_cabecotes()


	# Analisa os a distribuição dos cabeçotes e verifica se há algum problema
	# quanto ao limite em que está ocupando.
	def verificar_limites(self):
		self.ordenar_cabecotes()

		# 1. Verificar quais possuem mais problemas
		# 2. Verificar quais podem ser movidos para cima
		# 3. Verificar quais possuem menos furos
	
		# Lista de cabeçotes
		cabecotes = list(cabecote for cabecote in self.cabecotes
			if cabecote.used == True
			and cabecote.posicao == 'inferior')

		# Lista de cabecotes passantes
		passantes = list(cabecote for cabecote in cabecotes
			if cabecote.is_passante())


		# Verifica quais cabecotes passantes possuem problemas de limite
		for i, cabecote in enumerate(cabecotes):
			if cabecote in passantes:
				if i == 0:
					if cabecote.limite['end'] <= cabecotes[i + 1].limite['start']:
						passantes.remove(cabecote)
				elif i == len(cabecotes) - 1:
					if cabecote.limite['start'] >= cabecotes[i - 1].limite['end']:
						passantes.remove(cabecote)
				else:
					if cabecote.limite['start'] >= cabecotes[i - 1].limite['end'] and cabecote.limite['end'] <= cabecotes[i + 1].limite['start']:
						passantes.remove(cabecote)

		# Ordena conforme a quantidade de furos (menor para maior)
		passantes.sort(key=lambda cabecote: len(cabecote.furos))

		return passantes


	# Encontra problemas de limite nos cabecotes
	def encontrar_problemas_limite(self, posicao = 'inferior'):
		cabecotes = list(cabecote for cabecote in self.cabecotes 
			if cabecote.used == True
			and cabecote.posicao == posicao)

		problemas = {}
		for cabecote in cabecotes:
			problemas[cabecote] = 0

			for cabecote_lateral in cabecotes:
				if cabecote != cabecote_lateral:
					if cabecote.x > cabecote_lateral.x:
						if cabecote.limite['start'] < cabecote_lateral.limite['end']:
							problemas[cabecote] += 1
					elif cabecote.x < cabecote_lateral.x:
						if cabecote.limite['end'] > cabecote_lateral.limite['start']:
							problemas[cabecote] += 1

		return problemas


	# Ordena os cabeçotes que serão utilizados conforme a posição no eixo x
	def ordenar_cabecotes(self):
		for posicao in self.posicoes:
			cabecotes = list(
				cabecote for cabecote in self.cabecotes 
				if cabecote.posicao == posicao and cabecote.used)

			# Ordena os cabeçotes conforme X
			cabecotes.sort(key=lambda cabecote: cabecote.x)

			if (len(cabecotes) > 0):
				for i, cabecote in enumerate(cabecotes):
					cabecotes_nro = list(cabecote for cabecote in self.cabecotes
						if cabecote.posicao == posicao)
					cabecotes_nro.sort(key=lambda cabecote: cabecote.nro)

					if cabecote.nro != cabecotes_nro[i].nro:
						self.swap_cabecotes(cabecote, cabecotes_nro[i])

		self.sort_cabecotes()


	# Ordena os cabeçotes de acordo com o número
	def sort_cabecotes(self):
		self.cabecotes.sort(key=lambda cabecote: cabecote.nro)


	# Muda a posição do cabeçote
	def mover_cabecote(self, cabecote, posicao):
		novo_cabecote = list(cabecote for cabecote in self.cabecotes
			if cabecote.posicao == posicao 
			and cabecote.used == False)[0]

		self.swap_cabecotes(cabecote, novo_cabecote)


	# Troca 2 cabeçotes de nro e posição
	def swap_cabecotes(self, cabecote_1, cabecote_2):
		cabecote_1.nro, cabecote_2.nro = cabecote_2.nro, cabecote_1.nro
		cabecote_1.posicao, cabecote_2.posicao = cabecote_2.posicao, cabecote_1.posicao


	# Define o ponto X que os furos deverão ser aplicados
	def define_middle_x(self, furos):
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
		middle = min(ponto_x) + (len(ponto_x) // 2) * self.distancia_mandris

		return middle


	# Imprimir batente fundo
	def imprimir_setup(self):

		table = PrettyTable()
		table.title = 'Setup'
		table.field_names = [
			'Atributo',
			'Valor',
		]

		# Dados
		table.add_row([
			'Batente de fundo',
			self.batente_fundo
		])

		print(table)

	# Imprimir tabela de cabeçotes
	def imprimir_cabecotes(self):

		table = PrettyTable()
		table.title = 'Cabeçotes'
		table.field_names = list(cabecote.nro for cabecote in self.cabecotes)

		# Brocas
		for mandril in range(1, self.nro_mandris + 1):
			
			row = list()
			for cabecote in self.cabecotes:
				if cabecote.used_bipartido:
					eixo_rotacao = (mandril // ((self.nro_mandris // 2 + 1))) + 1

					if cabecote.used_bipartido_eixo[eixo_rotacao]:
						if mandril in cabecote.mandris_rotacao:
							array = []
							for rotacionado in list(cabecote.mandris)[
									int(((mandril // (self.nro_mandris / 2)) * (self.nro_mandris / 2))) 
									: 
									int((mandril // (self.nro_mandris / 2)) * (self.nro_mandris / 2) + (self.nro_mandris / 2))
								]:
								
								array.append(cabecote.mandris[rotacionado])

							line = ' '.join(array)
							row.append(line)
						else:
							row.append(' ')
					else:
						row.append(cabecote.mandris[mandril])
				else:
					row.append(cabecote.mandris[mandril])


			# table.add_row(list(cabecote.mandris[mandril] for cabecote in self.cabecotes))
			table.add_row(row)

		# Distancia x
		line = '-----'
		table.add_row(list(line for cabecote in self.cabecotes))
		# Limites
		row = []
		for cabecote in self.cabecotes:
			if cabecote.used_bipartido:
				string = str(cabecote.limite['start']) + ' ← ' + str(cabecote.x) + ' → ' + str(cabecote.limite['end'])
				row.append(string)
			else:
				row.append(cabecote.x)
		table.add_row(row)
		# Deslocamento Y
		table.add_row(list(cabecote.deslocamento_y for cabecote in self.cabecotes))
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

		# Índice 1
		indice = ''
		table._field_names.insert(0, indice)
		table._align[indice] = 'r'
		table._valign[indice] = 't'
		for i, _ in enumerate(table._rows):
			if i < self.nro_mandris:
				if self.eixo_y == 'invertido':
					table._rows[i].insert(0, (len(table._rows) - 3 - i) * self.distancia_mandris)
				else:
					table._rows[i].insert(0, (i+1) * self.distancia_mandris)
			elif i == self.nro_mandris:
				table._rows[i].insert(0, line)
			elif i == self.nro_mandris + 1:
				table._rows[i].insert(0, 'pos_x')
			elif i == self.nro_mandris + 2:
				table._rows[i].insert(0, 'des_y')
			else:
				table._rows[i].insert(0, '')

		# Índice 2
		table._field_names.insert(0, indice)
		for i, _ in enumerate(table._rows):
			if i < self.nro_mandris:
				table._rows[i].insert(0, (i+1))
			elif i == self.nro_mandris:
				table._rows[i].insert(0, line)
			else:
				table._rows[i].insert(0, '')


		print(table)

		# Observações
		if hasattr(self, 'observacao'):
			print(self.observacao)

	# Imprimir tabela de cabeçote específico
	def imprimir_cabecote(self, nro):
		cabecote = self.cabecotes[nro - 1]
		cabecote.imprimir_cabecote()


	def imprimir_furadeira(self):
		table = PrettyTable()
		table.title = self.marca + ' ' + self.nome
		table.field_names = list(['Atributo', 'Valor'])
		for var in vars(self):
			if var != 'cabecotes':
				table.add_row([var, vars(self)[var]])
		print(table)


	# Returna em formato json
	def toJson(self):

		furadeira = self

		# Deleta a furadeira do cabecote
		for cabecote in furadeira.cabecotes:
			cabecote.furos = [furo.__dict__ for furo in cabecote.furos]
			del cabecote.furadeira

		furadeira.cabecotes = [cabecote.__dict__ for cabecote in furadeira.cabecotes]

		return json.dumps(furadeira.__dict__, sort_keys=True, indent='\t')


	# Retorna um dicionário python 
	def toDict(self):
		furadeira = self.toJson()
		furadeira = furadeira.replace('true', 'True')
		furadeira = furadeira.replace('false', 'False')
		furadeira = furadeira.replace(str(json.dumps(self.default_mandril)), 'False')

		return furadeira

