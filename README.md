# MD-Furação

## Roadmap
- [ ] Automatizar a informação das informações de furação.

- [ ] Criar mecanismo automático que crie padrão de furação para as furadeiras lidear através da interação dos softwares Ardis e Topsolid.

- [ ] Criar interface gráfica para consulta das informações na máquina.

## Lógica de programação

### Definições

- Lados
    - `Side 0 : 0` - Horizontal inferior
    - `Side 0 : 1` - Vertical esquerda
    - `Side 0 : 2` - 
    - `Side 0 : 3` - Vertical direita
    - `Side 0 : 4` - 
    - `Side 0 : 5` - Frontal
- Posições
    - Primeiro cabeçote: `0:1`
    - Último cabeçote: `0:3`


### Casos
- Caso `Side == 0:1` ou `Side == 0:3`
    - Agrupar elementos onde `Y` e `Side` sejam iguais
- Senão
    - Agrupar elementos onde `X` e `Side` sejam iguais
