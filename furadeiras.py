# Configuração de furadeiras
furadeiras = {
	'F400-T': {
		'marca': 'Lidear',
		'nome': 'F400-T',
		'nro_cabecotes': 16,					# revisar
		'nro_mandris': 17,						# revisar
		'distancia_mandris': 32,				# revisar
		'distancia_min_cabecotes': 96,			# revisar
		'bipartido': False,
		'agregado': False,
		'batente_fundo': True,
		'eixo_y': 'normal',						# normal ou invertido	# revisar
		'posicao_cabecotes': {
			'esquerda': [1],					# 1	# revisar
			'direita': [16],					# 1	# revisar
			'inferior': list(range(2, 10)),		# 8	# revisar
			'superior': list(range(10, 16)),	# 6	# revisar
		},
		'dimensoes_peca': {
			'comprimento': {					# x
				'min': 120,
				'max': 2780,
			},
			'largura': {						# y
				'min': 40,
				'max': 800,
			},
			'espessura': {						# z
				'min': 8,
				'max': 70,
			},
		}
	},
	'F500-B': {
		'marca': 'Lidear',
		'nome': 'F500-B',
		'nro_cabecotes': 16,
		'nro_mandris': 22,
		'distancia_mandris': 32,
		'distancia_min_cabecotes': {
			'normal': 96,
			'rotacionado': 50,
		},
		'bipartido': True,
		'agregado': True,
		'batente_fundo': True,
		'eixo_y': 'normal',						# normal ou invertido
		'posicao_cabecotes': {
			'esquerda': [1],					# 1
			'direita': [16],					# 1
			'inferior': list(range(2, 10)),		# 8
			'superior': list(range(10, 16)),	# 6
		},				
		'dimensoes_peca': {
			'comprimento': {					# x
				'min': 115,
				'max': 2750,
			},
			'largura': {						# y
				'min': 30,
				'max': 870,
			},
			'espessura': {						# z
				'min': 8,
				'max': 70,
			},
		}
	}
}