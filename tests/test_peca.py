import json
from os import walk
import unittest

class testPeca(unittest.TestCase):
	
	def setUp(self):
		self.path = 'Peças Verificadas'
		self.diretorios = next(walk(self.path))[1]
		self.furadeiras = list(map(lambda x: x.split(' - ')[1], self.diretorios))

	def test_setup(self):

		for i, furadeira in enumerate(self.furadeiras):
			path = f'{self.path}/{self.diretorios[i]}'
			filenames = next(walk(path), (None, None, []))[2]

			for filename in filenames:

				file = open(f'{path}/{filename}')
				peca_verificada = json.load(file)
				file.close()

				# self.assertEqual(1, peca_verificada)
				# self.assertEqual(i + 2, 2)
		

if __name__ == '__main__':
	unittest.main()