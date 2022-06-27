import json
from os import walk
import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('.'))
from furacao import main

class testPeca(unittest.TestCase):
	
	def setUp(self):
		self.path = 'Peças Verificadas'
		self.diretorios = next(walk(self.path))[1]
		self.furadeiras = list(map(lambda x: x.split(' - ')[1], self.diretorios))

	def test_setup(self):
		for i, modelo_furadeira in enumerate(self.furadeiras):
			path = f'{self.path}/{self.diretorios[i]}'
			filenames = next(walk(path), (None, None, []))[2]

			print(path)
			print(filenames)

			for filename in filenames:

				# Peça Verificada
				file = open(f'{path}/{filename}')
				peca_verificada = json.load(file)
				file.close()

				furadeira = main(filename.replace('.json', ''), modelo_furadeira)
				# exit()
				# ----------
				# Verificação
				self.assertEqual(furadeira.to_json(), peca_verificada)
				# exit()
		

if __name__ == '__main__':
	unittest.main()