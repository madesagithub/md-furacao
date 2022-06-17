# MD-Furação


## Roadmap
- [x] Ler arquivo .bpp
	- [x] Obter informações sobre a peça
	- [x] Obter lista de furos, agrupados conforme o cabeçote
- [ ] Cadastro de furadeiras:
	- [ ] Cadastro geral
		- [x] Lidear F500-B
		- [ ] Lidear F400-T
	- [ ] Edição de atributos no momento da utilização
- [x] Agrupar furos que utilizarão o mesmo cabeçote
- [ ] Aplicar furos em cabeçote:
	- [ ] Definir mandril
		- [x] Cabeçote inteiro
		- [ ] Cabeçote bipartido
	- [ ] Definir deslocamento(`X`) do cabeçote:
		- [x] Cabeçote inteiro
		- [ ] Cabeçote bipartido:
			- [ ] Definir limites de deslocamento(`X`)
			- [ ] Considerar possibilidade de troca por um cabeçote menor
	- [ ] Definir deslocamento(Y) do cabeçote:
		- [ ] Cabeçote inteiro
		- [ ] Cabeçote bipartido
			- [ ] Considerar opção de deslocamento(`Y`) do eixo rotacionado
- [ ] Definir deslocamento(`Y`) da furadeira
	- [ ] Batente de fundo refletir nos cálculos dos cabeçotes
- [ ] Automatizar a informação das informações de furação.
- [ ] Criar mecanismo automático que crie padrão de furação para as furadeiras Lidear através da interação dos softwares Ardis e Topsolid.
- [ ] Criar interface gráfica para consulta das informações na máquina.

### Verificação de Peças

#### Peças simples
- [ ] TAMPO MAL 15X440X2280.bpp
- [ ] BASE 15X400X1046/BASE 15X400X1046.bpp
- [ ] BASE AÉREO 12X266X1174/BASE AÉREO 12X266X1174.bpp

#### Peças com furo superior
- [ ] BASE 12X489X1772/BASE 12X489X1772.bpp
- [ ] BASE BALCÃO 15X450X1198/BASE BALCÃO 15X450X1198.bpp
- [ ] DIVISÓRIA BALCÃO 12X400X645/DIVISÓRIA BALCÃO 12X400X645.bpp
- [ ] LATERAL ESQ GAVETEIRO 15X436X724/LATERAL ESQ GAVETEIRO 15X436X724.bpp

#### Peças com agregado
- [ ] DIVISÓRIA 12X387X1652.bpp

#### Peças com bipartido
- [ ] DIVISÓRIA BALCÃO 12X450X645/DIVISÓRIA BALCÃO 12X450X645.bpp
- [ ] DIVISÓRIA DIR 15X440X1685/DIVISÓRIA DIR 15X440X1685.bpp
- [ ] LATERAL DIR 15X544X2175/LATERAL DIR 15X544X2175.bpp
- [ ] TAMPO SUPERIOR 12X489X574/TAMPO SUPERIOR 12X489X574.bpp


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

### Problema de limites
1. Verificar quais possuem mais problemas
2. Verificar quais podem ser movidos para cima
3. Ordenar cabeçotes que possuem menos furos
4. Mover para cima um a um e verificar problemas

### Problema de agregado
5. Verificar limites dos cabeçotes superiores
6. Verificar onde o agregado pode ser colocado (cabeçotes inferiores ou superiores)
7. Remover cabecote e incluir agregado


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
| 4		| Direita para Esquerda / Cima para Baixo 	|

- Posições
	- Primeiro cabeçote: `0:1`
	- Último cabeçote: `0:3`


### Furadeiras

#### Furadeira-1
| Atributo						| Valor	|
|------------------------------	|------	|
| Número de cabeçotes			| 19	|
| Número de brocas				| 21	|
| Distância entre os mandris	| 32	|

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

#### Lidear F400-T
| Atributo						| Valor	|
|------------------------------	|------	|
| Número de cabeçotes			| 19	|
| Número de brocas				| 21	|
| Distância entre os mandris	| 32	|

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
- Distancia mandris: 32
- Distancia min cabeçotes: 96
- Bipartido: True
- Eixo y: normal
- Posicao cabeçotes:
	- esquerda: [1]
	- direita: [16]
	- inferior: [2, 3, 4, 5, 6, 7, 8, 9]
	- superior: [10, 11, 12, 13, 14, 15]			
- Dimensões da peça:
	- espessura:
		- min: 8
		- max: 70
	- largura:
		- min: 30
		- max: 870
	- comprimento:
		- min: 115
		- max: 2750
