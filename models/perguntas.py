import random
import operator

def gerar_pergunta(operacoes, dificuldade="fácil"):
    """Gera uma pergunta matemática com base no nível de dificuldade e adiciona (), [], {} conforme necessário."""
    
    operacao_nomes = {'+': 'Adição', '-': 'Subtração', '*': 'Multiplicação', '/': 'Divisão', '**': 'Exponenciação'}
    operacao_funcoes = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '**': operator.pow}

    if isinstance(operacoes, set):
        operacoes = list(operacoes)  # Converter para lista para evitar erro

    if dificuldade == "complexa":
        expressao = gerar_expressao_complexa()
        expressao = expressao.replace("{", "(").replace("}", ")")  # Garante que não tenha erro no eval()
        
        print(f"Expressão gerada: {expressao}")  # Log para depuração
        try:
            resposta_correta = eval(expressao)
        except Exception as e:
            print(f"Erro ao avaliar a expressão: {expressao}")
            raise e  # Lança o erro para depuração
        
        return f"{expressao} = ?", resposta_correta, "Expressão Complexa"

    # Geração de expressões normais
    if dificuldade == "fácil":
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
    elif dificuldade == "média":
        num1 = random.randint(10, 50)
        num2 = random.randint(5, 25)
    elif dificuldade == "difícil":
        num1 = random.randint(50, 100)
        num2 = random.randint(10, 50)

    operacao = random.choice(operacoes)

    if operacao == '/':
        num1 = num1 * num2  # Garante que a divisão seja exata
        resposta_correta = round(operacao_funcoes[operacao](num1, num2), 2)
    elif operacao == '**' and dificuldade != "fácil":
        num2 = random.randint(2, 3)  # Evita expoentes muito altos
        resposta_correta = operacao_funcoes[operacao](num1, num2)
    else:
        resposta_correta = operacao_funcoes[operacao](num1, num2)

    expressao_formatada = f"({num1} {operacao} {num2})"

    return f"{expressao_formatada} = ?", resposta_correta, operacao_nomes[operacao]


def gerar_expressao_complexa():
    """Gera uma expressão matemática complexa seguindo a hierarquia: (), depois [], depois {}."""
    
    # Gerar números aleatórios
    numeros = [str(random.randint(1, 50)) for _ in range(6)]
    operacoes = [random.choice(['+', '-', '*', '/']) for _ in range(5)]  

    if len(operacoes) < 5:
        raise ValueError("Número insuficiente de operadores gerados")

    # Formatos respeitando a hierarquia correta: () → [] → {}
    formatos = [
        "(({0} {1} {2}) {3} ({4} {5} {6}))",  # Apenas ()  
        "[(({0} {1} {2}) {3} ({4} {5} {6}))]",  # () dentro de []
        "{{[(({0} {1} {2}) {3} ({4} {5} {6}))]}}"  # () dentro de [] dentro de {}
    ]

    # Escolher o formato correto dependendo da profundidade desejada
    profundidade = random.choice([1, 2, 3])  # Aleatório entre 1, 2 ou 3 níveis de parênteses

    if profundidade == 1:
        formato_escolhido = formatos[0]
    elif profundidade == 2:
        formato_escolhido = formatos[1]
    else:
        formato_escolhido = formatos[2]

    expressao = formato_escolhido.format(
        numeros[0], operacoes[0], numeros[1],
        operacoes[1], numeros[2], operacoes[2],
        numeros[3]
    )

    # Substituir {} por () para evitar erros no eval()
    expressao = expressao.replace("{", "(").replace("}", ")")

    return expressao
