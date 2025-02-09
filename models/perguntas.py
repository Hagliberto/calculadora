import random

def gerar_pergunta(operacoes):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operacao_nomes = {'+': 'Adição', '-': 'Subtração', '*': 'Multiplicação', '/': 'Divisão'}
    operacao = random.choice(list(operacao_nomes.keys())) if 'Todas' in operacoes else random.choice(operacoes)
    operacao_nome = operacao_nomes[operacao]
    
    if operacao == '+':
        resposta_correta = num1 + num2
    elif operacao == '-':
        resposta_correta = num1 - num2
    elif operacao == '*':
        resposta_correta = num1 * num2
    else:
        num1 = num1 * num2  # Garante que a divisão seja exata
        resposta_correta = num1 / num2
    
    return f'{num1} {operacao} {num2} = ?', resposta_correta, operacao_nome
