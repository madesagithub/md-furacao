import math
from prettytable import PrettyTable

# from Furadeira import Furadeira

class Cabecote():
	nro: int
	posicao: str
	bipartido: bool
	x: int
	used: bool
	used_bipartido: bool
	used_bipartido_eixo: dict
	passante: bool
	furos: list
	mandris: dict
	mandris_rotacao: list
	deslocamento_y: int
	deslocamento_y_eixo = dict
	# furadeira: Furadeira


	def __init__(self, nro, posicao, furadeira):
		self.setNro(nro)
		self.posicao = posicao
		self.furadeira = furadeira

		# Informações da furadeira ----------
		self.setBipartido(self.furadeira.bipartido)

		# ----------
		self.used = False
		self.used_bipartido = False
		self.used_bipartido_eixo = {
			1: False,
			2: False,
		}
		self.passante = False
		self.furos = []
		self.deslocamento_y = 0
		self.deslocamento_y_eixo = {
			1: 0,
			2: 0,
		}

		# ----------
		self.setX(0)

		# Criação dos mandris ----------
		self.mandris = {}
		for i in range(1, self.furadeira.nro_mandris + 1):
			self.mandris[i] = self.furadeira.default_mandril


	# Define qual mandril será usado para colocar a broca
	def setMandril(self, furo, eixo_y = 'normal', eixo = 'y'):
		self.addFuro(furo)

		if eixo_y == 'invertido':
			deslocamento = getattr(furo, eixo) % self.furadeira.distancia_mandris
			nro_mandril = int(len(self.mandris) + 1 - ((getattr(furo, eixo) + deslocamento) // self.furadeira.distancia_mandris))
		else:
			deslocamento = getattr(furo, eixo) % self.furadeira.distancia_mandris
			nro_mandril = int((getattr(furo, eixo) + deslocamento) // self.furadeira.distancia_mandris)

		self.mandris[nro_mandril] = furo.broca

		if self.used_bipartido:
			eixo_rotacao = (nro_mandril // ((self.furadeira.nro_mandris // 2 + 1))) + 1
			self.useBipartidoEixo(eixo_rotacao)

		if deslocamento != 0:
			self.deslocamento_y = deslocamento


	# Define o número de identificação do cabeçote
	def setNro(self, nro):
		self.nro = nro


	# Define a distancia no eixo X do cabeçote
	def setX(self, x):
		self.x = x
		self.setLimite()


	# Define os limites que o cabeçote ira ocupar
	def	setLimite(self):
		self.limite = {}

		if self.posicao in ['esquerda', 'direita']:
			self.limite['start'] = self.x
			self.limite['end'] = self.x
		elif self.used_bipartido:
			# limites com bipartição
			self.limite['start'] = max(0, self.x - self.furadeira.distancia_min_cabecotes['rotacionado'])
			self.limite['end'] = self.x + self.furadeira.distancia_min_cabecotes['rotacionado']
		else:
			# limites sem bipartição
			self.limite['start'] = max(0, self.x - self.furadeira.distancia_min_cabecotes['normal'])
			self.limite['end'] = self.x + self.furadeira.distancia_min_cabecotes['normal']


	# Retorna os mandris que estão sobre o eixo de rotação do cabeçote bipartido
	def getMandrisRotacao(self):
		if self.furadeira.bipartido:
			if self.mandris_rotacao not in vars:
				self.setBipartido()
			return self.mandris_rotacao
		else:
			return False
		

	# Indica que o cabeçote está sendo utilizado
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
	def setBipartido(self, bool = True):
		self.bipartido = bool

		if bool:
			self.mandris_rotacao = [
				math.ceil(self.furadeira.nro_mandris * (1/4)),
				math.ceil(self.furadeira.nro_mandris * (3/4))
			]


	# Define se o cabeçote está usando a bipartição
	def useBipartido(self, bool = True):
		self.used_bipartido = bool


	# Define se o eixo do cabeçote está usando a bipartição
	def useBipartidoEixo(self, eixo, bool = True):
		self.used_bipartido_eixo[eixo] = bool


	def imprimir_cabecote(self):
		table = PrettyTable()
		table.title = 'Cabeçote Nro ' + str(self.nro)
		table.field_names = ['Mandris']

		# Mandris
		for mandril in range(1, len(self.mandris) + 1):
			if self.used_bipartido:
				eixo_rotacao = (mandril // ((self.furadeira.nro_mandris // 2 + 1))) + 1

				if self.used_bipartido_eixo[eixo_rotacao]:
					if mandril in self.mandris_rotacao:
						array = []
						for rotacionado in list(self.mandris)[
								int(((mandril // (self.furadeira.nro_mandris / 2)) * (self.furadeira.nro_mandris / 2))) 
								: 
								int((mandril // (self.furadeira.nro_mandris / 2)) * (self.furadeira.nro_mandris / 2) + (self.furadeira.nro_mandris / 2))
							]:
							
							array.append(self.mandris[rotacionado])

						line = ' '.join(array)
						table.add_row([line])
					else:
						table.add_row([' '])
				else:
					table.add_row([self.mandris[mandril]])
			else:
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
			if i < self.furadeira.nro_mandris:
				table._rows[i].insert(0, (i+1) * self.furadeira.distancia_mandris)
			else:
				table._rows[i].insert(0, '')
		
		# Índice 2
		indice = ''
		table._field_names.insert(0, indice)
		table._align[indice] = 'r'
		table._valign[indice] = 't'
		for i, _ in enumerate(table._rows):
			if i < self.furadeira.nro_mandris:
				table._rows[i].insert(0, (i+1))
			else:
				table._rows[i].insert(0, '')

		print(table)