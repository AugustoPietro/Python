'''
Código para demonstrar que o Python tem uma sintaxe versátil para fazer a mesma coisa de formas diferentes.
O algoritmo deverá solicitar dois números que serão somados ao usuário.
'''

# Jeito 1 : Criando variável para armazenar o resultado

num1 = int(input("Digite o primeiro número: "))
num2 = int(input("Digite o segundo número: "))
soma = num1 + num2

print("{} + {} = {}".format(num1, num2, soma))

# Jeito 2 : Criando variáveis em apenas uma linha

n1, n2 = input('Digite o primeiro número: '), input('Digite o segundo número: ')
# # O 'eval' dispensa declaração do tipo de variável # #
print(f'{n1} + {n2} =',eval(f'{n1} + {n2}'))

# Jeito 3 : Fazendo tudo em apenas uma linha

print('{} + {} = {}'.format(nro1 := float(input("Digite o primeiro número:")), nro2 := float(input("Digite o segundo número:")), nro1 + nro2))