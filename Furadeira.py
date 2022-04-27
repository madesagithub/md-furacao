from prettytable import PrettyTable
from Cabecote import Cabecote

class Furadeira:
	def __init__(self, array):
		self.nome = array['nome']
		self.nro_cabecotes = array['nro_cabecotes']
		self.nro_brocas = array['nro_brocas']
		self.distancia_pinos = array['distancia_pinos']
		self.posicao_cabecotes = array['posicao_cabecotes']
		self.eixo_y = array['eixo_y']
		self.bipartido = array['bipartido']

		self.criar_cabecotes()
		# self.__calcular_posicao_cabecotes()
		# self.__calcular_posicao_brocas()

	# Cria os cabeçotes com base nas definições da furadeira
	def criar_cabecotes(self):
		cabecotes = []

		for i in range(1, self.nro_cabecotes + 1):
			for j in self.posicao_cabecotes:
				if i in self.posicao_cabecotes[j]:
					cabecote = Cabecote(i,
						self.nro_brocas,
						self.distancia_pinos,
						j)
					cabecotes.append(cabecote)
					break

		self.cabecotes = cabecotes
	
	# Imprimir tabela de cabeçotes
	def imprimir_cabecotes(self):

		table = PrettyTable()
		table.title = 'Cabeçotes'
		table.field_names = list(cabecote.nro for cabecote in self.cabecotes)

		# Brocas
		for i in range(1, self.nro_brocas + 1):
			table.add_row(list(cabecote.brocas[i] for cabecote in self.cabecotes))

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
			if i < self.nro_brocas:
				if self.eixo_y == 'invertido':
					table._rows[i].insert(0, (len(table._rows) - 3 - i) * self.distancia_pinos)
				else:
					table._rows[i].insert(0, (i+1) * self.distancia_pinos)
			else:
				table._rows[i].insert(0, '')

		print(table)