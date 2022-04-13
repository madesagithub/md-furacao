class Cabecote:
	def __init__(self, nro, nro_brocas, distancia_pinos):
		self.nro = nro
		self.distancia_pinos = distancia_pinos
		self.x = 0
		self.used = False

		self.brocas = {}
		for i in range(1, nro_brocas + 1):
			self.brocas[i] = 'x'