import streamlit as st
import datetime
import os
import pandas as pd
from models.perguntas import gerar_pergunta
from views.historico import exibir_historico
from views.pontuacao import exibir_pontuacao

# Diretório onde os históricos diários serão salvos
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)  # Garante que a pasta de dados exista

def salvar_pontuacao_por_dia(nome, pontos, data, historico):
    """Salva apenas a última entrada do histórico em um arquivo separado por dia, incluindo a operação e o resultado."""
    
    if not historico:
        return  # Evita salvar caso o histórico esteja vazio

    data_formatada = data.strftime('%Y-%m-%d')
    arquivo_csv = os.path.join(DATA_DIR, f"historico_{data_formatada}.csv")

    # Salvar apenas a última resposta dada, incluindo operação e resultado
    ultima_entrada = [historico[-1]]  # Captura apenas o último registro
    df = pd.DataFrame(ultima_entrada, columns=['Nome', 'Data', 'Operação', 'Resultado'])

    # Salvar apenas a nova linha, sem sobrescrever ou duplicar
    if os.path.exists(arquivo_csv):
        df.to_csv(arquivo_csv, mode='a', header=False, index=False)
    else:
        df.to_csv(arquivo_csv, index=False)

    # Resetar histórico para evitar duplicação
    st.session_state.historico = []

def login():
    """Tela de login para capturar o nome do usuário antes de iniciar o jogo."""
    with st.form(key='nome_form'):
        nome = st.text_input('Digite seu nome:')
        confirmar_nome = st.form_submit_button('Confirmar')
        if confirmar_nome and nome:
            st.session_state.nome = nome
            st.toast(f'Bem-vindo(a), {nome}!', icon='🎉')
            st.balloons()
            st.rerun()

def main():
    st.title('Jogo da Tabuada')
    st.write('Teste seus conhecimentos de matemática!')
    
    # Garante que o usuário faça login antes de acessar o jogo
    if 'nome' not in st.session_state:
        login()
        return
    
    st.write(f'Jogador: **{st.session_state.nome}**')
    
    operacoes = st.multiselect('Escolha as operações:', ['Todas', 'Adição', 'Subtração', 'Multiplicação', 'Divisão'], default=['Todas'])
    operacoes_mapeadas = {'Adição': '+', 'Subtração': '-', 'Multiplicação': '*', 'Divisão': '/'}
    operacoes_selecionadas = [operacoes_mapeadas[op] for op in operacoes if op in operacoes_mapeadas] if 'Todas' not in operacoes else list(operacoes_mapeadas.values())
    
    if 'pontos' not in st.session_state:
        st.session_state.pontos = {'Certo': 0, 'Errado': 0}
    if 'pergunta' not in st.session_state or 'resposta_correta' not in st.session_state:
        st.session_state.pergunta, st.session_state.resposta_correta, st.session_state.operacao = gerar_pergunta(operacoes_selecionadas)
    if 'historico' not in st.session_state:
        st.session_state.historico = []
    if 'inicio' not in st.session_state:
        st.session_state.inicio = datetime.datetime.now().strftime('%Y-%m-%d')

    if st.toggle('Mostrar histórico de pontuação'):
        exibir_historico()
    else:
        with st.form(key='resposta_form'):
            st.write(f'Pergunta: {st.session_state.pergunta}')

            # Inicializa o campo apenas uma vez
            if "campo_resposta" not in st.session_state:
                st.session_state["campo_resposta"] = ""

            # Campo de texto sem `value`
            resposta_usuario = st.text_input("Digite sua resposta:", key="campo_resposta")

            # Botão de submissão do formulário
            responder = st.form_submit_button("Responder")

            if responder:
                try:
                    resposta_usuario = float(resposta_usuario.strip()) if resposta_usuario.strip() else None

                    if resposta_usuario is not None:
                        resultado = "Certo" if resposta_usuario == st.session_state.resposta_correta else "Errado"
                        st.session_state.pontos[resultado] += 1

                        data_atual = datetime.datetime.now().date()
                        ultima_resposta = [[st.session_state.nome, data_atual, st.session_state.operacao, resultado]]
                        salvar_pontuacao_por_dia(st.session_state.nome, st.session_state.pontos, data_atual, ultima_resposta)

                        # Resetar o campo de resposta antes de atualizar a interface indiretamente
                        st.session_state.pop("campo_resposta", None)

                        # Gerar uma nova pergunta antes de atualizar a interface
                        st.session_state.pergunta, st.session_state.resposta_correta, st.session_state.operacao = gerar_pergunta(operacoes_selecionadas)

                        st.rerun()
                    else:
                        st.error("Por favor, insira um número válido.")
                except ValueError:
                    st.error("Por favor, insira um número válido.")

    exibir_pontuacao()
