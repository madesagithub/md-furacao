import math
from prettytable import PrettyTable

class Cabecote():
	def __init__(self, nro, nro_mandris, distancia_mandris, distancia_min_cabecotes, posicao, bipartido):
		self.setNro(nro)
		self.nro_mandris = nro_mandris
		self.distancia_mandris = distancia_mandris
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
		self.default_mandril = '×'

		self.mandris = {}
		for i in range(1, nro_mandris + 1):
			self.mandris[i] = self.default_mandril

	# Define qual mandril será usado para colocar a broca
	def setMandril(self, furo, eixo_y = 'normal', eixo = 'y'):
		self.addFuro(furo)
		



		# if self.used_bipartido:
		# 	nro_mandril = (self.nro_mandris // 2)
		# 	nro_eixo = (nro_mandril // (self.nro_mandris / 2)) + 1




		if eixo_y == 'invertido':
			deslocamento = getattr(furo, eixo) % self.distancia_mandris
			nro_mandril = int(len(self.mandris) + 1 - ((getattr(furo, eixo) + deslocamento) // self.distancia_mandris))
		elif eixo_y == 'normal':
			deslocamento = getattr(furo, eixo) % self.distancia_mandris
			nro_mandril = int((getattr(furo, eixo) + deslocamento) // self.distancia_mandris)



		self.mandris[nro_mandril] = furo.broca

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
		self.limite['start'] = max(0, self.x - self.distancia_min_cabecotes['normal'])
		self.limite['end'] = self.x + self.distancia_min_cabecotes['normal']

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

	# Adicionar os furos ao cabeçote
	def setFuros(self, furos):
		
		for furo in furos:
			self.addFuro(furo)

		self.definePassante()

		self.furos = furos

	# Define se o cabeçote tem a possibilidade de ser bipartido
	def setBipartido(self, bool):
		self.bipartido = bool

		if bool:
			self.mandris_rotacao = [
				math.ceil(self.nro_mandris * (1/4)),
				math.ceil(self.nro_mandris * (3/4))
			]

	# Define se o cabeçote está usando a bipartição
	def setUsedBipartido(self, bool = True):
		self.used_bipartido = bool

	# Define se o eixo do cabeçote está usando a bipartição
	def setUsedBipartidoEixo(self, eixo, bool = True):
		self.used_bipartido_eixo[eixo] = bool

	def imprimir_cabecote(self):
		table = PrettyTable()
		table.title = 'Cabeçote Nro ' + str(self.nro)
		table.field_names = ['Nro']

		# Mandris
		for mandril in range(1, len(self.mandris) + 1):
			table.add_row([self.mandris[mandril]])

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
			if i < self.nro_mandris:
				table._rows[i].insert(0, (i+1) * self.distancia_mandris)
			else:
				table._rows[i].insert(0, '')
		
		# Índice 2
		indice = ''
		table._field_names.insert(0, indice)
		table._align[indice] = 'r'
		table._valign[indice] = 't'
		for i, _ in enumerate(table._rows):
			if i < self.nro_mandris:
				table._rows[i].insert(0, (i+1))
			else:
				table._rows[i].insert(0, '')

		print(table)