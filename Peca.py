from prettytable import PrettyTable

class Peca:
	def __init__(self, nome, comprimento, largura, espessura):
		self.nome = nome,
		self.comprimento = comprimento,
		self.largura = largura,
		self.espessura = espessura

	def imprimir_peca(self):
		table = PrettyTable()
		table.title = self.nome
		table.field_names = ['Dimensão', 'Valor (mm)']
		table.align = 'l'
		table._align['Valor (mm)'] = 'r'
		table.add_row(['Comprimento (X)', self.comprimento])
		table.add_row(['Largura (Y)', self.largura])
		table.add_row(['Espessura (Z)', self.espessura])
		print(table)