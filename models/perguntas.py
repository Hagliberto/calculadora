import random
import operator

def gerar_pergunta(operacoes, dificuldade="fácil"):
    """Gera uma pergunta matemática com base no nível de dificuldade e adiciona (), [], {} para melhor visualização."""
    
    operacao_nomes = {'+': 'Adição', '-': 'Subtração', '*': 'Multiplicação', '/': 'Divisão', '**': 'Exponenciação'}
    operacao_funcoes = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '**': operator.pow}

    if dificuldade == "fácil":
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        formato = random.choice(["({} {} {})", "[{} {} {}]", "{{{} {} {}}}"])
    
    elif dificuldade == "média":
        num1 = random.randint(10, 50)
        num2 = random.randint(5, 25)
        formato = random.choice(["({} {} {})", "[{} {} {}]", "{{{} {} {}}}"])

    elif dificuldade == "difícil":
        num1 = random.randint(50, 100)
        num2 = random.randint(10, 50)
        formato = random.choice(["({} {} {})", "[{} {} {}]", "{{{} {} {}}}"])

    elif dificuldade == "complexa":
        expressao = gerar_expressao_complexa()
        resposta_correta = eval(expressao)
        return f"{expressao} = ?", resposta_correta, "Expressão Complexa"
    
    else:
        raise ValueError("Dificuldade inválida. Escolha entre: fácil, média, difícil, complexa.")

    operacao = random.choice(list(operacao_nomes.keys())) if 'Todas' in operacoes else random.choice(operacoes)

    # Ajusta operações para evitar erros matemáticos
    if operacao == '/':
        num1 = num1 * num2  # Garante que a divisão seja exata
        resposta_correta = round(operacao_funcoes[operacao](num1, num2), 2)  # Arredondar para 2 casas decimais
    elif operacao == '**' and dificuldade != "fácil":
        num2 = random.randint(2, 3)  # Evita expoentes muito altos
        resposta_correta = operacao_funcoes[operacao](num1, num2)
    else:
        resposta_correta = operacao_funcoes[operacao](num1, num2)

    expressao_formatada = formato.format(num1, operacao, num2)

    return f"{expressao_formatada} = ?", resposta_correta, operacao_nomes[operacao]

def gerar_expressao_complexa():
    """Gera uma expressão matemática mais complexa, usando parênteses (), colchetes [] e chaves {}"""
    numeros = [str(random.randint(1, 50)) for _ in range(4)]
    operacoes = random.choices(['+', '-', '*', '/'], k=3)
    formatos = [
        "(({0} {1} {2}) {3} {4})",
        "[({0} {1} {2}) {3} {4}]",
        "{{({0} {1} {2}) {3} {4}}}"
    ]
    formato_escolhido = random.choice(formatos)
    
    expressao = formato_escolhido.format(numeros[0], operacoes[0], numeros[1], operacoes[1], numeros[2])
    return expressao
