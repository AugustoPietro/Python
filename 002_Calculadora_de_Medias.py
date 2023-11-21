'''
Objetivo do programa:
    Auxiliar docentes no cálculo de médias dos alunos.
O que faz o algoritmo:
    Calcula a média aritimética ou geométrica de cada aluno
    Retorna a situação do aluno (aprovado, reprovado ou em recuperação)
    Informa o aproveitamento da turma ou grupo de alunos
'''
from math import sqrt

# Funções utilizadas

def mediaAritmetica(n1, n2):
    return (n1 + n2) / 2

def mediaGeometrica(n1, n2):
    return sqrt(n1 * n2)

# Inicialização de contadores
      
aprovados = 0
recuperacao = 0
reprovados = 0

# Inicio do algoritmo

print('\n--CALCULADORA DE MÉDIA ESTUDANTIL--\n')

while True:
    tipo_med = int(input('Qual o tipo de média deseja calcular?\n1) Média Aritmética\n2) Média Geométrica\n'))
    qtd_alunos = int(input('Digite a quantidade de alunos: '))

    # Calculo de média aritmética (condição 1)

    if tipo_med == 1:
        for aluno in range(qtd_alunos):
            media = mediaAritmetica(float(input(f'\n1ª nota do {1 + aluno}º aluno: ')), float(input(f'\n2ª nota do {1 + aluno}º aluno: ')))
            
            if (media >= 6 and media <= 10):
                aprovados += 1
                print(f'A média é {media}\nAluno aprovado!\n')
            elif (media >= 3 and media < 6):
                recuperacao += 1
                print(f'A média é {media}\nAluno em recuperação.\n')
            elif (media >= 0 and media < 3):
                reprovados += 1
                print(f'A média é {media}\nAluno reprovado.\n')
            else:
                print('Média inválida!\nA nota deve estar entre 0 e 10.\n')
        break
    
    # Cálculo de média geométrica (condição 2)

    elif tipo_med == 2:
        for aluno in range(qtd_alunos):
            media = mediaGeometrica(float(input(f'\n1ª nota do {1 + aluno}º aluno: ')), float(input(f'\n2ª nota do {1 + aluno}º aluno: ')))
            
            if (media >= 6 and media <= 10):
                aprovados += 1
                print(f'A média é {media}\nAluno aprovado!\n')
            elif (media >= 3 and media < 6):
                recuperacao += 1
                print(f'A média é {media}\nAluno em recuperação.\n')
            elif (media >= 0 and media < 3):
                reprovados += 1
                print(f'A média é {media}\nAluno reprovado.\n')
            else:
                print('Média inválida!\nA nota deve estar entre 0 e 10.\n')
        break
    
    else:
        print('Opção inválida.\nDigite 1 ou 2.\n')

# Resultado da turma

print(f'{((aprovados / qtd_alunos)*100):.1f}% dos alunos foram APROVADOS')
print(f'{((recuperacao / qtd_alunos)*100):.1f}% dos alunos estão EM RECUPERAÇÃO')
print(f'{((reprovados / qtd_alunos)*100):.1f}% dos alunos foram REPROVADOS')