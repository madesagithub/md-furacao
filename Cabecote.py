import math
from prettytable import PrettyTable

class Cabecote():
	def __init__(self, nro, nro_pinos, distancia_pinos, distancia_min_cabecotes, posicao, bipartido):
		self.setNro(nro)
		self.nro_pinos = nro_pinos
		self.distancia_pinos = distancia_pinos
		self.distancia_min_cabecotes = distancia_min_cabecotes
		self.posicao = posicao
		self.setBipartido(bipartido)

		# ----------
		self.setX(0)
		self.used = False
		self.used_bipartido = False
		self.used_bipartido_eixo = {
			1: False,
			2: False,
		}
		self.passante = False
		self.furos = []
		self.deslocamento_y = 0
		self.default_pino = '×'

		self.pinos = {}
		for i in range(1, nro_pinos + 1):
			self.pinos[i] = self.default_pino

	# Define qual pino será usado para colocar a broca
	def setPino(self, furo, eixo_y = 'normal', eixo = 'y'):
		self.addFuro(furo)
		



		# if self.used_bipartido:
		# 	nro_pino = (self.nro_pinos // 2)
		# 	nro_eixo = (nro_pino // (self.nro_pinos / 2)) + 1




		if eixo_y == 'invertido':
			deslocamento = getattr(furo, eixo) % self.distancia_pinos
			nro_pino = int(len(self.pinos) + 1 - ((getattr(furo, eixo) + deslocamento) // self.distancia_pinos))
		elif eixo_y == 'normal':
			deslocamento = getattr(furo, eixo) % self.distancia_pinos
			nro_pino = int((getattr(furo, eixo) + deslocamento) // self.distancia_pinos)



		self.pinos[nro_pino] = furo.broca

		if deslocamento != 0:
			self.deslocamento_y = deslocamento

	# Define o número de identificação do cabeçote
	def setNro(self, nro):
		self.nro = nro

	# Define a distancia no eixo X do cabeçote
	def setX(self, x):
		self.x = x
		self.setLimite()

	def	setLimite(self):
		self.limite = {}
		self.limite['start'] = max(0, self.x - self.distancia_min_cabecotes)
		self.limite['end'] = self.x + self.distancia_min_cabecotes

	def use(self):
		self.used = True

	# Verifica se o cabeçote possui somente furos passantes
	# Cabeçotes assim definidos podem ser alocados na posição superior
	def definePassante(self):
		if 0 in list(furo.p for furo in self.furos):
			self.passante = False
		else:
			self.passante = True

	# Adiciona o furo para a lista
	def addFuro(self, furo):
		self.furos.append(furo)
		self.definePassante()

	# Define se o cabeçote tem a possibilidade de ser bipartido
	def setBipartido(self, bool):
		self.bipartido = bool

		if bool:
			self.pinos_rotacao = [math.ceil(self.nro_pinos * (1/4)), math.ceil(self.nro_pinos * (3/4))]

	# Define se o cabeçote está usando a bipartição
	def setUsedBipartido(self, bool):
		self.used_bipartido = bool

	# Define se o eixo do cabeçote está usando a bipartição
	def setUsedBipartidoEixo(self, eixo, bool):
		self.used_bipartido_eixo[eixo] = bool

	def imprimir_cabecote(self):
		table = PrettyTable()
		table.title = 'Cabeçote Nro ' + str(self.nro)
		table.field_names = ['Nro']

		# Pinos
		for pino in range(1, len(self.pinos) + 1):
			table.add_row([self.pinos[pino]])

		# Distancia x
		table.add_row(['-----'])
		table.add_row([self.x])
		table.add_row([self.posicao])

		# Índice 1
		indice = ''
		table._field_names.insert(0, indice)
		table._align[indice] = 'c'
		table._valign[indice] = 't'
		for i, _ in enumerate(table._rows):
			if i < self.nro_pinos:
				table._rows[i].insert(0, (i+1) * self.distancia_pinos)
			else:
				table._rows[i].insert(0, '')
		
		# Índice 2
		indice = ''
		table._field_names.insert(0, indice)
		table._align[indice] = 'r'
		table._valign[indice] = 't'
		for i, _ in enumerate(table._rows):
			if i < self.nro_pinos:
				table._rows[i].insert(0, (i+1))
			else:
				table._rows[i].insert(0, '')

		print(table)