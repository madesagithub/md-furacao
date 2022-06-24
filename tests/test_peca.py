import unittest

from setups import setups, pecas_verificadas	# dicionario para teste de validação

class testPeca(unittest.TestCase):
	
	def __init__(self):
		pass

	def test_setup(self):
		for peca in pecas_verificadas:
			self.assertEqual( , peca)