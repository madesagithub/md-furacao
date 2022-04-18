class Cabecote:
	def __init__(self, nro, nro_brocas, distancia_pinos, posicao):
		self.nro = nro
		self.distancia_pinos = distancia_pinos
		self.posicao = posicao
		self.x = 0
		self.used = False

		self.brocas = {}
		for i in range(1, nro_brocas + 1):
			self.brocas[i] = 'x'

	# def setBroca(self, nro, nro_broca, broca):
	def setBroca(self, furo, var = 'y'):
		nro_broca = getattr(furo, var) / self.distancia_pinos
		self.brocas[nro_broca] = furo.broca

	def setX(self, x):
		self.x = x

	def use(self):
		self.used = True