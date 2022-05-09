from prettytable import PrettyTable

class Cabecote:
	def __init__(self, nro, nro_pinos, distancia_pinos, posicao, bipartido):
		self.nro = nro
		self.nro_pinos = nro_pinos
		self.distancia_pinos = distancia_pinos
		self.posicao = posicao
		self.bipartido = bipartido
		self.used_bipartido = False
		self.x = 0
		self.deslocamento_x = 0
		self.used = False

		self.pinos = {}
		for i in range(1, nro_pinos + 1):
			self.pinos[i] = 'x'

	def setBroca(self, furo, eixo_y = 'normal', var = 'y'):
		if eixo_y == 'invertido':
			nro_broca = len(self.pinos) + 1 - (getattr(furo, var) // self.distancia_pinos)
			deslocamento = getattr(furo, var) % self.distancia_pinos
		elif eixo_y == 'normal':
			nro_broca = getattr(furo, var) // self.distancia_pinos
			deslocamento = getattr(furo, var) % self.distancia_pinos

		self.pinos[nro_broca] = furo.broca

		if deslocamento != 0:
			self.deslocamento_x = deslocamento

	def setX(self, x):
		self.x = x

	def use(self):
		self.used = True

	def setBipartido(self, bool):
		self.bipartido = bool

	def setUsedBipartido(self, bool):
		self.used_bipartido = bool

	def imprimir_cabecote(self):
		table = PrettyTable()
		table.title = 'Cabeçote Nro ' + str(self.nro)
		table.field_names = ['Nro']

		# pinos
		for pino in range(1, len(self.pinos) + 1):
			table.add_row(self.pinos[pino])

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