# MD-Furação


## Roadmap
- [ ] Automatizar a informação das informações de furação.
- [ ] Criar mecanismo automático que crie padrão de furação para as furadeiras lidear através da interação dos softwares Ardis e Topsolid.
- [ ] Criar interface gráfica para consulta das informações na máquina.


## Lógica de programação

1. Agrupar os furos por `side`;
2. Novo agrupamento:
	- Caso `side` seja igual a `0:1` ou `0:3`:
		- Agrupar subgrupos por `Y`;
	- Caso contrário:
		- Agrupar subgrupos por `X`;
3. Varrer a lista de furos agrupados pelo `side`;
4. Varrer a lista de cabeçotes até encontrar o primeiro que seja da posição desejada e que não esteja sendo utilizado.
5. Varrer a lista de furo agrupados por `side` e (`x` ou `y`) e definir em qual broca o furo será colocado.


## Definições

| Atributo			 	| Descrição									|
|----------------------	|------------------------------------------	|
| **Side**				| Lado/face de furação		   				|
| **CRN**			 	| Sentido de furação da broca			   	|
| **DP**			   	| Profundidade do furo					 	|
| **TRH ou T**		 	| Se é um furo passante (atravessa a peça) 	|
| **DIA ou Diâmetro**   | Diâmetro do furo							|
| **X**					| Eixo horizontal (esquerda para direita)  	|
| **Y**					| Eixo ~vertical (cima para baixo)~	?distancia? (trás para frente)		|
| **Z**					|										 	|


### Cabeçotes

| Side  | CRN	| Posição		  			|
|------	|------	|--------------------------	|
| 0 : 0 | 1		| Inferior 					|
| 0 : 1 | 1	 	| Topo/Vertical Esquerda	|
| 0 : 2 | 	 	|				  			|
| 0 : 3 | 4	 	| Topo/Vertical Direita	 	|
| 0 : 4 | 	 	|						   	|
| 0 : 5 | 4	 	| Superior					|

| CRN   | Posição		  							|
|------ |------------------------------------------	|
| 1		| Esquerda para Direita / Baixo para Cima	|
| 2		| 											|
| 3		| 											|
| 4		| Direita para Esqeurda / Cima para Baixo 	|

- Posições
	- Primeiro cabeçote: `0:1`
	- Último cabeçote: `0:3`


### Furadeiras

#### Furadeira-1

| Atributo					| Valor	|
|--------------------------	|------	|
| Número de cabeçotes		| 19	|
| Número de brocas			| 21	|
| Distância entre os pinos	| 32	|

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

#### Lidear: F400-T

| Atributo					| Valor	|
|--------------------------	|------	|
| Número de cabeçotes		| 19	|
| Número de brocas			| 21	|
| Distância entre os pinos	| 32	|

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
| 10		| Superior		| 1				|								|
| 11		| Superior  	| 2			 	|								|
| 12		| Superior  	| 3		 		|								|
| 13		| Superior  	| 4			 	|								|
| 14		| Superior  	| 5		 		|								|
| 15		| Superior  	| 6		 		|								|
| 16		| Topo direito  | 				| Final (x = medida da peça)	|

### F500-B

- Marca: Lidear
- Nome: F500-B
- Nro cabeçotes: 16
- Nro brocas: 21
- Distancia pinos: 32
- Distancia min cabeçotes: 96
- Bipartido: True
- Eixo y: normal
- Posicao cabeçotes:
	- esquerda: [1]
	- direita: [16]
	- inferior: [2, 3, 4, 5, 6, 7, 8, 9]
	- superior: [10, 11, 12, 13, 14, 15]			
- Dimensões:
	- espessura_peca:
		- min: 8
		- max: 70
	- largura_peca:
		- min: 30
		- max: 870
	- comprimento_peca:
		- min: 115
		- max: 2750
