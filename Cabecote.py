from prettytable import PrettyTable

class Cabecote:
	def __init__(self, nro, nro_pinos, distancia_pinos, distancia_min_cabecotes, posicao, bipartido):
		self.setNro(nro)
		self.nro_pinos = nro_pinos
		self.distancia_pinos = distancia_pinos
		self.distancia_min_cabecotes = distancia_min_cabecotes
		self.posicao = posicao
		self.bipartido = bipartido
		self.used = False
		self.used_bipartido = False
		self.passante = False
		self.furos = []
		self.limite = {}
		self.setX(0)
		self.deslocamento_x = 0
		self.default_pino = '×'

		self.pinos = {}
		for i in range(1, nro_pinos + 1):
			self.pinos[i] = self.default_pino

	def setBroca(self, furo, eixo_y = 'normal', var = 'y'):
		self.setFuro(furo)
		
		if eixo_y == 'invertido':
			nro_broca = len(self.pinos) + 1 - (getattr(furo, var) // self.distancia_pinos)
			deslocamento = getattr(furo, var) % self.distancia_pinos
		elif eixo_y == 'normal':
			nro_broca = getattr(furo, var) // self.distancia_pinos
			deslocamento = getattr(furo, var) % self.distancia_pinos

		self.pinos[nro_broca] = furo.broca

		if deslocamento != 0:
			self.deslocamento_x = deslocamento

	# Define o Número do cabeçote
	def setNro(self, nro):
		self.nro = nro

	# Define a distancia no eixo X do cabeçote
	def setX(self, x):
		self.x = x
		self.setLimite()

	def	setLimite(self):
		self.limite['start'] = max(0, self.x - self.distancia_min_cabecotes)
		self.limite['end'] = self.x + self.distancia_min_cabecotes

	def use(self):
		self.used = True
		self.definePassante()

	# Verifica se o cabeçote possui somente furos passantes
	# Cabeçotes assim definidos podem ser alocados na posição superior
	def definePassante(self):
		print(self.furos)

	# Adiciona o furo para a lista
	def setFuro(self, furo):
		self.furos.append(furo)

	# Define se o cabeçote tem a possibilidade de ser bipartido
	def setBipartido(self, bool):
		self.bipartido = bool

	# Define se o cabeçote está usando a bipartição
	def setUsedBipartido(self, bool):
		self.used_bipartido = bool

	def imprimir_cabecote(self):
		table = PrettyTable()
		table.title = 'Cabeçote Nro ' + str(self.nro)
		table.field_names = ['Nro']

		# Pinos
		for pino in range(1, len(self.pinos) + 1):
			table.add_row([self.pinos[pino]])

		# Distancia x
		table.add_row(['---'])
		table.add_row([self.x])
		table.add_row([self.posicao])

		# Índice
		indice = ''
		table._field_names.insert(0, indice)
		table._align[indice] = 'c'
		table._valign[indice] = 't'
		for i, _ in enumerate(table._rows):
			if i < self.nro_pinos:
				table._rows[i].insert(0, (i+1) * self.distancia_pinos)
			else:
				table._rows[i].insert(0, '')

		print(table)