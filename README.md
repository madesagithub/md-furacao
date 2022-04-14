# MD-Furação

## Roadmap
- [ ] Automatizar a informação das informações de furação.

- [ ] Criar mecanismo automático que crie padrão de furação para as furadeiras lidear através da interação dos softwares Ardis e Topsolid.

- [ ] Criar interface gráfica para consulta das informações na máquina.

## Definições

| Atributo			 	| Descrição									|
|----------------------	|------------------------------------------	|
| **Side**				| Corresponde ao lado de furação		   	|
| **CRN**			 	| Corresponde ao lado de furação		   	|
| **DP**			   	| Profundidade do furo					 	|
| **TRH ou T**		 	| Se é um furo passante (atravessa a peça) 	|
| **DIA ou Diâmetro**   | Diâmetro do furo						 	|
| **X**					| Eixo horizontal (esquerda para direita)  	|
| **Y**					| Eixo vertical	(cima para baixo)           |
| **Z**					|										 	|


### Cabeçotes

| Side  	| CRN   | Posição		  				|
|-------	| ----- |------------------------------ |
| 0 : 0 	| 1	 	| Furação Inferior 				|
| 0 : 1 	| 1	 	| Topo/Vertical Esquerda		|
| 0 : 2 	| 	 	|				  				|
| 0 : 3 	| 4	 	| Topo/Vertical Direita	 		|
| 0 : 4 	| 	 	|						   		|
| 0 : 5 	| 4	 	| Furação Superior ~frontal~	|

- Posições
	- Primeiro cabeçote: `0:1`
	- Último cabeçote: `0:3`

| Cabeçote  | Posição 	    | Ordenamento 	| Observação 					|
|---------- |-------------- |-------------- |------------------------------ |
| 1		 	| Topo esquerdo	| 				| Início						|
| 2			| Inferior  	| 1				|								|
| 3			| Inferior  	| 2				|								|
| 4		 	| Inferior  	| 3				|								|
| 5			| Inferior  	| 4				|								|
| 6			| Inferior  	| 5				|								|
| 7		 	| Inferior  	| 6				|								|
| 8		 	| Inferior  	| 7				|								|
| 9		 	| Inferior	    | 8				|								|
| 10		| Topo direito  | 				| Final (x = medida da peça)	|
| 11		| Superior  	| 1			 	|								|
| 12		| Superior  	| 2		 		|								|
| 13		| Superior  	| 3			 	|								|
| 14		| Superior  	| 4		 		|								|
| 15		| Superior  	| 5		 		|								|
| 16		| Traseiro  	| 1		 		|								|
| 17		| Traseiro  	| 2		 		|								|
| 18		| Traseiro	    | 3		 		|								|
| 19		| Traseiro  	| 4		 		|								|

## Lógica de programação
### Casos
- Caso `Side == 0:1` ou `Side == 0:3`
	- Agrupar elementos onde `Y` e `Side` sejam iguais
- Senão
	- Agrupar elementos onde `X` e `Side` sejam iguais
