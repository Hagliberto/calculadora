import random
import operator
from fractions import Fraction
import streamlit as st

def gerar_pergunta(operacoes, dificuldade="fácil"):
    """Gera uma pergunta matemática, incluindo cálculos com frações e exibição colorida."""

    operacao_nomes = {'+': 'Adição', '-': 'Subtração', '*': 'Multiplicação', '/': 'Divisão', '**': 'Exponenciação'}

    if isinstance(operacoes, set):
        operacoes = list(operacoes)  # Converter para lista para evitar erro

    if dificuldade == "complexa":
        expressao, expressao_exibida = gerar_expressao_complexa(incluir_fracoes=True)

        # Garante que a expressão seja válida para o eval()
        expressao = expressao.replace("{", "(").replace("}", ")")

        try:
            resposta_correta = eval(expressao)
            if isinstance(resposta_correta, Fraction):
                resposta_correta = resposta_correta  # Mantém como fração exata
        except Exception as e:
            print(f"Erro ao avaliar a expressão: {expressao}")
            raise e  # Lança o erro para depuração
        
        # Exibir a expressão colorida no Streamlit
        exibir_expressao_colorida(expressao_exibida)

        return f"{expressao_exibida} = ?", resposta_correta, "Expressão Complexa"

    # Geração de expressões normais
    num1 = random.randint(1, 50)
    num2 = random.randint(1, 50)
    operacao = random.choice(operacoes)

    resposta_correta = eval(f"{num1} {operacao} {num2}")
    expressao_formatada = f"({num1} {operacao} {num2})"

    return f"{expressao_formatada} = ?", resposta_correta, operacao_nomes[operacao]


def gerar_expressao_complexa(incluir_fracoes=False):
    """Gera uma expressão matemática complexa garantindo que frações estejam bem agrupadas."""
    
    def gerar_numero():
        """Gera um número inteiro ou uma fração corretamente formatada para exibição e cálculo."""
        if incluir_fracoes and random.random() < 0.5:  # 50% de chance de gerar fração
            numerador = random.randint(1, 10)
            denominador = random.randint(2, 10)  # Evita divisão por zero
            
            # Representação correta da fração com parênteses para evitar múltiplas divisões seguidas
            fracao_calculo = f"Fraction({numerador}, {denominador})"
            fracao_exibida = f"({numerador}/{denominador})"
            return fracao_calculo, fracao_exibida
        else:
            valor = str(random.randint(1, 50))
            return valor, valor

    # Gerar números aleatórios (inteiros ou frações corretamente formatadas)
    numeros = [gerar_numero() for _ in range(6)]
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

    # Criando a expressão para cálculo e a exibição para o usuário
    expressao = formato_escolhido.format(
        numeros[0][0], operacoes[0], numeros[1][0],
        operacoes[1], numeros[2][0], operacoes[2],
        numeros[3][0]
    )

    expressao_exibida = formato_escolhido.format(
        numeros[0][1], operacoes[0], numeros[1][1],
        operacoes[1], numeros[2][1], operacoes[2],
        numeros[3][1]
    )

    # Substituir {} por () para evitar erros no eval()
    expressao = expressao.replace("{", "(").replace("}", ")")
    expressao_exibida = expressao_exibida.replace("{", "(").replace("}", ")")

    return expressao, expressao_exibida


def exibir_expressao_colorida(expressao):
    """Exibe a expressão no Streamlit com cores para facilitar a identificação dos parênteses."""

    # Definição das cores para cada nível de agrupamento
    cores = {
        "(": '<span style="color: blue; font-weight: bold;">(</span>',
        ")": '<span style="color: blue; font-weight: bold;">)</span>',
        "[": '<span style="color: green; font-weight: bold;">[</span>',
        "]": '<span style="color: green; font-weight: bold;">]</span>',
        "{": '<span style="color: orange; font-weight: bold;">{</span>',
        "}": '<span style="color: orange; font-weight: bold;">}</span>',
    }

    # Substituir os caracteres por versões coloridas
    expressao_colorida = expressao
    for char, cor in cores.items():
        expressao_colorida = expressao_colorida.replace(char, cor)

    # Exibir no Streamlit com estilo aprimorado
    st.markdown(
        f"""
        <div style="
            background-color: #FFFBEA; 
            padding: 10px; 
            border-radius: 20px; 
            border: 1px solid #FFD700; 
            text-align: center;
            font-size: 25px;">
            <span style="color: red; font-weight: bold;">{expressao_colorida}</span>
        </div>
        """,
        unsafe_allow_html=True
    )