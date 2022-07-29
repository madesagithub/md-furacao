import math
from prettytable import PrettyTable

# from Furadeira import Furadeira
from Agregado import Agregado

class Cabecote():
	nro: int
	posicao: str
	bipartido: bool
	x: int
	used: bool
	used_bipartido: bool
	used_bipartido_eixo: dict
	furos: list
	agregados: list
	mandris: dict
	mandris_rotacao: list
	deslocamento_y: int
	deslocamento_y_eixo = dict
	# furadeira: Furadeira


	def __init__(self, nro, posicao, furadeira):
		self.set_nro(nro)
		self.posicao = posicao
		self.furadeira = furadeira

		# Informações da furadeira ----------
		self.set_bipartido(self.furadeira.bipartido)

		self.create()


	def create(self):
		self.used = False
		self.used_bipartido = False
		self.used_bipartido_eixo = {
			1: False,
			2: False,
		}
		self.furos = []
		self.agregados = []
		self.deslocamento_y = 0
		self.deslocamento_y_eixo = {
			1: 0,
			2: 0,
		}

		# ----------
		self.set_x(0)

		# Criação dos mandris ----------
		self.mandris = {}
		for i in range(1, self.furadeira.nro_mandris + 1):
			self.mandris[i] = self.furadeira.default_mandril


	# Define qual mandril será usado para colocar a broca
	def set_mandril(self, furo, eixo_y = 'normal', eixo = 'y'):
		self.add_furo(furo)
		self.set_deslocamento_y(furo, eixo)

		nro_mandril = self.calcular_mandril(furo, eixo_y, eixo)

		self.mandris[nro_mandril] = furo.broca

		if self.used_bipartido:
			eixo_rotacao = (nro_mandril // ((self.furadeira.nro_mandris // 2 + 1))) + 1
			self.use_bipartido_eixo(eixo_rotacao)

		self.set_deslocamento_y_eixo_rotacao()
		return nro_mandril


	# Calcular qual mandril será utilizado
	def calcular_mandril(self, furo, eixo_y = 'normal', eixo = 'y'):

		deslocamento = (getattr(furo, eixo) % self.furadeira.distancia_mandris) - self.furadeira.batente_fundo

		if furo.id == 'P1012_3' or furo.id == 'P1012_2_2':
			print (furo.id, getattr(furo, eixo) % 32, deslocamento)


		if eixo_y == 'invertido':
			nro_mandril = int(len(self.mandris) + 1 - ((getattr(furo, eixo) + deslocamento) // self.furadeira.distancia_mandris))
		else:
			nro_mandril = int((getattr(furo, eixo) + deslocamento) // self.furadeira.distancia_mandris) + 1

		if furo.id == 'P1012_3' or furo.id == 'P1012_2_2':
			print (furo.id, nro_mandril)
		return nro_mandril

	
	# Calcula o deslocamento do cabeçote com base na necessária para alocar o furo
	def set_deslocamento_y(self, furo, eixo):
		# deslocamento = (getattr(furo, eixo) % self.furadeira.distancia_mandris) + self.furadeira.distancia_mandris - self.furadeira.batente_fundo
		deslocamento = (getattr(furo, eixo) % self.furadeira.distancia_mandris) - self.furadeira.batente_fundo
	
		if deslocamento != 0:
			self.deslocamento_y = deslocamento

		return deslocamento

	
	def set_deslocamento_y_eixo_rotacao(self):
		pass


	# Define o número de identificação do cabeçote
	def set_nro(self, nro):
		self.nro = nro


	# Define a distancia no eixo X do cabeçote
	def set_x(self, x):
		self.x = x
		self.set_limite()


	# Define os limites que o cabeçote ira ocupar
	def	set_limite(self):
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
	def get_mandris_rotacao(self):
		if self.furadeira.bipartido:
			if self.mandris_rotacao not in vars:
				self.set_bipartido()
			return self.mandris_rotacao
		else:
			return False


	# Retorna em qual eixo de rotação um mandril está
	def get_eixo_rotacao(self, mandril):
		eixo = (mandril // ((self.furadeira.nro_mandris // 2 + 1))) + 1
		
		return eixo

	# Indica que o cabeçote está sendo utilizado
	def use(self):
		self.used = True


	# Restaura o furos para a condição inicial
	def restore(self):
		self.create()


	# Verifica se é um cabeçote passante
	# Verifica se o cabeçote possui somente furos passantes
	# Cabeçotes assim definidos podem ser alocados na posição superior
	def is_passante(self):
		return 0 not in list(furo.p for furo in self.furos)


	# Adiciona o furo para a lista
	def add_furo(self, furo):
		self.furos.append(furo)


	# Define se o cabeçote tem a possibilidade de ser bipartido
	def set_bipartido(self, bool = True):
		self.bipartido = bool

		if bool:
			self.mandris_rotacao = [
				math.ceil(self.furadeira.nro_mandris * (1/4)),
				math.ceil(self.furadeira.nro_mandris * (3/4))
			]


	# Define se o cabeçote está usando a bipartição
	def use_bipartido(self, bool = True):
		self.used_bipartido = bool


	# Define se o eixo do cabeçote está usando a bipartição
	def use_bipartido_eixo(self, eixo, bool = True):
		self.used_bipartido_eixo[eixo] = bool


	# Adiciona uma peça agregada ao cabeçote
	def add_agregado(self, furos):
		for furo in furos:
			# Definir mandril
			mandril = self.calcular_mandril(furo)

			# Definir posicao
			if furo.x < self.x:
				posicao = 'esquerda'
			elif furo.x > self.x:
				posicao = 'direita'

			# Adicionar furo
			self.furos.append(furo)

			agregado = Agregado(
					self.furadeira,
					self,
					mandril,
					posicao,
					furo
				)

			self.agregados.append(agregado)


	# Verifica se o cabeçote está usando o agregado
	def used_agregado(self, nro_mandril = False):
		if nro_mandril:
			for agregado in self.agregados:
				if agregado.mandril == nro_mandril:
					return True
			return False
		else:
			return len(self.agregados) > 0


	# Verifica se o deslocamento do cabeçote é multiplo de outro deslocamento
	def deslocamento_y_multiplo(self, deslocamento_y):
		return (abs(deslocamento_y - self.deslocamento_y) % self.furadeira.distancia_mandris) == 0


	def imprimir_cabecote(self):
		table = PrettyTable()
		table.title = 'Cabeçote Nro ' + str(self.nro)
		table.field_names = ['Mandris']

		# Mandris
		for mandril in range(1, len(self.mandris) + 1):
			if self.used_bipartido:
				eixo_rotacao = self.get_eixo_rotacao(mandril)

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